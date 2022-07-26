import glob
import os.path
import pathlib
import pyzipper

from models.client_service import ClientService
from config.log_conf import LogConf


class Zip(ClientService):

    def __init__(self, file_name='file', zip_dir='zip_storage', zip_name='sample.zip', zip_pass=None):
        """

        :param file_name(str): zip 圧縮するファイル名
        :param zip_dir(str): zip 圧縮する Directory Name
        :param zip_name(str): zip 圧縮名
        :param zip_pass(str): zip password
        """
        super().__init__()
        self.file_name = file_name
        self.zip_dir = zip_dir
        self.zip_name = zip_name
        self.zip_pass = zip_pass
        self.logger = LogConf().get_logger(__file__)

    def _mkdir(self):
        """ zip 扱う Directory 作成 """
        pathlib.Path(self.zip_dir).mkdir(exist_ok=True)

    def touch_file(self, extension='txt'):
        """ ファイル作成 """
        file_path = f"./{self.zip_dir}/{self.file_name}.{extension}"
        if os.path.isfile(file_path):
            self.logger.info({
                'msg': "ファイルが既に存在します。",
                'file_path': file_path,
            })
            return True

        try:
            with open(file_path, "x") as f:
                f.write("x モードでファイルを作成しました。")
            self.logger.info({
                'msg': "ファイルを作成しました",
                'file_path': file_path,
            })
        except FileExistsError as ex:
            self.logger.error({
                'ex': ex,
                'msg': 'ファイルが既に存在します。',
            })
            raise FileExistsError

    def compress_zip(self):
        """ zip 圧縮処理
        password は bytes 型変換

        """
        try:
            with pyzipper.AESZipFile(f'{self.zip_dir}/{self.zip_name}', 'w', encryption=pyzipper.WZ_AES) as zf:
                zip_pass = self.zip_pass.encode()
                zf.setpassword(zip_pass)

                # 圧縮対象ファイル参照し、zip化
                files = glob.glob(f"./{self.zip_dir}/*")
                for file in files:
                    file_name = file.split('/')[-1]
                    if '.zip' not in file_name:
                        zf.write(file, arcname=file_name)
                        self.logger.info({
                            'msg': '指定ファイルを圧縮しました',
                            'file_name': file_name,
                        })

        except Exception as ex:
            self.logger.error({
                'ex': ex,
                'msg': 'Error The zip compression process failed.',
            })
            raise Exception

    def run_zip_compress(self):
        """ 添付ファイル作成処理 """
        self._mkdir()
        self.touch_file(extension='txt')
        self.compress_zip()
