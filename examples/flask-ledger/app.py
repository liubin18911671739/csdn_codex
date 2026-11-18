# Code license: pending author designation; publication not approved.
import io
from flask import Flask, Request, Response, render_template, request
from werkzeug.exceptions import RequestEntityTooLarge
from ledger_core import LedgerError, analyze

class MemoryRequest(Request):
    def _get_file_stream(self, total_content_length, content_type, filename=None,
                         content_length=None):
        return io.BytesIO()


app = Flask(__name__)
app.request_class = MemoryRequest
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024


@app.get('/')
def index():
    return render_template('index.html')


@app.post('/analyze')
def analyze_upload():
    upload = request.files.get('file')
    if upload is None or not upload.filename:
        return render_template('index.html', error='请选择 CSV 文件。'), 400
    try:
        # Read only into memory; never save the uploaded file.
        text = upload.read().decode('utf-8-sig')
        result = analyze(io.StringIO(text, newline=''))
    except UnicodeError:
        return render_template('index.html', error='编码错误：请使用 UTF-8 或 UTF-8 BOM 编码的 CSV。'), 400
    except LedgerError as exc:
        return render_template('index.html', error=str(exc)), 400
    return render_template('result.html', result=result)


@app.errorhandler(RequestEntityTooLarge)
def too_large(error):
    return render_template('index.html', error='上传超过 1 MiB 上限（含表单开销），请缩小 CSV 文件。'), 413


@app.get('/sample.csv')
def sample():
    data = ('日期,类型,类别,金额,备注\n'
            '2026-11-01,收入,工资,5000.00,合成样例\n'
            '2026-11-02,支出,餐饮,50.00,合成样例\n'
            '2026-11-03,支出,交通,12.00,合成样例\n')
    return Response(data.encode('utf-8-sig'), content_type='text/csv; charset=utf-8',
                    headers={'Content-Disposition': 'attachment; filename="sample.csv"'})
