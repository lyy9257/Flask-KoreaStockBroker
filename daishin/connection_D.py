'''
대신증권 - 연결
'''
from pywinauto import application
import os
import win32com.client
import time

class Connection():
    def __init__(self):
        self.obj_CpUtil_CpCybos = win32com.client.Dispatch('CpUtil.CpCybos')

    ## 로그인
    def login(self, _id, _pwd, _pwdcert, trycnt=300):
        
        ## 연결 체크 후 연결되었지 않았을 경우 실행 
        if not self._connected():
            self.disconnect()
            self.kill_client()
            app = application.Application()
            app.start(
                'C:\\CREON\\STARTER\\coStarter.exe /prj:cp /id:{id} /pwd:{pwd} /pwdcert:{pwdcert} /autostart'.format(
                    id=_id, pwd=_pwd, pwdcert=_pwdcert
                )
            )

        cnt = 0

        ## 로그인 후 체크 (300초 이내)
        while not self._connected():
            if cnt > trycnt:
                return False

            time.sleep(1)
            cnt += 1

        return True
        
    ## 연결
    def _connected(self):
        b_connected = self.obj_CpUtil_CpCybos.IsConnect

        if b_connected == 0:
            return False

        return True

    ## 연결해제
    def disconnect(self):
        if self.connected():
            self.obj_CpUtil_CpCybos.PlusDisconnect()
            return True

        return False

    ## 강제종료
    def kill_client(self):
        os.system('taskkill /IM coStarter* /F /T')
        os.system('taskkill /IM CpStart* /F /T')
        os.system('taskkill /IM DibServer* /F /T')
        os.system('wmic process where "name like \'%coStarter%\'" call terminate')
        os.system('wmic process where "name like \'%CpStart%\'" call terminate')
        os.system('wmic process where "name like \'%DibServer%\'" call terminate')

    ## 요청제한 감시
    def avoid_reqlimitwarning(self):
        remainTime = self.obj_CpUtil_CpCybos.LimitRequestRemainTime
        remainCount = self.obj_CpUtil_CpCybos.GetLimitRemainCount(1)  # 시세 제한
        
        if remainCount <= 3:
            time.sleep(remainTime / 1000)