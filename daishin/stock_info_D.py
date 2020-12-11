# 대신증권 - 종목정보
import win32com.client
from datetime import datetime
import pandas as pd
import time

class StockInfo():

    ## 초기화
    def __init__(self):
        self.obj_CpSysDib_StockChart = win32com.client.Dispatch('CpSysDib.StockChart')
        self.obj_CpSysDib_MarketEye = win32com.client.Dispatch('CpSysDib.MarketEye')
        self.obj_CpSysDib_CpSvr7238 = win32com.client.Dispatch('CpSysDib.CpSvr7238')
        self.obj_CpSysDib_CpSvr7254 = win32com.client.Dispatch('CpSysDib.CpSvr7254')
        self.obj_CpSysDib_CpMarketEye = win32com.client.Dispatch('CpSysDib.MarketEye')
        self.obj_CbSysDib_CpStatus = win32com.client.Dispatch('CpUtil.CpCybos')
        self.obj_CpTrade_CpTdUtil = win32com.client.Dispatch('CpTrade.CpTdUtil')
        self.obj_CpUtil_CpCodeMgr = win32com.client.Dispatch('CpUtil.CpCodeMgr')
        self.obj_DsCbo1_StockMst = win32com.client.Dispatch("DsCbo1.StockMst")

        self.initCheck = self.obj_CpTrade_CpTdUtil.TradeInit(0)

    ## 종목정보 호출
    def get_stockfeatures(self, code):
        
        ## 1차 데이터 호출
        result = {
            '이름': self.obj_CpUtil_CpCodeMgr.CodeToName(code),
            '증거금률(%)': self.obj_CpUtil_CpCodeMgr.GetStockMarginRate(code),
            '시장구분코드 ': self.obj_CpUtil_CpCodeMgr.GetStockMarketKind(code),
            '부구분코드': self.obj_CpUtil_CpCodeMgr.GetStockSectionKind(code),
            '감리': self.obj_CpUtil_CpCodeMgr.GetStockControlKind(code),
            '관리': self.obj_CpUtil_CpCodeMgr.GetStockSupervisionKind(code),
            '현재상태': self.obj_CpUtil_CpCodeMgr.GetStockStatusKind(code),
            '결산기': self.obj_CpUtil_CpCodeMgr.GetStockFiscalMonth(code),
            'K200여부': self.obj_CpUtil_CpCodeMgr.GetStockKospi200Kind(code),
            '업종코드': self.obj_CpUtil_CpCodeMgr.GetStockSectionKind(code),
            '상장일': self.obj_CpUtil_CpCodeMgr.GetStockListedDate(code),
            '신용가능여부': self.obj_CpUtil_CpCodeMgr.IsStockCreditEnable(code),
        }

        ## 2차 데이터 입력값 설정
        _fields = [67, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 86, 87, 88,
            89, 90, 91, 92, 93, 94, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107,
            108, 109, 110, 111
        ]

        _keys = ['PER', 'EPS', '자본금(백만)', '액면가', '배당률', '배당수익률', '부채비율', '유보율',
            '자기자본이익률(ROE)', '매출액증가율', '경상이익증가율', '순이익증가율', '투자심리', '매출액',
            '경상이익', '당기순이익', 'BPS', '영업이익증가율', '영업이익', '매출액영업이익률', '매출액경상이익률',
            '이자보상비율', '분기BPS', '분기매출액증가율', '분기영업이익증가율', '분기경상이익증가율', '분기순이익증가율',
            '분기매출액', '분기영업이익', '분기경상이익', '분기당기순이익', '분기매출액영업이익률', '분기매출액경상이익률',
            '분기ROE', '분기이자보상비율', '분기유보율', '분기부채비율', '최근분기년월'
        ]

        self.obj_CpSysDib_MarketEye.SetInputValue(0, _fields)
        self.obj_CpSysDib_MarketEye.SetInputValue(1, code)
        self.obj_CpSysDib_MarketEye.BlockRequest()

        field_length = self.obj_CpSysDib_MarketEye.GetHeaderValue(0)

        if field_length > 0:
            for i in range(field_length):
                value = self.obj_CpSysDib_MarketEye.GetDataValue(i, 0)
                if type(value) == float:
                    value = round(value, 4)
                    
                result[_keys[i]] = value
        
        return result

    ## 차트데이터 호출
    def get_chart(self, code, unit='D', n=None, date_from=None, date_to=None):
            
        _fields = [0, 2, 3, 4, 5, 8, 9]
        _keys = ['date', 'open', 'high', 'low', 'close', 'volume', 'vol_amount']

        if date_to is None:
            date_to = datetime.today().strftime('%Y%m%d')

        ## 필요 데이터 입력
        self.obj_CpSysDib_StockChart.SetInputValue(0, code) # 주식코드: A, 업종코드: U

        if n is not None:
            self.obj_CpSysDib_StockChart.SetInputValue(1, ord('2'))  # 0: ?, 1: 기간, 2: 개수
            self.obj_CpSysDib_StockChart.SetInputValue(4, n)  # 요청 개수

        if date_from is not None or date_to is not None:
            if date_from is not None and date_to is not None:
                self.obj_CpSysDib_StockChart.SetInputValue(1, ord('1'))  # 0: ?, 1: 기간, 2: 개수
            if date_from is not None:
                self.obj_CpSysDib_StockChart.SetInputValue(3, date_from)  # 시작일
            if date_to is not None:
                self.obj_CpSysDib_StockChart.SetInputValue(2, date_to)  # 종료일

        self.obj_CpSysDib_StockChart.SetInputValue(5, _fields)  # 필드
        self.obj_CpSysDib_StockChart.SetInputValue(6, ord(unit))
        self.obj_CpSysDib_StockChart.SetInputValue(9, ord('1')) # 0: 무수정주가, 1: 수정주가
        
        ## 호출
        self.obj_CpSysDib_StockChart.BlockRequest()

        length = self.obj_CpSysDib_StockChart.GetHeaderValue(3)
        list_item = []

        for i in range(length):
            temp_idx = []
            for j in range(len(_keys)):
                temp_idx.append(self.obj_CpSysDib_StockChart.GetDataValue(j, i))
            list_item.append(temp_idx)

        result = pd.DataFrame(data=list_item, columns=_keys).reset_index()

        return result
        

    ## 종목별 공매도 추이
    def get_shortstockselling(self, code):

        ## 필요 데이터 설정
        _fields = [0, 1, 2, 4, 5, 6, 7]
        _keys = [
            '거래일', '종가', '전일대비', '거래량', '공매도량', '공매도비중', '공매도거래대금'
            ]

        ## 데이터 입력
        self.obj_CpSysDib_CpSvr7238.SetInputValue(0, code) 
        
        ## 호출
        self.obj_CpSysDib_CpSvr7238.BlockRequest()
        
        ## 데이터 수신
        data_len = self.obj_CpSysDib_CpSvr7238.GetHeaderValue(0)
        list_item = []

        for i in range(data_len):
            temp_idx = []
            for j in _fields:
                temp_idx.append(self.obj_CpSysDib_CpSvr7238.GetDataValue(j, i))
            list_item.append(temp_idx)

        result = pd.DataFrame(data=list_item, columns=_keys).reset_index()

        return result

    # 여러종목 데이터 호출
    ## input : code(list)
    def get_MarketEye(self, code_list):
        
        ## 필요 데이터 설정
        ## 코드, 종목명, 시간,
        ## 현재가, 시가, 고가, 저가,
        ## 매도호가, 매수호가, 거래량, 거래대금,
        ## 총매도호가잔량, 총매수호가잔량, 최우선매도호가잔량, 최우선매수호가잔량 
        _fields = (0, 17, 1, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16) 
        _keys = ('종목코드', '시간', '현재가', '시가',
            '고가', '저가', '매도호가', '매수호가', '거래량',
            '거래대금', '총매도호가잔량', '총매수호가잔량',
            '최우선매도호가잔량', '최우선매수호가잔량', '종목명' 
        )
        _sorted_keys = ['종목코드', '종목명', '시간', '현재가',
            '시가', '고가', '저가', '매도호가', '매수호가',
            '거래량', '거래대금', '총매도호가잔량', '총매수호가잔량',
            '최우선매도호가잔량', '최우선매수호가잔량' 
        ]

        ## 입력 변수 설정
        self.obj_CpSysDib_CpMarketEye.SetInputValue(0, _fields) # 요청 필드
        self.obj_CpSysDib_CpMarketEye.SetInputValue(1, code_list)  # 종목코드 or 종목코드 리스트
        
        ## 요청
        self.obj_CpSysDib_CpMarketEye.BlockRequest()

        ## 호출 후 데이터 길이 확인
        list_idx = self.obj_CpSysDib_CpMarketEye.GetHeaderValue(2)

        ## 결과값 저장
        res_value = []

        for i in range(list_idx):
            temp = []

            for j in range(len(_fields)):
                temp.append(self.obj_CpSysDib_CpMarketEye.GetDataValue(j, i))
                
            res_value.append(temp)
        
        res = pd.DataFrame(data=res_value, columns=_keys).reset_index()
        result = res[_sorted_keys]
        
        return result

    ## 10단호가 호출
    ## input : code(str)
    def get_hogainfo(self, code, k):
        
        ## 필요 데이터 설정
        buy_dataframe = pd.DataFrame(columns = ['매수매도여부', '호가', '잔량'])
        sell_dataframe = pd.DataFrame(columns = ['매수매도여부', '호가', '잔량'])
        k = int(k)

        ## 데이터 입력(종목코드)
        self.obj_DsCbo1_StockMst.SetInputValue(0, code)

        ## 데이터 호출
        self.obj_DsCbo1_StockMst.BlockRequest()

        buy_dataframe['매수매도여부'] = ['매수'] * k
        buy_dataframe['호가'] = [self.obj_DsCbo1_StockMst.GetDataValue(1, x)  for x in range(k)] # 매수호가
        buy_dataframe['잔량'] = [self.obj_DsCbo1_StockMst.GetDataValue(3, x) for x in range(k)]  # 매수호가 잔량
        
        sell_dataframe['매수매도여부'] = ['매도'] * k
        sell_dataframe['호가'] = [self.obj_DsCbo1_StockMst.GetDataValue(0, x) for x in range(k)]
        sell_dataframe['잔량'] = [self.obj_DsCbo1_StockMst.GetDataValue(2, x) for x in range(k)]    
        
        result = pd.concat([buy_dataframe, sell_dataframe]).reset_index(drop=True)

        return result

    def get_tradematrix(self, code):
        
        ## 필요데이터 선언
        matrix_idx = [0, 14, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        matrix_col = [
            '날짜', '종가' ,'개인', '외국인', '기관계', '금융투자', '보험', '투신',
            '은행', '기타금융', '연기금등', '기타법인', '기타외인',
            '사모펀드', '국가지자체'
        ]
        matrix_df = pd.DataFrame(columns = matrix_col)

        ## 데이터 입력(종목코드)
        self.obj_CpSysDib_CpSvr7254.SetInputValue(0, code)
        self.obj_CpSysDib_CpSvr7254.SetInputValue(1, 4)
        self.obj_CpSysDib_CpSvr7254.SetInputValue(4, '1')
        self.obj_CpSysDib_CpSvr7254.SetInputValue(5, 0)

        ## 데이터 저장
        self.obj_CpSysDib_CpSvr7254.BlockRequest()

        ## 연속조회
        while self.obj_CpSysDib_CpSvr7254.Continue:
            self.obj_CpSysDib_CpSvr7254.BlockRequest()
            data_len = self.obj_CpSysDib_CpSvr7254.GetHeaderValue(1)

            ## 연속 조회용 데이터프레임(데이터 이어붙이기)
            temp_matrix_df = pd.DataFrame(columns = matrix_col)

            ## 데이터 호출
            for i in range(len(matrix_idx)):
                t = matrix_idx[i]
                temp_res = [self.obj_CpSysDib_CpSvr7254.GetDataValue(t, i) for i in range(data_len)]
                temp_matrix_df[matrix_col[i]] = temp_res

            matrix_df = pd.concat([matrix_df, temp_matrix_df]).reset_index(drop=True)

        res = matrix_df[::-1].reset_index(drop=True)

        return res