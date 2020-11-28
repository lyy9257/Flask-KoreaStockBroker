# 대신증권 - 계좌정보
import win32com.client

class Account():
    def __init__(self):
        self.obj_CpTrade_CpTdUtil = win32com.client.Dispatch('CpTrade.CpTdUtil')
        self.obj_CpTrade_CpTd6032 = win32com.client.Dispatch("CpTrade.CpTd6032")
        self.obj_CpTrade_CpTd6033 = win32com.client.Dispatch("CpTrade.CpTd6033")

        self.initCheck = self.obj_CpTrade_CpTdUtil.TradeInit(0)

    ## 계좌정보
    def account_info(self):
        acc = self.obj_CpTrade_CpTdUtil.AccountNumber[0] #계좌번호
        accFlag = self.obj_CpTrade_CpTdUtil.GoodsList(acc, 1)  # 주식상품 구분

        ### 필요 데이터 입력
        self.obj_CpTrade_CpTd6033.SetInputValue(0, acc)
        self.obj_CpTrade_CpTd6033.SetInputValue(1, accFlag[0])
        self.obj_CpTrade_CpTd6033.SetInputValue(2, 20)
        self.obj_CpTrade_CpTd6033.SetInputValue(3, '2') # 0프로 기준 수익률 출력

        self.obj_CpTrade_CpTd6033.BlockRequest()    
        
        ### 계좌이름, 총평가액, 평가손익, D+2예수금
        name = self.obj_CpTrade_CpTd6033.GetHeaderValue(0)
        tot_amount = self.obj_CpTrade_CpTd6033.GetHeaderValue(3)
        profit_amount = self.obj_CpTrade_CpTd6033.GetHeaderValue(4)
        twoday_amount = self.obj_CpTrade_CpTd6033.GetHeaderValue(9)

        ## 결과값 리턴
        res = {
            'name': name,
            'tot_amount':tot_amount,
            'profit_amount':profit_amount,
            'twoday_amount':twoday_amount
        }

        return res

    ## 계좌잔고 조회
    def request6032(self):
        bIsFist = True

        while True:
            self.obj_CpTrade_CpTd6032.BlockRequest()
            # 통신 및 통신 에러 처리
            rqStatus = self.obj_CpTrade_CpTd6032.GetDibStatus()
            rqRet = self.obj_CpTrade_CpTd6032.GetDibMsg1()

            print("통신상태", rqStatus, rqRet)
            if rqStatus != 0:
                return False
 
            cnt = self.obj_CpTrade_CpTd6032.GetHeaderValue(0)

            print('데이터 조회 개수', cnt)
 
            # 헤더 정보는 한번만 처리
            if bIsFist == True:
                sumJango = self.obj_CpTrade_CpTd6032.GetHeaderValue(1)
                sumSellM = self.obj_CpTrade_CpTd6032.GetHeaderValue(2)
                sumRate = self.obj_CpTrade_CpTd6032.GetHeaderValue(3)

                print('잔량평가손익', sumJango, '매도실현손익',sumSellM, '수익률',sumRate)

                bIsFist = False
 
            for i in range(cnt):
                item = {}
                item['종목코드'] = self.obj_CpTrade_CpTd6032.GetDataValue(12, i)  # 종목코드
                item['종목명'] = self.obj_CpTrade_CpTd6032.GetDataValue(0, i)  # 종목명
                item['전일잔고'] = self.obj_CpTrade_CpTd6032.GetDataValue(2, i)
                item['금일매수수량'] = self.obj_CpTrade_CpTd6032.GetDataValue(3, i)
                item['금일매도수량'] = self.obj_CpTrade_CpTd6032.GetDataValue(4, i)
                item['금일잔고'] = self.obj_CpTrade_CpTd6032.GetDataValue(5, i)
                item['평균매입단가'] = self.obj_CpTrade_CpTd6032.GetDataValue(6, i)
                item['평균매도단가'] = self.obj_CpTrade_CpTd6032.GetDataValue(7, i)
                item['현재가'] = self.obj_CpTrade_CpTd6032.GetDataValue(8, i)
                item['잔량평가손익'] = self.obj_CpTrade_CpTd6032.GetDataValue(9, i)
                item['매도실현손익'] = self.obj_CpTrade_CpTd6032.GetDataValue(10, i)
                item['수익률'] = self.obj_CpTrade_CpTd6032.GetDataValue(11, i)

            if (self.obj_CpTrade_CpTd6032.Continue == False):
                break

        return True
