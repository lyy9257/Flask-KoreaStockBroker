'''
대신증권 - 매수매도
'''
import win32com.client

class Order():
    def __init__(self):
        self.obj_CpTrade_CpTdUtil = win32com.client.Dispatch('CpTrade.CpTdUtil')
        self.objStockOrder = win32com.client.Dispatch("CpTrade.CpTd0311")
        
        self.initCheck = self.obj_CpTrade_CpTdUtil.TradeInit(0)

    ## 매수주문
    ## 계좌번호, 종목코드, 수량, 주문단가
    def buy(self, acc, stock_code, amount, price):
        
        # 주문 초기화
        if (self.initCheck != 0):
            print("주문 초기화 실패")
            
            return False
                
        # 주식 매도 주문
        accFlag = self.obj_CpTrade_CpTdUtil.GoodsList(acc, 1)  # 주식상품 구분

        self.objStockOrder.SetInputValue(0, "2")   #  2: 매수
        self.objStockOrder.SetInputValue(1, acc)   #  계좌번호
        self.objStockOrder.SetInputValue(2, accFlag[0])   #  상품구분 - 주식 상품 중 첫번째
        self.objStockOrder.SetInputValue(3, stock_code)   #  종목코드 - A003540 - 대신증권 종목
        self.objStockOrder.SetInputValue(4, amount)   #  매도수량
        self.objStockOrder.SetInputValue(5, price)   #  매도주문단가
        self.objStockOrder.SetInputValue(7, "0")   #  주문 조건 구분 코드, 0: 기본 1: IOC 2:FOK
        self.objStockOrder.SetInputValue(8, "01")   # 주문호가 구분코드 - 01: 보통
        
        # 매수 주문 요청
        self.objStockOrder.BlockRequest()
        
        rqStatus = self.objStockOrder.GetDibStatus()

        if rqStatus == -1:
            rqStatus = '주문 실패'

        rqRet = self.objStockOrder.GetDibMsg1()
                
        return (rqStatus, rqRet)

    ## 매도주문
    ## 계좌번호, 종목코드, 수량, 주문단가
    def sell(self, acc, stock_code, amount, price):

        # 주문 초기화
        if (self.initCheck != 0):
            print("주문 초기화 실패")
            
            return False
        
        # 주식 매도 주문
        accFlag = self.obj_CpTrade_CpTdUtil.GoodsList(acc, 1)  # 주식상품 구분

        self.objStockOrder.SetInputValue(0, "1")   #  1: 매도
        self.objStockOrder.SetInputValue(1, acc)   #  계좌번호
        self.objStockOrder.SetInputValue(2, accFlag[0])   #  상품구분 - 주식 상품 중 첫번째
        self.objStockOrder.SetInputValue(3, stock_code)   #  종목코드 - A003540 - 대신증권 종목
        self.objStockOrder.SetInputValue(4, amount)   #  매도수량
        self.objStockOrder.SetInputValue(5, price)   #  매도주문단가
        self.objStockOrder.SetInputValue(7, "0")   #  주문 조건 구분 코드, 0: 기본 1: IOC 2:FOK
        self.objStockOrder.SetInputValue(8, "01")   # 주문호가 구분코드 - 01: 보통
        
        # 매도 주문 요청
        self.objStockOrder.BlockRequest()
        
        rqStatus = self.objStockOrder.GetDibStatus()

        if rqStatus == -1:
            rqStatus = '주문 실패'

        rqRet = self.objStockOrder.GetDibMsg1()
                
        return (rqStatus, rqRet)