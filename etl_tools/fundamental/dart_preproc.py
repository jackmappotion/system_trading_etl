import pandas as pd
from typing import Optional


class FundamentalPreProc:
    """
    Prepocess Fundamental DataFrame
    """
    def __init__(self, fundamentals: pd.DataFrame) -> None:
        self.fundamentals = fundamentals

    def __call__(self, fs_nm: str):
        """
        fs_nm = ['CFS','OFS']
        """
        fundamentals = self.fundamentals
        fundamental = fundamentals[fundamentals["fs_div"] == fs_nm.upper()].copy()
        #
        fundamental["reprt_date"] = pd.to_datetime(fundamental["rcept_no"].apply(lambda x: x[:8]))
        fundamental["reprt_year"] = fundamental["bsns_year"]
        fundamental = self.slice_columns(fundamental)
        #
        fundamental["thstrm_amount"] = fundamental["thstrm_amount"].apply(self.value2numeric)
        fundamental["frmtrm_amount"] = fundamental["frmtrm_amount"].apply(self.value2numeric)
        fundamental["bfefrmtrm_amount"] = fundamental["bfefrmtrm_amount"].apply(self.value2numeric)
        return fundamental

    @staticmethod
    def value2numeric(value: str) -> Optional[int]:
        if value == "-":
            return None
        return int(value.replace(",", ""))

    @staticmethod
    def slice_columns(df: pd.DataFrame) -> pd.DataFrame:
        using_columns = [
            "reprt_date",
            "reprt_code",
            "reprt_year",
            "stock_code",
            "fs_div",
            "account_nm",
            "thstrm_amount",
            "frmtrm_amount",
            "bfefrmtrm_amount",
        ]
        sliced_df = df.loc[:, using_columns]
        return sliced_df


class CorpPreProc:
    def __init__(self, corps: pd.DataFrame) -> None:
        self.corps = corps

    @staticmethod
    def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
        column_rename_dict = {"corp_name": "stock_nm"}
        renamed_df = df.rename(columns=column_rename_dict)
        return renamed_df

    @staticmethod
    def slice_columns(df: pd.DataFrame) -> pd.DataFrame:
        using_columns = ["stock_code", "stock_nm", "sector", "product"]
        sliced_df = df.loc[:, using_columns]
        return sliced_df

    def __call__(self) -> pd.DataFrame:
        corps = self.corps.copy()
        corps = self.rename_columns(corps)
        corps = self.slice_columns(corps)
        return corps
