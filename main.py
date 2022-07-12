from flask import Flask, request, json
from weasyprint import HTML, CSS
import os

app = Flask(__name__)


def htlm_template(title,ruleName,message,imageUrl):
    # 1. Combine them together using a long f-string
    html = f'''
        <html>
            <head>
                <title>{title}</title>
            </head>
            <body>
                <h1>{ruleName}</h1>
                <p>{message}</p>
                <img src="{imageUrl}" alt="alert_image""> 
            </body>
        </html>
        '''
    # 2. Write the html string as an HTML file
    with open('html_report.html', 'w') as f:
        f.write(html)
    # 3. html to pdf conversion
    css = CSS(string='''
        @page {size: A4; margin: 1cm;} 
        th, td {border: 1px solid black;}
        ''')
    try:
        HTML('html_report.html').write_pdf('january/report_w1.pdf', stylesheets=[css])
    except FileNotFoundError:
        # Creation of path.
        dir_path = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(dir_path, 'january')
        os.mkdir(path)

        HTML('html_report.html').write_pdf('january/report_w1.pdf', stylesheets=[css])

@app.route('/')
def hello():
    return 'webhooks xd'

@app.route('/reports', methods=['POST'])
def githubIssue():
    data = request.json
    htlm_template(data['title'], data['ruleName'], data['message'], data['imageUrl'])
    return data


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.get('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

if __name__ == '__main__':
    app.run(debug=True)
