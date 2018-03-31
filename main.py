# -*- coding: utf-8 -*-
"""
#  main.py
Description :
@Author     : Jianfeng
@Date       : 2018/3/11
@Software   : PyCharm
"""

import os
import sys
import time
from apps.ChinaUnicom import ChinaUnicomApp

mobile = os.getenv('unicom_mobile')
mobilepwd = os.getenv('unicom_pwd')

def unicomCheckin():
    unicom = ChinaUnicomApp()
    loginFlag, loginContent = unicom.login_CU(mobile, mobilepwd)
    signininFlag, signinContent = unicom.signin_CU()
    mailcontent_CU = loginContent + signinContent + '\n\n'
    return mailcontent_CU

if __name__=='__main__':
    try:
        msg = unicomCheckin()
        exitCode = 0
    except Exception as e:
        print('Error: ' + msg)
        exitCode = 1

    sys.exit(exitCode)
