#-*-coding: utf-8-*-
"""
Голосовая интерпритация
Примечание:
                        Для индификаторов переменных я попытался сделать наподобии Венгерской нотации т.е.
                        идет инфо о типе , потом семантический смысл переменной , например
                        str_char_op , int_ptr , mas_S_OpStack означает массив с типом String ,
                        а mas_I_Or_S_resOpnZapis список ( массив ) с типами Int или String .
                        Имена полей придваряются суффиксом fi ( field ) , например fi_dict_str_int_funcTable это
                        поле - карта с сключом Str , а значением Int .
                        Методы предваряются суффиксом me ( method ) . У функций и методов бывают сигнатуры в конце ,
                        после буквы S ( signature ) , т.е. какие типы функция / метод принимает , например
                        me_recurs_evalPerList_SMrV - метод recurs_evalPerList принимает M - массив / список ,
                        возвращае Пустое т.е V ( void ) . После буквы r ( Return ) идет возвращаемое 
                        функций / методом значение. I это всегда Int , D или F - вещественное число, S - строка
"""
from flask import Flask,render_template,request
from S_compiler import * # компилятор Ukuvchi
import libTestPydModuleFloat as vt # VM Ukuvchi
import os
# обект веб-сервера(фреймоврка) Flask
obj_serverApp=Flask(__name__,static_folder='static')
# вызываемый метод
@obj_serverApp.route('/vizovSait_decode',methods=["POST"])
def vizovSait_decode():
    """
    Sym-expression == (S_funcName S S S ...) смотри Lisp
    S_gotFromBrowser_ZnachfuSexpr==S_funcName ma ->  строка от браузера
    S_gotFromBrowser_restSexp==S S S ... -> от строка  от браузера
    """
    S_gotFromBrowser_ZnachfuSexpr= request.form['znachfuSexpr']
    S_gotFromBrowser_restSexp= request.form['restSexpr']
    # разбиваем S S S ... -> mas_S_
    mas_S_gotFromBrowser_restSexp=S_gotFromBrowser_restSexp.split()
    I_count=0
    # заменяем некоторые слова
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
    # востанавливаем строку -> S S S ...
    for i in  mas_S_gotFromBrowser_restSexp:
       S_gotFromBrowser_restSexp+=i+" " 
        
    # запись в temp файл ддля сессий -> исходный текст ЯП
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
    if  S_gotFromBrowser_ZnachfuSexpr==')': # программа закончена
     fObj_CompilText.write(')') 
     fObj_CompilText.close() # закрываем файл
     # читаем и выполняем
     fObj_CompilText=open('tmpFile_compilText.tmp','r')
     S_textProgram=fObj_CompilText.read()
     obj_LispMach=LispMach()
     obj_LispMach.me_recurs_evalPerList_SMrV(read(S_textProgram))
     vectorKintK_opCode=obj_LispMach.me_ret_byteCode_SVrL()
     vectorKintK_opCode.append(HALT)
     vt.eval(vectorKintK_opCode,obj_LispMach.fi_int_startIp,0)
     fObj_CompilText.close() # закрываем файл
     with  open('tmpFile_compilText.tmp','w') as fObj_CompilText:
         fObj_CompilText.truncate(0) # затираем фаил
    return "Ok"
# просто страница   
@obj_serverApp.route('/')
def home():
    return ""


if __name__=='__main__':
    """ запускаем сервер"""
    obj_serverApp.run(host="0.0.0.0",debug=True,port=os.environ.get('PORT',5000))
    