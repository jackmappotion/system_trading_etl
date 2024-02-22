import pandas as pd


class StockPreProc:
    def __init__(self, stocks) -> None:
        self.stocks = stocks

    @staticmethod
    def rename_columns(df):
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
    def slice_columns(df):
        using_columns = ["stock_code", "stock_nm", "market", "shares", "market_cap"]
        sliced_df = df.loc[:, using_columns]
        return sliced_df

    def __call__(self):
        stocks = self.stocks.copy()
        stocks = self.rename_columns(stocks)
        stocks = self.slice_columns(stocks)
        return stocks
