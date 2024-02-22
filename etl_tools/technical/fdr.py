from tqdm import tqdm
import FinanceDataReader as fdr


class FdrExtractor:
    def __init__(self) -> None:
        self.fdr = fdr

    def load_stocks(self, only_major=True):
        """
        only_major : [KOSPI / KOSDAQ]
        """
        stocks = self.fdr.StockListing("KRX")
        if only_major:
            stocks = stocks[stocks["Market"].isin(["KOSPI", "KOSDAQ"])]
        return stocks

    def load_ohlcv(self, stock_code, start_date, end_date):
        ohlcv = self.fdr.DataReader(symbol=stock_code, start=start_date, end=end_date)
        ohlcv["stock_code"] = stock_code
        return ohlcv

    def load_ohlcvs(self, stock_codes, start_date, end_date):
        ohlcv_list = list()
        for stock_code in tqdm(stock_codes):
            try:
                ohlcv = self.load_ohlcv(stock_code, start_date, end_date)
                ohlcv_list.append(ohlcv)
            except:
                print(stock_code)
