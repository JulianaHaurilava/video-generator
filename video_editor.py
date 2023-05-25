import os
import tkinter as tk
from tkinter import filedialog, X, LEFT, messagebox as mb, DISABLED, NORMAL
import check_user_input as check
import json_manager as jm
import video_concatenator as vc

# расширения видеофайлов
VIDEO_EXTENSIONS = ('.mp4', '.avi', '.mov', '.mkv')
# расширения видеофайлов для выбора видеороликов пользователем
VIDEO_FORMATS = (("MP4 files", "*.MP4"), ("MOV files", "*.MOV"), ("AVI files", "*.avi"), ("MKV files", "*mkv"))


class Model:
    def __init__(self):
        self.video_generator = None
        self.video_directory_path = ""      # папка с исходными видео
        self.result_directory_path = ""     # папка для финального видео
        self.first_video_path = ""          # путь к первому видео для финального ролика
        self.second_video_path = ""         # путь ко второму видео для финального ролика
        self.target_duration = 0            # требуемая длина финального видео
        self.bitrate = 0                    # битрейт
        self.result_name = ""               # название финального видеоролика
        self.video_list = []                # список видео без первого и второго для создания финального ролика

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

    def set_bitrate(self, bitrate):
        self.bitrate = int(bitrate)

    def get_video_directory_path(self):
        return self.video_directory_path

    def get_result_path(self):
        return f"{self.result_directory_path}/{self.result_name}.mp4"

    def get_all_videos_from_dir(self):
        """Получает список роликов для создания финального видео"""
        if self.video_directory_path:
            for video in os.listdir(self.video_directory_path):
                video_path = f'{self.video_directory_path}/{video}'
                if video.lower().endswith(VIDEO_EXTENSIONS) \
                        and video_path != self.first_video_path \
                        and video_path != self.second_video_path:
                    self.video_list.append(video_path)

    def try_create_video(self):
        """Запускает процесс генерации видео"""
        self.video_generator = vc.VideoConcatenator(self.result_directory_path, self.first_video_path,
                                                    self.second_video_path, self.target_duration, self.bitrate,
                                                    self.result_name, self.video_list)
        return self.video_generator.start_video_creation()


class View:
    def on_closing(self):
        """Обновление json-файла при завершении программы"""
        self.controller.save_json(bool(self.save_videos_path.get()), self.save_result_path.get())
        self.root.destroy()

    def __init__(self, controller):
        self.controller = controller

        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.root.title('Генератор видеороликов')
        self.root.geometry("560x250")
        self.root.minsize(590, 290)
        self.root.maxsize(590, 290)

        self.__init_video_folder_ui()
        self.__init_result_folder_ui()
        self.__init_first_video_path_ui()
        self.__init_second_video_path_ui()
        self.__init_duration_ui()
        self.__init_bitrate_ui()
        self.__init_result_name_ui()
        self.__init_create_video_button_ui()

    def __init_video_folder_ui(self):
        """Инициализирует виджеты для выбора и отображения папки с исходными видео"""
        self.save_videos_path = tk.IntVar()

        self.all_videos_frame = tk.Frame(self.root)
        self.all_videos_frame.pack(fill=X)

        self.videos_folder_label = tk.Label(self.all_videos_frame, width=27, text="Папка с исходными видео:",
                                            anchor="w")
        self.videos_folder_entry = tk.Entry(self.all_videos_frame, width=50, state="readonly")
        self.all_videos_folder_button = tk.Button(self.all_videos_frame, text="...",
                                                  command=self.update_video_directory_path)
        self.save_videos_path_ch = tk.Checkbutton(self.all_videos_frame, variable=self.save_videos_path)

        self.videos_folder_label.pack(side=LEFT, padx=5, pady=5)
        self.save_videos_path_ch.pack(side=LEFT, padx=5)
        self.videos_folder_entry.pack(side=LEFT, fill=X, expand=True)
        self.all_videos_folder_button.pack(padx=5)

    def __init_result_folder_ui(self):
        """Инициализирует виджеты для выбора и отображения папки для финального видео"""
        self.save_result_path = tk.IntVar()

        self.result_video_frame = tk.Frame(self.root)
        self.result_video_frame.pack(fill=X)

        self.result_folder_label = tk.Label(self.result_video_frame, width=27, text="Папка для итогового видео:",
                                            anchor="w")
        self.result_folder_entry = tk.Entry(self.result_video_frame, width=50, state="readonly")
        self.result_folder_button = tk.Button(self.result_video_frame, text="...",
                                              command=self.update_result_directory_path)
        self.result_videos_path_ch = tk.Checkbutton(self.result_video_frame, variable=self.save_result_path)

        self.result_folder_label.pack(side=LEFT, padx=5, pady=5)
        self.result_videos_path_ch.pack(side=LEFT, padx=5)
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

    def __init_bitrate_ui(self):
        """Инициализирует виджеты для ввода битрейта финального видеоролика"""
        self.bitrate_frame = tk.Frame(self.root)
        self.bitrate_frame.pack(fill=tk.X)

        self.bitrate_label = tk.Label(self.bitrate_frame, width=26, text="Битрейт:", anchor="w")
        self.bitrate_scale = tk.Scale(self.bitrate_frame, from_=16, to=512, orient=tk.HORIZONTAL)

        self.bitrate_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.bitrate_scale.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=X)

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

    def get_bitrate(self):
        return self.bitrate_scale.get()

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

    def set_save_videos_path_ch_true(self):
        self.save_videos_path.set(1)

    def set_save_result_path_ch_true(self):
        self.save_result_path.set(1)

    def create_video_click(self):
        self.controller.create_video()

    def show_success_window(self):
        """Выводит сообщение об успешном создании видеоролика"""
        mb.showinfo("Успех!", "Видео создано")

    def show_error_window(self, error_text):
        """Выводит сообщение о том, что видеоролик не создан и текст ошибки"""
        mb.showerror("Ошибка!", error_text)

    def show_warning_window(self, error_text):
        """Выводит предупреждение о том, что видеоролик мог быть сгенерирован с ошибками"""
        mb.showwarning("Предупреждение!", error_text)

    def disable_create_video_button(self):
        self.create_video_button.config(state=DISABLED)

    def enable_create_video_button(self):
        self.create_video_button.config(state=NORMAL)


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View(self)
        self.json_manager = jm.JsonManager()
        self.get_saved_paths()

    def run(self):
        self.view.root.mainloop()

    def get_saved_paths(self):
        video_directory_path, result_directory_path = self.json_manager.get_data()

        # отображает сохраненные директории и чекбоксы на экране
        self.show_saved_video_directory_path(video_directory_path)
        self.show_saved_result_directory_path(result_directory_path)

        # устанавливает значение директориям в Модели
        self.model.set_video_directory_path(video_directory_path)
        self.model.set_result_directory_path(result_directory_path)

    def save_json(self, save_videos_path, save_result_path):
        """Сохраняет json с данными о сохраненных директориях"""
        video_directory_path = self.model.video_directory_path
        result_directory_path = self.model.result_directory_path
        if not save_videos_path:
            video_directory_path = ""
        if not save_result_path:
            result_directory_path = ""

        self.json_manager.update_json(video_directory_path, result_directory_path)

    def check_input_is_valid(self):
        """Проверяет все введенные пользователем данные"""
        self.model.get_all_videos_from_dir()
        duration_error_text = check.validate_duration(self.view.get_duration())
        name_error_text = check.validate_new_file_name(self.view.get_result_name(),
                                                       self.model.result_directory_path)
        all_videos_error_text = check.validate_video_directory_path(self.model.video_directory_path,
                                                                    self.model.video_list)
        result_directory_error_text = check.validate_result_directory_path(self.model.result_directory_path)

        if all_videos_error_text:
            mb.showerror("Ошибка!", all_videos_error_text)
            return False

        if result_directory_error_text:
            mb.showerror("Ошибка!", result_directory_error_text)
            return False

        if not self.model.first_video_path:
            mb.showerror("Ошибка!", "Поле первого видео должно быть заполнено")
            return False
        elif not os.path.exists(self.model.first_video_path):
            mb.showerror("Ошибка!", "Первое видео не найдено по указанному пути")
            return False

        if self.model.second_video_path and not os.path.exists(self.model.second_video_path):
            mb.showerror("Ошибка!", "Второе видео не найдено по указанному пути")
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
        self.set_bitrate((self.view.get_bitrate()))

        return True

    def set_duration(self, duration):
        self.model.set_duration(duration)

    def set_result_name(self, result_name):
        self.model.set_result_name(result_name)

    def set_bitrate(self, bitrate):
        self.model.set_bitrate(bitrate)

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

    def show_saved_video_directory_path(self, path):
        if path:
            self.view.show_all_videos_path(path)
            self.view.set_save_videos_path_ch_true()

    def show_saved_result_directory_path(self, path):
        if path:
            self.view.show_result_video_path(path)
            self.view.set_save_result_path_ch_true()

    def create_video(self):
        """Генерирует видео и информирует пользователя о результате"""
        if self.check_input_is_valid():
            self.view.disable_create_video_button()
            error_text = self.model.try_create_video()
            video_path = self.model.get_result_path()
            if not os.path.exists(video_path):
                if error_text:
                    error_text = f"{error_text}\n" \
                                 "Видео не было создано."
                    self.view.show_error_window(error_text)
                else:
                    error_text = "Видео не было создано."
                    self.view.show_error_window(error_text)
            else:
                if error_text:
                    error_text = f"{error_text}\n" \
                                "Видео могло сгенерироваться некорректно."
                    self.view.show_warning_window(error_text)
                else:
                    self.view.show_success_window()
            self.view.enable_create_video_button()


if __name__ == "__main__":
    app = Controller()
    app.run()
