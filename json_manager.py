import json
import os


class JsonManager:
    def __init__(self):
        self.folder_path = "data"                                   # папка с json-файлом
        self.file_path = f"{self.folder_path}/json_saved_paths"     # путь к json-файлом
        self.json = {                                               # дефолтный текст json-файла
                    "video_directory_path": "",
                    "result_directory_path": ""
        }

    def update_json(self, video_directory_path, result_directory_path):
        """Обновляет данные в json-файле"""
        self.json = {
            "video_directory_path": video_directory_path,
            "result_directory_path": result_directory_path
        }
        self.write_json()

    def write_json(self):
        """Сохраняет информацию в json-файле"""
        with open(self.file_path, "w", encoding='utf-8') as f:
            json.dump(self.json, f)

    def get_data(self):
        """Возвращает информацию о видео из json-файла"""
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
        try:
            with open(self.file_path, "r", encoding='utf-8') as f:
                data = json.load(f)
        except:
            with open(self.file_path, "w", encoding='utf-8') as f:
                json.dump(self.json, f)
            with open(self.file_path, "r", encoding='utf-8') as f:
                data = json.load(f)

        return data["video_directory_path"], data["result_directory_path"]
