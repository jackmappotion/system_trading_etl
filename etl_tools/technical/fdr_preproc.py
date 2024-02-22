import pandas as pd


class OhlcvPreProc:
    def __init__(self, ohlcvs: pd.DataFrame) -> None:
        self.ohlcvs = ohlcvs

    @staticmethod
    def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
        df.columns = [col.lower() for col in df.columns]
        return df

    @staticmethod
    def rename_index(df: pd.DataFrame) -> pd.DataFrame:
        df.index.name = df.index.name.lower()
        return df

    def __call__(self) -> pd.DataFrame:
        ohlcvs = self.ohlcvs.copy()
        ohlcvs = self.rename_columns(ohlcvs)
        ohlcvs = self.rename_index(ohlcvs)
        return ohlcvs


class StockPreProc:
    def __init__(self, stocks: pd.DataFrame) -> None:
        self.stocks = stocks

    @staticmethod
    def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
        column_rename_dict = {
            "Code": "stock_code",
            "Name": "stock_nm",
            "Market": "market",
            "Stocks": "shares",
            "Marcap": "market_cap",
        }
        renamed_df = df.rename(columns=column_rename_dict)
        return renamed_df

    @staticmethod
    def slice_columns(df: pd.DataFrame) -> pd.DataFrame:
        using_columns = ["stock_code", "stock_nm", "market", "shares", "market_cap"]
        sliced_df = df.loc[:, using_columns]
        return sliced_df

    def __call__(self) -> pd.DataFrame:
        stocks = self.stocks.copy()
        stocks = self.rename_columns(stocks)
        stocks = self.slice_columns(stocks)
        return stocks
