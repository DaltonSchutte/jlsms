"""
Retrives file update file from GDELT for processing
"""

import os
import datetime
import urllib
from typing import (Optional,
                    Union
                   )

from pandas import (read_csv,
                    DataFrame
                   )

import sys
sys.path.insert(0, '..')
from src import ROOT_DIR


###########
# CLASSES #
###########

class GDELT:
    def __init__(self):
        self.base_url = 'http://data.gdeltproject.org/gdeltv2'
        self.table2ext = {
            'events': 'export',
            'gkg': 'gkg',
            'mentions': 'mentions'
        }
        self.table2colfile = {
            'events': 'events2.csv',
            'gkg': 'gkg2.csv',
            'mentions': 'mentions.csv'
        }

    def get_latest(self, table: str='events'):
        latest_url = 'http://data.gdeltproject.org/gdeltv2/lastupdate.txt'
        response = urllib.request.urlopen(latest_url)
        # Trailing newline character is removed
        update_urls = response.read().split('\n')[:-1]
        # Grab only the last item (the url for the update)
        update_urls = [u.split(' ')[-1] for u in update_urls]

        target_url = [u for u in update_urls if self.table2ext[table] in u][0]

        column_info = self._get_column_info(table)
        headers = self._get_column_headers(column_info)

        data = read_csv(
            target_url,
            sep='\t',
            header=None,
            names=headers,
            index_col=None,
            low_memory=False
        )
        return data


    def search(
        self,
        date: Optional[str, datetime.datetime, datetime.date]=None,
        table: str='events',
        coverage: bool=True
    ):
        column_info = self._get_column_info(table)
        headers = self._get_column_headers(column_info)

        raise NotImplementedError("WIP")

    def _get_column_info(self, table: str):
        path = os.path.join(ROOT_DIR, 'resources', 'gdelt_columns', table)
        column_info = read_csv(
            path,
            index_col='name',
            header=0,
            low_memory=False
        )
        return column_info

    def _get_column_headers(self, column_info: DataFrame):
        return column_info.index.values.tolist()

    def _make_url(self, date: datetime.datetime):
        raise NotImplementedError("WIP")

    def _format_date(
        self,
        date: Union[str, datetime.datetime, datetime.date]
    ):
        if isinstance(date, str):
            date = datetime.datetime.fromisoformat(date)

        # Modify minute
        minute = date.minute
        minute += (15 - (t%15))

        # Make date formatted for GDELT URL YYYYMMDDHHmmSS
        date = date.astimezone(datetime.timezone.utc)
        str_format = f"%Y%m%d%H{minute}00"

        date_str = date.strftime(str_format)

        return date_str
