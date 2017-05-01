import time
from flask import Flask, redirect, url_for, render_template
app = Flask(__name__)

def ssend(msg):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", "12345"))
    s.send(msg+"\n")
    data = s.recv(1024)
    s.close()

@app.route('/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(path)

@app.route('/step1/<path:path>')
def step1(path):
    if path.startwsith("filter/"):
        ssend("filter," + path.split("/")[1])
    elif path == "pictures":
        ssend("takepic,")
        time.sleep(2)
        ssend("accept,")
        return redirect(url_for('step2'))
    
    return render_template('step1.html')

@app.route('/step2/<path:path>')
def step2(path):
    if path.startwsith("frame/"):
        ssend("border," + path.split("/")[1])
    elif path == "select":
        ssend("select,")
        return redirect(url_for('step3'))
    
    return render_template('step2.html')

@app.route('/step3/<path:path>')
def step3(path):
    if path != "":
        ssend("copies," + path)
        time.sleep(2)
        ssend("confirm,")
        return redirect(url_for('step1'))
    
    return render_template('step3.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
