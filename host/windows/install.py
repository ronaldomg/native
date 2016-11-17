#!/usr/bin/env python

from _winreg import SetValueEx, CreateKeyEx, HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE, KEY_ALL_ACCESS, REG_SZ, FlushKey
from os import path
from win32clipboard import CloseClipboard, OpenClipboard, GetClipboardData

c_path = path.dirname(path.realpath(__file__))+path.sep
extensionID = raw_input('Digite o valor da extensao ou pressione enter para colar')

if extensionID == '':
    OpenClipboard()
    extensionID = GetClipboardData()
    CloseClipboard()

print('extensionID: '+extensionID)

if extensionID != '':

    jobDone = False
    try:
        host_key = r'SOFTWARE\Google\Chrome\NativeMessagingHosts\br.com.bluefocus.printhost'
        hostKey = CreateKeyEx(HKEY_LOCAL_MACHINE, host_key, 0, KEY_ALL_ACCESS)
        SetValueEx(hostKey, "", 0, REG_SZ, c_path + "br.com.bluefocus.printhost-win.json")
        FlushKey(hostKey)

        list_key = r'SOFTWARE\Google\Chrome\NativeMessagingHosts\br.com.bluefocus.printlist'
        listKey = CreateKeyEx(HKEY_LOCAL_MACHINE, list_key, 0, KEY_ALL_ACCESS)
        SetValueEx(listKey, "", 0, REG_SZ, c_path + "br.com.bluefocus.printlist-win.json")
        FlushKey(listKey)
        jobDone = True
    except WindowsError as e:
        if e.winerror == 5:
            print u"N\xe3o foi poss\xedvel alterar o registro do sistema, para instalar a extens\xe3o, " \
                  u"\xe9 necess\xe1rio alterar o registro."
        else:
            print e.message

    try:
        host_key = r'Software\Google\Chrome\NativeMessagingHosts\br.com.bluefocus.printhost'
        hostKey = CreateKeyEx(HKEY_CURRENT_USER, host_key, 0, KEY_ALL_ACCESS)
        SetValueEx(hostKey, "", 0, REG_SZ, c_path + "br.com.bluefocus.printhost-win.json")
        FlushKey(hostKey)

        list_key = r'Software\Google\Chrome\NativeMessagingHosts\br.com.bluefocus.printlist'
        listKey = CreateKeyEx(HKEY_CURRENT_USER, list_key, 0, KEY_ALL_ACCESS)
        SetValueEx(listKey, "", 0, REG_SZ, c_path + "br.com.bluefocus.printlist-win.json")
        FlushKey(listKey)
        jobDone = True
    except WindowsError as e:
        if e.winerror == 5:
            print u"N\xe3o foi poss\xedvel alterar o registro do sistema, para instalar a extens\xe3o, " \
                  u"\xe9 necess\xe1rio alterar o registro."
        else:
            print e.message

    if jobDone:
        try:
            fo = open(c_path + "br.com.bluefocus.printhost-win.json", 'w+')
            fo.write('{')
            fo.write('"name": "br.com.bluefocus.printhost",')
            fo.write('"description": "BlueFocus Print Host",')
            fo.write('"path": "printhost.exe",')
            fo.write('"type": "stdio",')
            fo.write('"allowed_origins": [')
            fo.write('"chrome-extension://' + extensionID + '/"')
            fo.write(']')
            fo.write('}')

        except IOError:
            print 'Erro ao alterar dados do arquivo json'
            jobDone = False

    if not jobDone:
        print "Ocorreram erros que impediram o sistema de ser configurado corretamente, verifique por favor"

    raw_input("Aperte enter para finalizar")
    quit()
else:
    print("O valor solicitado nao foi informado.")
    print("para finalizar a instalacao execute o arquivo configura-host.exe em: " + path.dirname(path.realpath(__file__)) + path.sep)
    raw_input("Aperte enter para finalizar")
    quit()
