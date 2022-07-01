import pathlib
import pyzipper


def mkdir(mkdir_path='./zip_storage'):
    pathlib.Path(mkdir_path).mkdir(exist_ok=True)


def touch_file(dir_='zip_storage', file_name='file', extension='txt'):
    try:
        with open(f"./{dir_}/{file_name}.{extension}", "x") as f:
            f.write("x モードでファイルを作成しました。")
    except FileExistsError:
        print("ファイルが既に存在します。")


def compress_zip(pass_word=b'password', dir_zip='zip_storage', file_name='file'):
    with pyzipper.AESZipFile('archive_with_pass.zip', 'w',
                             encryption=pyzipper.WZ_AES) as zf:
        zf.setpassword(pass_word)

        zf.write(f'./{dir_zip}/{file_name}.txt', arcname=f'{file_name}.txt')
        zf.write(f'./{dir_zip}/{file_name}.xlsx', arcname=f'{file_name}.xlsx')


if __name__ == '__main__':
    mkdir()
    touch_file(extension='csv')
    compress_zip()
