import json

from daishin import account_info_D, connection_D, order_D, stock_info_D
# from eBest import account_info_eB, connection_eB, order_eB, stock_info_eb

# 중계모듈
# 거래증권사에 따른 매매모듈설정
class Broker():
    def __init__(self, broker, id, pw, certpw):

        self._broker = broker
        self._id = id
        self._pw = pw
        self._certpw = certpw

        ## 대신증권 
        if self._broker == 'DAISHIN':
            self.con_broker = connection_D.Connection()
            self.acc_info = account_info_D.Account()
            self.stock_info = stock_info_D.StockInfo()
            self.order = order_D.Order()
        
        ## 이후 기타 증권사 추가예정

        else:
            print("XX")

    ## 로그인 
    def login(self):
        res_login = self.con_broker.login(
            self._id, self._pw, self._certpw
        )

        if res_login is True:
            status = 200
            message = "로그인 성공!"
            broker = "%s" %self._broker

        else:
            status = 400
            message = "로그인 실패"
            broker = "%s" %self._broker

        return (status, message, broker)

    ## 연결 체크
    def check_connection(self):
        res = self.con_broker._connected()
        
        if res is True:
            status = 200 
            msg_body = "연결되었습니다."

        else:
            status = 400
            msg_body = "연결되지 않았습니다."

        res = {
            'status' : status,
            'broker' : self._broker,
            'res' : msg_body
        }

        return res

    ## 계좌정보 요청
    def account_info(self):
        self.con_broker.avoid_reqlimitwarning()
        result = self.acc_info.account_info()

        return result

    ## 종목정보
    def get_stockfeatures(self, code):
        self.con_broker.avoid_reqlimitwarning()
        featuredata = self.stock_info.get_stockfeatures(code)
        result = json.dumps(featuredata, indent=4, ensure_ascii=False)

        return result

    ## 가격정보
    def get_price(self, code, n, date_from, date_to):
        self.con_broker.avoid_reqlimitwarning()
        pricedata = self.stock_info.get_chart(code, unit='D', n=n, date_from=date_from, date_to=date_to)
        result = json.dumps(json.loads(pricedata.to_json(orient='records')), indent=4, ensure_ascii=False)

        return result

    ## 공매도정보
    def get_stockshortselling(self, code):
        self.con_broker.avoid_reqlimitwarning()
        shortdata = self.stock_info.get_shortstockselling(code)
        result = json.dumps(json.loads(shortdata.to_json(orient='records')), indent=4, ensure_ascii=False)

        return result

    ## 매수
    def buy(self, acc, code, amount, price):
        self.con_broker.avoid_reqlimitwarning()
        result = self.order.buy(acc, code, amount, price)
        
        if result is False:
            res = {
                'server_status' : 400,
                'message': '주문 초기화 실패!'
            }
        
        res = {
            'Server_Status' : 200,
            'cybos_status' : result[0],
            'message' : result[1]
        }
            
        return res

    ## 매도
    def sell(self, acc, code, amount, price):
        self.con_broker.avoid_reqlimitwarning()
        result = self.order.sell(acc, code, amount, price)

        if result is False:
            res = {
                'server_status' : 400,
                'message': '주문 초기화 실패!'
            }
        
        res = {
            'Server_Status' : 200,
            'cybos_status' : result[0],
            'message' : result[1]
        }

        return res