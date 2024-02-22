import datetime as dt
import pandas as pd
from tqdm import tqdm
import FinanceDataReader as fdr

date = dt.date | str


class FdrExtractor:
    def __init__(self) -> None:
        self.fdr = fdr

    def load_stocks(self, only_major: bool = True) -> pd.DataFrame:
        """
        only_major : [KOSPI / KOSDAQ]
        """
        stocks = self.fdr.StockListing("KRX")
        if only_major:
            stocks = stocks[stocks["Market"].isin(["KOSPI", "KOSDAQ"])]
        return stocks

    def load_ohlcv(self, stock_code: str, start_date: date, end_date: date) -> pd.DataFrame:
        ohlcv = self.fdr.DataReader(symbol=stock_code, start=start_date, end=end_date)
        ohlcv["stock_code"] = stock_code
        return ohlcv

    def load_ohlcvs(self, stock_codes: list, start_date: date, end_date: date) -> pd.DataFrame:
        ohlcv_list = list()
        for stock_code in tqdm(stock_codes):
            try:
                ohlcv = self.load_ohlcv(stock_code, start_date, end_date)
                ohlcv_list.append(ohlcv)
            except:
                print(stock_code)
        ohlcvs = pd.concat(ohlcv_list, axis=0)
        return ohlcvs
