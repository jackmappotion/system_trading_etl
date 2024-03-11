import os
import requests
import pandas as pd
from typing import List
import dart_fss


class DartFss:
    """
    dart-fss : external libaray
    - load corpinfo
    """
    def __init__(self, api_key: str) -> None:
        dart_fss.set_api_key(api_key)
        self.dart_fss = dart_fss

    def load_corps(self, only_public: bool = True) -> pd.DataFrame:
        corp_list = dart_fss.get_corp_list()
        corps = pd.DataFrame([corp.info for corp in corp_list])
        if only_public:
            corps = corps[~corps["stock_code"].isna()]
        return corps


class DartExtractor:
    """
    DartExtractor
    - load fundamentals
    """
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.base_url = "https://opendart.fss.or.kr/api"

    def load_fundamental(self, corp: str, year: str, reprt: str) -> pd.DataFrame:
        _url = self._format_url("fnlttSinglAcnt.json")
        _params = self._format_params(corp_code=corp, bsns_year=year, reprt_code=reprt)
        data = self._load_data(url=_url, params=_params)
        return data

    def _load_fundamentals(self, corps: str, year: str, reprt: str) -> pd.DataFrame:
        _url = self._format_url("fnlttMultiAcnt.json")
        _params = self._format_params(corp_code=corps, bsns_year=year, reprt_code=reprt)
        data = self._load_data(url=_url, params=_params)
        return data

    def load_fundamentals(self, corps: list, year: str, reprt: str) -> pd.DataFrame:
        fundamentals_list = list()
        corps_list = self._get_chunked_list(corps, 99)
        for corps in corps_list:
            str_corps = ",".join(corps)
            fundamentals = self._load_fundamentals(corps=str_corps, year=year, reprt=reprt)
            fundamentals_list.append(fundamentals)
        data = pd.concat(fundamentals_list, axis=0)
        return data

    def _load_data(self, url: str, params: dict) -> pd.DataFrame:
        try:
            resp = requests.get(url=url, params=params)
        except requests.exceptions.SSLError:
            print("SSL error occurred: might be a problem with the IP or SSL certification.")
            return pd.DataFrame()

        except requests.exceptions.HTTPError:
            print(
                "HTTP error occurred: might be a problem with the internet connection or the server."
            )
            return pd.DataFrame()
        try:
            resp_json = resp.json()
            if resp_json["status"] == "000":
                resp_df = pd.DataFrame(resp_json["list"])
                return resp_df
            else:
                return pd.DataFrame()
        except ValueError:
            print("Error decoding JSON from resp")
            return pd.DataFrame()

    def _format_url(self, theme: str) -> str:
        url = os.path.join(self.base_url, theme)
        return url

    def _format_params(self, **kwargs) -> dict:
        params = {**kwargs}
        params["crtfc_key"] = self.api_key
        return params

    @staticmethod
    def _get_chunked_list(_list: list, n: int) -> List[List]:
        return [_list[i : i + n] for i in range(0, len(_list), n)]
