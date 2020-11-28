# **Flask-KoreaStockBroker**

증권사 API를 Flask 기반으로 제작하여

범용 환경에서 트레이딩 할 수 있도록 한다.

(현재는 대신증권만 지원합니다.)


* * *

## **사용방법**

1. 32비트 가상환경을 생성합니다.

2. 의존성을 설치합니다.
    > pip install -r requirements.txt

3. CreonPlus를 실행합니다.

4. config.cfg 파일에 정보를 입력합니다.
 
        [BROKER]
        
        BROKER_NAME = DAISHIN
        
        BROKER_ID = (대신증권 ID)
        
        BROKER_PW = (대신증권 비밀번호)
            
        CERT_PW = (공인인증 비밀번호)

6. main.py 파일을 실행합니다.
    > python main.py


* * *


## **API 명세**

1. ### 로그인 조회

    - endpoint : /connection

    - method : GET

    - argument
        - None.

    - result (Example)
        > http://127.0.0.1:5000/connection

            "broker": "DAISHIN",
            
            "res": "연결되었습니다.",
            
            "status": 200

2. ### 계좌 조회

    - endpoint : /accountinfo

    - method : GET

    - argument
        - None.

    - result (Example)
        > http://127.0.0.1:5000/accountinfo

            "name": (계좌 사용자 이름)

            "profit_amount": 0,

            "tot_amount": 0,

            "twoday_amount": (D+2 예수금)       

3. ### 차트 데이터 조회

    - endpoint : /chart

    - method : GET
    
    - argument
        - code : 종목코드(Axxxxxx, Qxxxxxx)
        - n : 조회갯수
        - date_from : 조회시작날짜
        - date_to : 조회종료날짜(default : 당일)

    - result (Example)
        > http://127.0.0.1:5000/chart?code=A233740&n=20

        > http://127.0.0.1:5000/chart?code=A233740&date_from=20200501

        > http://127.0.0.1:5000/chart?code=A233740&date_from=20200501&date_to=20200701

            "index": 0,
            "date": 20201127,
            "open": 12900,
            "high": 13490,
            "low": 12900,
            "close": 13395,
            "volume": 32898683,
            "vol_amount": 437723000000

4. ### 종목정보 조회

    - endpoint : /stockfeatures

    - method : GET
    
    - argument
        - code : 종목코드(Axxxxxx, Qxxxxxx)

    - result (Example)
        > http://127.0.0.1:5000/stockfeatures?code=A207940

            "이름": "삼성바이오로직스",
            "증거금률(%)": 40,
            "시장구분코드 ": 1,
            "부구분코드": 1,
            "감리": 0,
            "관리": 0,
            "현재상태": 0,
            "결산기": 12,
            "K200여부": 10,
            "업종코드": 1,
            "상장일": 20161110,
            "신용가능여부": 1,
            "PER": 148.76,
            "EPS": 5371,
            "자본금(백만)": 165412,
            "액면가": 2500,
            "배당률": 0.0,
            "배당수익률": 0.0,
            "부채비율": 35.76,
            "유보율": 2532.48,
            "자기자본이익률(ROE)": 0.0,
            "매출액증가율": 30.94,
            "경상이익증가율": -48.7,
            "순이익증가율": -9.46,
            "투자심리": 0.0,
            "매출액": 701591,
            "경상이익": 155435000000,
            "당기순이익": 202904000000,
            "BPS": 67994,
            "영업이익증가율": 64.77,
            "영업이익": 91742000000,
            "매출액영업이익률": 13.08,
            "매출액경상이익률": 22.15,
            "이자보상비율": 3.58,
            "분기BPS": 67994,
            "분기매출액증가율": 103.33,
            "분기영업이익증가율": 0.0,
            "분기경상이익증가율": 0.0,
            "분기순이익증가율": 0.0,
            "분기매출액": 789470,
            "분기영업이익": 200210000000,
            "분기경상이익": 189265000000,
            "분기당기순이익": 144753000000,
            "분개매출액영업이익률": 25.36,
            "분기매출액경상이익률": 23.97,
            "분기ROE": 4.36,
            "분기이자보상비율": 16.07,
            "분기유보율": 2619.77,
            "분기부채비율": 36.42,
            "최근분기년월": 202009


5. ### 공매도정보 조회
    
     - endpoint : /short

     - method : GET
     
     - argument
       - code : 종목코드(Axxxxxx, Qxxxxxx)

     - result (Example)
        > http://127.0.0.1:5000/short?code=A233740
        
            "index": 0,
            "거래일": 20201127,
            "종가": 799000,
            "전일대비": 0,
            "거래량": 88639,
            "공매도량": 25,
            "공매도비중": 0.0282,
            "공매도거래대금": 2007

  
* * *

## **주요 사항**
1. 매수, 매도 모듈은 구현되어 있으나 장중 테스트를 수행하지 않았습니다.
   
   현재 사용을 권장하지 않습니다.

* * *

## **참고 글**
 [퀀티랩 - 대신증권 크레온(Creon) HTS 브리지 서버 만들기 (Flask 편)](http://blog.quantylab.com/creon_hts_bridge.html)

* * *
