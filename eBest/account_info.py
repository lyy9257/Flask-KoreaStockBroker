## 이베스트 - 계좌정보
import win32com.client
import pythoncom

class XASessionEventHandler:
    login_state = 0

    def OnLogin(self, code, msg):
        if code == "0000":
            print("로그인 성공")
            XASessionEventHandler.login_state = 1
        else:
            print("로그인 실패")


class Account(self):
    def __init__(self):
        self.instXASession = win32com.client.DispatchWithEvents("XA_Session.XASession", XASessionEventHandler)

        id = "아이디"
        passwd = "비밀번호"
        cert_passwd = "공인인증서"

    ## 로그인
    def login(self):
        self.instXASession.ConnectServer("hts.ebestsec.co.kr", 20001)
    
        self.instXASession.Login(id, passwd, cert_passwd, 0, 0)

        while XASessionEventHandler.login_state == 0:
            pythoncom.PumpWaitingMessages()

    ## 계좌정보
    def acoount_info(self, acc_index):

        acc = self.instXASession.GetAccountList(acc_index)
            
        ## 결과값 리턴
        res = {            
            'acc_num': acc,
            'tot_amount':tot_amount,
            'profit_amount':profit_amount,
            'twoday_amount':twoday_amount  
        }

    