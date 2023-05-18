import json
import os


class JsonManager:
    def __init__(self):
        self.folder_path = "data"
        self.file_name = "data/json_saved_paths"
        self.json = {}

    def update_json(self, video_directory_path, result_directory_path):
        self.json = {
            "video_directory_path": video_directory_path,
            "result_directory_path": result_directory_path
        }
        self.write_json()

    def write_json(self):
        with open(self.file_name, "w") as f:
            json.dump(self.json, f)

    def get_data(self):
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
        try:
            with open(self.file_name, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            with open(self.file_name, "w") as f:
                json.dump({
                    "video_directory_path": "",
                    "result_directory_path": ""
                }, f)
            with open(self.file_name, "r") as f:
                data = json.load(f)
        return data["video_directory_path"], data["result_directory_path"]
