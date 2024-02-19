import os
import requests
import pandas as pd


class DartExtractor:
    def __init__(self, api_key) -> None:
        self.api_key = api_key
        self.base_url = "https://opendart.fss.or.kr/api"

    def load_fundamental(self, corp: str, year: str, reprt: str):
        _url = self._format_url("fnlttSinglAcnt.json")
        _params = self._format_params(corp_code=corp, bsns_year=year, reprt_code=reprt)
        data = self._load_data(url=_url, params=_params)
        return data

    def _load_fundamentals(self, corps: str, year: str, reprt: str):
        _url = self._format_url("fnlttMultiAcnt.json")
        _params = self._format_params(corp_code=corps, bsns_year=year, reprt_code=reprt)
        data = self._load_data(url=_url, params=_params)
        return data

    def load_fundamentals(self, corps: list, year: str, reprt: str):
        fundamentals_list = list()
        corps_list = self._get_chunked_list(corps, 99)
        for corps in corps_list:
            str_corps = ",".join(corps)
            fundamentals = self._load_fundamentals(corps=str_corps, year=year, reprt=reprt)
            fundamentals_list.append(fundamentals)
        data = pd.concat(fundamentals_list, axis=0)
        return data

    def _load_data(self, url, params):
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

    def _format_url(self, theme):
        url = os.path.join(self.base_url, theme)
        return url

    def _format_params(self, **kwargs):
        params = {**kwargs}
        params["crtfc_key"] = self.api_key
        return params

    @staticmethod
    def _get_chunked_list(_list, n):
        return [_list[i : i + n] for i in range(0, len(_list), n)]
