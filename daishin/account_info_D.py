# 대신증권 - 계좌정보
import pandas as pd
import win32com.client

class Account():

    ## 초기화
    def __init__(self):
        self.obj_CpTrade_CpTdUtil = win32com.client.Dispatch('CpTrade.CpTdUtil')
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
            'acc_num': acc,
            'tot_amount':tot_amount,
            'profit_amount':profit_amount,
            'twoday_amount':twoday_amount
        }

        return res

    ## 주식잔고 조회(6033)
    def account_stock_info(self):

        ## 필요데이터 선언
        stock_account_idx = [12, 0, 3, 7, 17, 18, 11, 15]
        stock_account_col = [
            '종목코드', '종목명', '(결제)잔고수량', '(체결)잔고수량', 
            '체결장부단가', '손익단가', '수익률', '매도가능수량'
        ]
        stock_account_df = pd.DataFrame(columns = stock_account_col)
    

        ### 계좌정보 호출
        acc = self.obj_CpTrade_CpTdUtil.AccountNumber[0] #계좌번호
        accFlag = self.obj_CpTrade_CpTdUtil.GoodsList(acc, 1)  # 주식상품 구분

        ### 필요 데이터 입력
        self.obj_CpTrade_CpTd6033.SetInputValue(0, acc)
        self.obj_CpTrade_CpTd6033.SetInputValue(1, accFlag[0])
        self.obj_CpTrade_CpTd6033.SetInputValue(2, 50)
        self.obj_CpTrade_CpTd6033.SetInputValue(3, '2') # 0프로 기준 수익률 출력

        self.obj_CpTrade_CpTd6033.BlockRequest()
        
        data_len = self.obj_CpTrade_CpTd6033.GetHeaderValue(7)
        print(data_len)
        ## 연속 조회용 데이터프레임(데이터 이어붙이기)
        temp_stock_account_df = pd.DataFrame(columns = stock_account_col)

        ## 데이터 호출
        for i in range(len(stock_account_col)):
            t = stock_account_idx[i]
            temp_res = [self.obj_CpTrade_CpTd6033.GetDataValue(t, i) for i in range(data_len)]
            temp_stock_account_df[stock_account_col[i]] = temp_res

        stock_account_df = pd.concat(
            [stock_account_df, temp_stock_account_df]).reset_index(drop=True)

        stock_account_df['수익률'] = stock_account_df['수익률'].round(2).astype(str)
        
        return stock_account_df
