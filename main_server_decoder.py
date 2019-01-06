#-*-coding: utf-8-*-
from flask import Flask,render_template,request
from S_compiler import *
import libTestPydModuleFloat as vt
import os
obj_serverApp=Flask(__name__,static_folder='static')
@obj_serverApp.route('/vizovSait_decode',methods=["POST"])
def vizovSait_decode():
    S_gotFromBrowser_ZnachfuSexpr= request.form['znachfuSexpr']
    S_gotFromBrowser_restSexp= request.form['restSexpr']
    print('rest:',S_gotFromBrowser_restSexp)
    mas_S_gotFromBrowser_restSexp=S_gotFromBrowser_restSexp.split()
    I_count=0
    for i in mas_S_gotFromBrowser_restSexp:
        if i=='сложить':
            mas_S_gotFromBrowser_restSexp[I_count]=' + '
        elif i=='вычесть':
            mas_S_gotFromBrowser_restSexp[I_count]=' - '  
        elif i=='умножить':
            mas_S_gotFromBrowser_restSexp[I_count] =' * '  
        elif i=='делить':
            mas_S_gotFromBrowser_restSexp[I_count] =' /  '  
        elif i=='возвести':
            mas_S_gotFromBrowser_restSexp[I_count]=' ^ '
        elif i=='модула':
            mas_S_gotFromBrowser_restSexp[I_count]=' % '  
        elif i=='левая':
            mas_S_gotFromBrowser_restSexp[I_count] =' [ '  
        elif i=='правая' :
            mas_S_gotFromBrowser_restSexp[I_count] =' ] '
        elif i=='на':
            mas_S_gotFromBrowser_restSexp[I_count] = ' '
        elif  i=='скобка' :
            mas_S_gotFromBrowser_restSexp[I_count] = ' '         
        I_count+=1    
    S_gotFromBrowser_restSexp=""
    for i in  mas_S_gotFromBrowser_restSexp:
       S_gotFromBrowser_restSexp+=i+" " 
        
    print('raw WebPars:',S_gotFromBrowser_ZnachfuSexpr,S_gotFromBrowser_restSexp)
    
    fObj_CompilText=open('tmpFile_compilText.tmp','a')
    if  S_gotFromBrowser_ZnachfuSexpr=='$':
        fObj_CompilText.write('($ ')
    if S_gotFromBrowser_ZnachfuSexpr=='arif':
         S_partTextProg='(arif '+S_gotFromBrowser_restSexp +")"
         fObj_CompilText.write(S_partTextProg)
    if S_gotFromBrowser_ZnachfuSexpr=='userCos':
        fObj_CompilText.write("(callUserCos)")   
    if S_gotFromBrowser_ZnachfuSexpr=='z':
        fObj_CompilText.write("(print z)")          
    if  S_gotFromBrowser_ZnachfuSexpr==')': 
     fObj_CompilText.write(')')
     fObj_CompilText.close() 
     fObj_CompilText=open('tmpFile_compilText.tmp','r')
     S_textProgram=fObj_CompilText.read()
     obj_LispMach=LispMach()
     obj_LispMach.me_recurs_evalPerList_SMrV(read(S_textProgram))
     vectorKintK_opCode=obj_LispMach.me_ret_byteCode_SVrL()
     vectorKintK_opCode.append(HALT)
     vt.eval(vectorKintK_opCode,obj_LispMach.fi_int_startIp,0)
     fObj_CompilText.close()
     with  open('tmpFile_compilText.tmp','w') as fObj_CompilText:
         fObj_CompilText.truncate(0)
     #if I_gotFromBrowser==2:
      #print("Zapusk blocknota")
      #os.system("start cmd /C \"D:/Programs/npp.7.4.1.bin/notepad++.exe\"")
      
    #elif I_gotFromBrowser==3:
        #print("Zakritie blocknota")
        #os.system("%SystemRoot%/system32/taskkill /f /im notepad++.exe")
    return "Ok"
   
@obj_serverApp.route('/')
def home():
    return ""


if __name__=='__main__':
    obj_serverApp.run(host="0.0.0.0",debug=True,port=os.environ.get('PORT',5000))
    