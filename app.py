from flask import Flask, render_template
import os,time,socket
from flask import Flask, render_template, send_file, request
import signal
import pythoncom
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("mocker.html")

@app.route("/",methods = ['GET', 'POST'])
def va():
    df = request.form.get('submit1')
    df1 = request.form.get('submit3')
    df2 = request.form.get('submit2')
    if df == "start_assistant":
        print("\nStarting the Virtual Assistant - GROOT\n")
        try:
            pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
            os.system('python groot.py')
        except pythoncom.com_error:
            pass
        #os.system("\& \"C:/Users/Abhishek Reddy/AppData/Local/Microsoft/WindowsApps/python3.10.exe\" \"c:/Users/Abhishek Reddy/Desktop/GROOT/groot.py\"")
        message = "start_assistant"
        return render_template("mocker1.html",msg=message)
    if df1 == "restart_assistant":
        print("\nRestarting the Virtual Assistant - GROOT\n")
        try:
            pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
            os.system('python groot.py')
        except pythoncom.com_error:
            pass
        message = "restart_assistant"
        return render_template("mocker2.html",msg=message)
    if df2 == "stop":
        print("\nStopping the Flask Server.\n")
        os.kill(os.getpid(), signal.SIGINT)
        message = "stop"
        return render_template("mocker3.html",msg=message)

if __name__ == "__main__":
    app.run(debug=True)