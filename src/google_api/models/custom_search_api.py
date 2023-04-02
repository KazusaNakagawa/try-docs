import os
import datetime
import json

from googleapiclient.discovery import build

from config.log_conf import LogConf

GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
CUSTOM_SEARCH_ENGINE_ID = os.environ["CUSTOM_SEARCH_ENGINE_ID"]
DATA_DIR = 'data'


class CustomSearchApi(object):

    def __init__(self):
        super().__init__()
        self.logger = LogConf().get_logger(__file__)

    def mkdir(self, path):
        if not os.path.isdir(path):
            os.mkdir(path)

    def get_search_response(self, keyword):
        self.logger.info({'msg': 'Start', 'func': __name__})
        today = datetime.datetime.today().strftime("%Y%m%d")
        timestamp = datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S")

        self.mkdir(DATA_DIR)

        service = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)
        self.logger.info({'service': service})
        page_limit = 2
        start_index = 1

        response = []
        for n_page in range(0, page_limit):
            # res = service.cse().list(q=keyword, cx=CUSTOM_SEARCH_ENGINE_ID).execute()
            # return res['items']
            response.append(service.cse().list(
                q=keyword,
                cx=CUSTOM_SEARCH_ENGINE_ID,
                lr='lang_ja',
            ).execute())

        # レスポンスをjson形式で保存
        save_response_dir = os.path.join(DATA_DIR, 'response')
        self.mkdir(save_response_dir)

        out = {'snapshot_ymd': today, 'snapshot_timestamp': timestamp, 'response': response}
        jsonstr = json.dumps(out, ensure_ascii=False)
        with open(os.path.join(save_response_dir, 'response_' + today + '.json'), mode='w') as response_file:
            response_file.write(jsonstr)
