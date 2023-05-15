import os
import random
import tkinter as tk
from tkinter import filedialog, X, LEFT, messagebox as mb
import ffmpeg
import check_user_input as check

# расширения видеофайлов
VIDEO_EXTENSIONS = ('.mp4', '.avi', '.MOV', '.mkv')
# расширения видеофайлов для выбора видеороликов пользователем
VIDEO_FORMATS = (("MP4 files", "*.mp4"), ("MOV files", "*.MOV"), ("AVI files", "*.avi"), ("MKV files", "*mkv"))


class Model:
    def __init__(self):
        self.video_directory_path = ""      # папка с исходными видео
        self.result_directory_path = ""     # папка для финального видео
        self.first_video_path = ""          # путь к первому видео для финального ролика
        self.second_video_path = ""         # путь ко второму видео для финального ролика
        self.target_duration = 0            # требуемая длина финального видео
        self.result_name = ""               # название финального видеоролика
        self.video_list = []                # список видео для формирования финального ролика

    @staticmethod
    def __get_video_duration(video_path):
        """Возвращает длительность видеоролика"""
        probe = ffmpeg.probe(video_path)
        duration = float(probe["format"]["duration"])
        return duration

    def get_all_videos_from_dir(self):
        """Получает список роликов для создания финального видео"""
        if self.video_directory_path:
            for video in os.listdir(self.video_directory_path):
                video_path = f'{self.video_directory_path}/{video}'
                if video.endswith(VIDEO_EXTENSIONS) \
                        and video_path != self.first_video_path \
                        and video_path != self.second_video_path:
                    self.video_list.append(video_path)

    def set_video_directory_path(self, video_directory_path):
        self.video_directory_path = video_directory_path

    def set_result_directory_path(self, result_directory_path):
        self.result_directory_path = result_directory_path

    def set_first_video_path(self, first_video_path):
        self.first_video_path = first_video_path

    def set_second_video_path(self, second_video_path):
        self.second_video_path = second_video_path

    def set_duration(self, duration):
        self.target_duration = float(duration)

    def set_result_name(self, result_name):
        self.result_name = result_name

    def create_video(self):
        """Генерирует видеоролик по заданным параметрам"""

        # присоединение первого видео к финальному ролику
        concat_video_list = [ffmpeg.input(self.first_video_path)]
        duration = self.__get_video_duration(self.first_video_path)

        # присоединение второго видео к финальному ролику, если к нему указан путь
        if self.second_video_path:
            duration += self.__get_video_duration(self.second_video_path)
            concat_video_list.append(ffmpeg.input(self.second_video_path))

        # присоединение видео из списка до достижения требуемой длины финального ролика
        while duration <= self.target_duration and self.video_list:
            video = random.choice(self.video_list)
            concat_video_list.append(ffmpeg.input(video))
            self.video_list.remove(video)
            duration += self.__get_video_duration(video)

        # склейка финального видеоролика и сохранение его в указанной папке
        output_file = self.result_directory_path + f'/{self.result_name}.mp4'
        ffmpeg.concat(*concat_video_list).output(output_file, video_size='1920x1080').run()


class View:

    def __init__(self, controller):
        self.controller = controller

        self.root = tk.Tk()
        self.root.title('Генератор видеороликов')
        self.root.geometry("560x250")
        self.root.minsize(560, 250)
        self.root.maxsize(560, 250)

        self.__init_video_folder_ui()
        self.__init_result_folder_ui()
        self.__init_first_video_path_ui()
        self.__init_second_video_path_ui()
        self.__init_duration_ui()
        self.__init_result_name_ui()
        self.__init_create_video_button_ui()

    def __init_video_folder_ui(self):
        """Инициализирует виджеты для выбора и отображения папки с исходными видео"""
        self.all_videos_frame = tk.Frame(self.root)
        self.all_videos_frame.pack(fill=X)

        self.videos_folder_label = tk.Label(self.all_videos_frame, width=27, text="Папка с исходными видео:",
                                            anchor="w")
        self.videos_folder_entry = tk.Entry(self.all_videos_frame, width=50, state="readonly")
        self.all_videos_folder_button = tk.Button(self.all_videos_frame, text="...",
                                                  command=self.update_video_directory_path)
        self.videos_folder_label.pack(side=LEFT, padx=5, pady=5)
        self.videos_folder_entry.pack(side=LEFT, fill=X, expand=True)
        self.all_videos_folder_button.pack(padx=5)

    def __init_result_folder_ui(self):
        """Инициализирует виджеты для выбора и отображения папки для финального видео"""
        self.result_video_frame = tk.Frame(self.root)
        self.result_video_frame.pack(fill=X)

        self.result_folder_label = tk.Label(self.result_video_frame, width=27, text="Папка для итогового видео:",
                                            anchor="w")
        self.result_folder_entry = tk.Entry(self.result_video_frame, width=50, state="readonly")
        self.result_folder_button = tk.Button(self.result_video_frame, text="...",
                                              command=self.update_result_directory_path)
        self.result_folder_label.pack(side=LEFT, padx=5, pady=5)
        self.result_folder_entry.pack(side=LEFT, fill=X, expand=True)
        self.result_folder_button.pack(side=LEFT, padx=5)

    def __init_first_video_path_ui(self):
        """Инициализирует виджеты для выбора и отображения пути к первому видео"""
        self.first_video_frame = tk.Frame(self.root)
        self.first_video_frame.pack(fill=X)

        self.first_video_path_label = tk.Label(self.first_video_frame, width=27, text="Первое видео:", anchor="w")
        self.first_video_path_entry = tk.Entry(self.first_video_frame, width=50, state="readonly")
        self.first_video_choice_button = tk.Button(self.first_video_frame, text="...",
                                                   command=self.update_first_video_path)
        self.first_video_path_label.pack(side=LEFT, padx=5, pady=5)
        self.first_video_path_entry.pack(side=LEFT, fill=X, expand=True)
        self.first_video_choice_button.pack(side=LEFT, padx=5)

    def __init_second_video_path_ui(self):
        """Инициализирует виджеты для выбора и отображения пути ко второму видео"""
        self.second_video_frame = tk.Frame(self.root)
        self.second_video_frame.pack(fill=X)

        self.second_video_path_label = tk.Label(self.second_video_frame, width=27,
                                                text="Второе видео:", anchor="w")
        self.second_video_path_entry = tk.Entry(self.second_video_frame, width=50, state="readonly")
        self.second_video_choice_button = tk.Button(self.second_video_frame, text="...",
                                                    command=self.update_second_video_path)
        self.second_video_path_label.pack(side=LEFT, padx=5, pady=5)
        self.second_video_path_entry.pack(side=LEFT, fill=X, expand=True)
        self.second_video_choice_button.pack(side=LEFT, padx=5)

    def __init_duration_ui(self):
        """Инициализирует виджеты для ввода длительности финального видеоролика"""
        self.duration_frame = tk.Frame(self.root)
        self.duration_frame.pack(fill=X)

        self.duration_label = tk.Label(self.duration_frame, width=27, text="Длительность итогового видео:", anchor="w")
        self.duration_entry = tk.Entry(self.duration_frame, width=5)
        self.second_label = tk.Label(self.duration_frame, text="c", anchor="w")

        self.duration_label.pack(side=LEFT, padx=5, pady=5)
        self.duration_entry.pack(side=LEFT)
        self.second_label.pack(side=LEFT, padx=5, pady=5)

    def __init_result_name_ui(self):
        """Инициализирует виджеты для ввода названия финального видеоролика"""
        self.result_name_frame = tk.Frame(self.root)
        self.result_name_frame.pack(fill=X)

        self.result_name_label = tk.Label(self.result_name_frame, width=27,
                                          text="Название итогового видео:", anchor="w")
        self.result_name_entry = tk.Entry(self.result_name_frame, width=30)

        self.result_name_label.pack(side=LEFT, padx=5, pady=5)
        self.result_name_entry.pack(side=LEFT)

    def __init_create_video_button_ui(self):
        """Инициализирует кнопку для создания видеоролика"""
        self.create_video_button = tk.Button(self.root, text="Сгенерировать видеоролик",
                                             command=self.create_video_click)
        self.create_video_button.pack(expand=1)

    def update_video_directory_path(self):
        """Получает директорию с исходными видео"""
        path = filedialog.askdirectory(initialdir='C:/',
                                       title="Выберите папку с видеороликами",
                                       mustexist=True)
        self.controller.set_video_directory_path(path)

    def update_result_directory_path(self):
        """Получает директорию для сохранения финального видео"""
        path = filedialog.askdirectory(initialdir='C:/',
                                       title="Выберите папку, в которой сохранится результат",
                                       mustexist=True)
        self.controller.set_result_directory_path(path)

    def update_first_video_path(self):
        """Получает путь к первому видео для финального ролика"""
        path = filedialog.askopenfilename(initialdir=self.videos_folder_entry.get(),
                                          title="Выберите первый видеоролик",
                                          filetypes=VIDEO_FORMATS)
        self.controller.set_first_video_path(path)

    def update_second_video_path(self):
        """Получает путь ко второму видео для финального ролика"""
        path = filedialog.askopenfilename(initialdir=self.videos_folder_entry.get(),
                                          title="Выберите второй видеоролик",
                                          filetypes=VIDEO_FORMATS)
        self.controller.set_second_video_path(path)

    def get_duration(self):
        return self.duration_entry.get()

    def get_result_name(self):
        return self.result_name_entry.get()

    def show_all_videos_path(self, all_videos_path):
        """Отображает путь к выбранной папке с исходными видео"""
        self.videos_folder_entry.config(state='normal')
        self.videos_folder_entry.delete(0, 'end')
        self.videos_folder_entry.insert(0, all_videos_path)
        self.videos_folder_entry.config(state='readonly')

    def show_result_video_path(self, result_video_path):
        """Отображает путь к выбранной папке для финального видео"""
        self.result_folder_entry.config(state='normal')
        self.result_folder_entry.delete(0, 'end')
        self.result_folder_entry.insert(0, result_video_path)
        self.result_folder_entry.config(state='readonly')

    def show_first_video_path(self, first_video_path):
        """Отображает путь к первому видео для финального ролика"""
        self.first_video_path_entry.config(state='normal')
        self.first_video_path_entry.delete(0, 'end')
        self.first_video_path_entry.insert(0, first_video_path)
        self.first_video_path_entry.config(state='readonly')

    def show_second_video_path(self, second_video_path):
        """Отображает путь ко второму видео для финального ролика"""
        self.second_video_path_entry.config(state='normal')
        self.second_video_path_entry.delete(0, 'end')
        self.second_video_path_entry.insert(0, second_video_path)
        self.second_video_path_entry.config(state='readonly')

    def create_video_click(self):
        self.controller.create_video()

    def show_success_window(self):
        mb.showinfo("Успех!", "Видео создано")

    def show_error_window(self):
        mb.showinfo("Ошибка!", "Видео не было создано")


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View(self)

    def run(self):
        self.view.root.mainloop()

    def check_input_is_valid(self):
        """Проверяет все введенные пользователем данные"""
        self.model.get_all_videos_from_dir()
        duration_error_text = check.validate_duration(self.view.get_duration())
        name_error_text = check.validate_new_file_name(self.view.get_result_name(),
                                                       self.model.result_directory_path)
        all_videos_error_text = check.validate_video_directory_path(self.model.video_directory_path,
                                                                    self.model.video_list)

        if all_videos_error_text:
            mb.showerror("Ошибка!", all_videos_error_text)
            return False

        if not self.model.result_directory_path:
            mb.showerror("Ошибка!", "Поле папки для финального видеоролика должно быть заполнено")
            return False

        if not self.model.first_video_path:
            mb.showerror("Ошибка!", "Поле первого видео должно быть заполнено")
            return False

        if duration_error_text:
            mb.showerror("Ошибка!", duration_error_text)
            return False

        if name_error_text:
            mb.showerror("Ошибка!", name_error_text)
            return False

        # инициализация переменных в Model
        self.set_duration(self.view.get_duration())
        self.set_result_name(self.view.get_result_name())

        return True

    def set_duration(self, duration):
        self.model.set_duration(duration)

    def set_result_name(self, result_name):
        self.model.set_result_name(result_name)

    def set_video_directory_path(self, path):
        self.model.set_video_directory_path(path)
        self.view.show_all_videos_path(path)

    def set_result_directory_path(self, path):
        self.model.set_result_directory_path(path)
        self.view.show_result_video_path(path)

    def set_first_video_path(self, path):
        self.model.set_first_video_path(path)
        self.view.show_first_video_path(path)

    def set_second_video_path(self, path):
        self.model.set_second_video_path(path)
        self.view.show_second_video_path(path)

    def create_video(self):
        if self.check_input_is_valid():
            try:
                self.model.create_video()
                self.view.show_success_window()
            except:
                self.view.show_error_window()


if __name__ == "__main__":
    app = Controller()
    app.run()
