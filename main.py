import configparser
from flask import Flask, request, jsonify

from handler import Broker

## 초기 설정
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

config = configparser.ConfigParser()
config.read('config.cfg', encoding='utf-8')

broker_name = config.get('BROKER', 'BROKER_NAME')
id = config.get('BROKER', 'BROKER_ID')
pw = config.get('BROKER', 'BROKER_PW')
cert_pw = config.get('BROKER', 'CERT_PW') 

b = Broker(broker_name, id, pw, cert_pw)

## 연결
@app.route('/connection', methods=['GET', 'POST', 'DELETE'])
def handle_connect(): 
    ## 접속 상태
    if request.method == 'GET':
        # check connection status
        return jsonify(b.check_connection())

    ## 로그인
    elif request.method == 'POST':
        # make connection
        return jsonify(b.login())

## 계좌정보
@app.route('/accountinfo', methods=['GET'])
def get_acc_info():
    res = b.account_info()
    
    return jsonify(res)

## 차트정보
@app.route('/chart', methods=['GET'])
def chart_data():
    
    ## 입력값 확인
    stockcode = request.args.get('code')
    n = request.args.get('n')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')

    ## 필요데이터 (갯수, 시작일)가 없을경우
    if not (n or date_from):
        res = {
            'status' : 400,
            'result' : 'Need to provide "n" or "date_from" argument.'
        }

    res = b.get_price(stockcode, n, date_from, date_to)

    return res

## 종목분석 
@app.route('/stockfeatures', methods=['GET'])
def handle_stockfeatures():
    stockcode = request.args.get('code')

    if not stockcode:
        return '', 400

    res = b.get_stockfeatures(stockcode)

    return res

## 공매도현황
@app.route('/short', methods=['GET'])
def handle_short():
    stockcode = request.args.get('code')
    
    if not stockcode:
        return '', 400

    result = b.get_stockshortselling(stockcode)
    
    return result

# 여러종목 감시
@app.route('/marketeye', methods=['GET'])
def marketeye():
    code_list = request.args.getlist('code', type=str)
    print(code_list)
    
    if not code_list:
        return '', 400

    result = b.marketeye(code_list)
    
    return result

## 매수
@app.route('/buy', methods=['GET', 'DELETE'])
def buy(): 
    acc = request.args.get('acc')
    front_code = request.args.get('front')
    code = request.args.get('code')
    amount = request.args.get('amount')
    price = request.args.get('price')
    
    stock_code = front_code + str(code)

    ## 파라미터 확인
    if request.method == 'GET':
        res = b.buy(acc, stock_code, amount, price)

    ## 로그인
    elif request.method == 'DELETE':
        # make connection
        return False

    return res

## 매도
@app.route('/sell', methods=['GET', 'DELETE'])
def sell(): 
    acc = request.args.get('acc')
    front_code = request.args.get('front')
    code = request.args.get('code')
    amount = request.args.get('amount')
    price = request.args.get('price')
    
    stock_code = front_code + str(code)

    ## 파라미터 확인
    if request.method == 'GET':
        res = b.sell(acc, stock_code, amount, price)

    ## 로그인
    elif request.method == 'DELETE':
        # make connection
        return False

    return res

## 실행
if __name__ == "__main__": 
    app.run(host='0.0.0.0', debug=True)