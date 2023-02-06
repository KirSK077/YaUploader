from pprint import pprint
import requests
import os


class YaUploader:
    def __init__(self, token_filename, pc_folder_path, yd_folder_path):
        self.token_filename = token_filename
        self.pc_folder_path = pc_folder_path
        self.yd_folder_path = yd_folder_path
        self.file = file
        self.headers = {}

    def get_token(self):
        token_path = os.path.join(os.getcwd(), self.token_filename)
        with open(token_path, 'r', encoding='utf') as token_text:
            self.token = token_text.read()
            return self.token

    def get_headers(self):
        self.headers = {'Content-Type': 'application/json',
                        'Accept': 'application/json',
                        'Authorization': f'OAuth {self.get_token()}'}
        return self.headers

    def get_files_list(self):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
        resp_files = requests.get(url=url, headers=self.get_headers())
        return resp_files.json()

    def create_upload_folder(self):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/'
        param = {"path": self.yd_folder_path}
        upload_link = requests.put(url=url, params=param, headers=self.get_headers())
        if upload_link.status_code == 201:
            return f'Папка {self.yd_folder_path} успешно создана'

    def get_upload_link(self):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        param = {"path": f'{self.yd_folder_path}/{self.file}', "overwrite": "true"}
        upload_url = requests.get(url=url, params=param, headers=self.get_headers())
        return upload_url.json()

    def upload_file(self, file):
        path = self.get_upload_link().get('href')
        file_path = os.path.join(os.getcwd(), self.pc_folder_path, file)
        with open(file_path, 'rb') as f:
            response_up_file = requests.put(url=path, headers=self.get_headers(), data=f)
        if response_up_file.status_code == 201:
            return 'Файл успешно загружен'


if __name__ == '__main__':
    token = 'token.txt'
    pc_folder = 'Test_Folder'
    yd_folder = 'New_Folder_0'
    file = 'Pict.jpg'
    YaUploader(token, pc_folder, yd_folder).create_upload_folder()
    YaUploader(token, pc_folder, yd_folder).get_upload_link()
    pprint(YaUploader(token, pc_folder, yd_folder).upload_file(file))
