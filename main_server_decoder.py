#-*-coding: utf-8-*-
from flask import Flask,render_template,request
import os

obj_serverApp=Flask(__name__,static_folder='static')
@obj_serverApp.route('/vizovSait_decode',methods=["POST"])
def vizovSait_decode():
    I_gotFromBrowser= int(request.form['parWeb_znach'])
    print(I_gotFromBrowser,type(I_gotFromBrowser))
    if I_gotFromBrowser==2:
      print("Zapusk blocknota")
      os.system("start cmd /C \"D:/Programs/npp.7.4.1.bin/notepad++.exe\"")
      
    elif I_gotFromBrowser==3:
        print("Zakritie blocknota")
        os.system("%SystemRoot%/system32/taskkill /f /im notepad++.exe")
    return "Ok"
   
@obj_serverApp.route('/')
def home():
    return ""


if __name__=='__main__':
    obj_serverApp.run(host="0.0.0.0",debug=True,port=os.environ.get('PORT',5000))
    