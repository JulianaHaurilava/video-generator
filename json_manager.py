import json


class JsonManager:
    def __init__(self):
        self.file_name = "json_saved_paths"
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
        try:
            with open(self.file_name, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            with open(self.file_name, "w") as f:
                json.dump({}, f)
            with open(self.file_name, "r") as f:
                data = json.load(f)
        return data["video_directory_path"], data["result_directory_path"]
