# Code license: pending author designation; publication not approved.
import io
import unittest
from app import app

HEADER = '日期,类型,类别,金额,备注\n'


class AppTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def upload(self, text, filename='ledger.csv'):
        data = text.encode('utf-8') if isinstance(text, str) else text
        return self.client.post('/analyze', data={'file': (io.BytesIO(data), filename)})

    def test_routes(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('CSV 字段说明', response.text)
        self.assertEqual(self.client.get('/analyze').status_code, 405)
        self.assertEqual(self.client.post('/').status_code, 405)
        with self.client.get('/static/style.css') as stylesheet:
            self.assertEqual(stylesheet.status_code, 200)

    def test_sample_and_normal_upload(self):
        sample = self.client.get('/sample.csv')
        self.assertEqual(sample.status_code, 200)
        self.assertIn('attachment', sample.headers['Content-Disposition'])
        result = self.upload(sample.data)
        self.assertEqual(result.status_code, 200)
        for value in ('5000.00', '62.00', '4938.00', '餐饮', '交通', 'new Blob', '返回首页'):
            self.assertIn(value, result.text)

    def test_bom(self):
        response = self.upload(b'\xef\xbb\xbf' + (HEADER + '2026-11-01,收入,工资,12.34,\n').encode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('12.34', response.text)

    def test_empty(self):
        for text in ('', HEADER):
            with self.subTest(text=text):
                response = self.upload(text)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.text.count('¥ 0.00'), 3)

    def test_missing_file(self):
        for response in (self.client.post('/analyze'), self.upload('', filename='')):
            self.assertEqual(response.status_code, 400)
            self.assertIn('请选择 CSV 文件', response.text)

    def test_bad_encoding(self):
        response = self.upload(b'\xff\xfe')
        self.assertEqual(response.status_code, 400)
        self.assertIn('编码错误', response.text)

    def test_invalid_records(self):
        cases = [
            ('日期,类型,类别,备注\n', '缺列'),
            (HEADER + '2026-11-01,收入,工资\n', '记录缺列'),
            (HEADER + '2026-02-30,支出,餐饮,1,\n', '非法日期'),
            (HEADER + '2026-1-01,支出,餐饮,1,\n', '非法日期'),
            (HEADER + '2026-11-01,转账,餐饮,1,\n', '非法类型'),
            (HEADER + '2026-11-01,支出,,1,\n', '空类别'),
        ]
        for amount, message in [('abc', '非法金额'), ('-1', '金额不能为负数'),
                                ('NaN', '金额必须为有限数值'), ('Infinity', '金额必须为有限数值'),
                                ('1.001', '金额超过两位小数')]:
            cases.append((HEADER + f'2026-11-01,支出,餐饮,{amount},\n', message))
        for text, message in cases:
            with self.subTest(message=message, text=text):
                response = self.upload(text)
                self.assertEqual(response.status_code, 400)
                self.assertIn(message, response.text)
                self.assertNotIn('id="download"', response.text)
                self.assertNotIn('aria-label="收支概览"', response.text)

    def test_no_partial_results(self):
        response = self.upload(HEADER + '2026-11-01,收入,工资,999.99,\n2026-02-30,支出,餐饮,1,\n')
        self.assertEqual(response.status_code, 400)
        self.assertNotIn('999.99', response.text)
        self.assertNotIn('new Blob', response.text)

    def test_size_limit(self):
        response = self.upload(b'a' * (1024 * 1024))
        self.assertEqual(response.status_code, 413)
        self.assertIn('1 MiB', response.text)
        self.assertNotIn('id="download"', response.text)

    def test_html_escaping(self):
        attack = '</script><script>alert(1)</script>'
        response = self.upload(HEADER + f'2026-11-01,支出,{attack},1.00,\n')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(attack, response.text)
        self.assertIn('&lt;/script&gt;', response.text)
        self.assertIn(r'\u003c/script\u003e', response.text)
        self.assertIn('const report = ', response.text)

    def test_malformed_csv(self):
        response = self.upload(HEADER + '"unterminated')
        self.assertEqual(response.status_code, 400)
        self.assertIn('读取失败', response.text)


if __name__ == '__main__':
    unittest.main()
