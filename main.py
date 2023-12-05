from flask import Flask,request,redirect,jsonify, url_for
from LockIP import IPStatus, check

app = Flask(__name__)

@app.route('/new')
def newHtml():
    ip = request.remote_addr
    status = check(ip)
    if status == IPStatus.Lock:
        return "你已在黑名单中"
    elif status == IPStatus.Suspicion:
        return "频繁触发警告"  
    return "lpl 加油!"



@app.route('/form',methods=['POST'])
def form():
    ip = request.remote_addr
    status = check(ip)
    if status == IPStatus.Lock:
        return "你已在黑名单中"
    elif status == IPStatus.Suspicion:
        return "频繁触发警告"  

    #获取上传的文件
    files = request.files
    for key in files:
        file = files[key]
        file.save(f"imgs/{file.filename}")
    return "upload success"


def openserver():
    import datetime
    timestr = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{timestr} 服务器启动中.....')
    
    # 本地测试
    # app.run(host="0.0.0.0", port=8000,debug=True)

    # debug开发模式
    # app.run(host="0.0.0.0", port=8002, ssl_context=(
    #     'www.geek7.top.crt', 'www.geek7.top.key'))

    #生产环境
    from gevent import pywsgi
    server = pywsgi.WSGIServer(('0.0.0.0',8002),app,keyfile='www.geek7.top.key', certfile='www.geek7.top.crt')
    server.serve_forever()


if __name__ == '__main__':
    openserver()
 