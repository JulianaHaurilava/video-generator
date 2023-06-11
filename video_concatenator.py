import os
import ffmpeg
import random
import subprocess as sp
import tkinter as tk
from tkinter import ttk
from threading import Thread

from ffmpeg_progress_yield import FfmpegProgress


class VideoConcatenator:
    def __init__(self, first_video_path, second_video_path,
                 target_duration, bitrate, result_path, video_list):
        self.__video_width = 1920                           # требуемая ширина видео
        self.__video_height = 1080                          # требуемая высота видео
        self.__sar = '1/1'                                  # sar итогового видео

        self.video_list = video_list                        # список видео для генерации финального ролика
        self.first_video_path = first_video_path            # путь к первому видео для финального ролика
        self.second_video_path = second_video_path          # путь ко второму видео для финального ролика
        self.target_duration = target_duration              # требуемая длина финального видео
        self.bitrate = bitrate                              # битрейт
        self.result_path = result_path                      # путь к финальному видеоролику

        self.error_text = ""                                # резульат генерации ролика

        self.mts_files_path = "data/mts_files"
        self.all_videos_file_path = "data/temp_videos_file.txt"
        self.__init_status_bar()

    @staticmethod
    def __get_abs_path(path):
        return os.path.abspath(path)

    def __init_status_bar(self):
        """Инициализирует виджеты для отображения процесса создания видеоролика"""
        self.sb_root = tk.Tk()
        self.sb_root.title("Генерация видео")
        self.progress_bar = ttk.Progressbar(self.sb_root, length=300, mode="determinate")
        self.progress_bar.pack(pady=20)
        self.error_text = ""  # резульат генерации ролика
        self.progress_bar["maximum"] = 100

    def update_progress(self, progress):
        """Обновляет progress_bar для отображения прогресса генерации ролика"""
        self.progress_bar['value'] = progress
        self.sb_root.update_idletasks()

    @staticmethod
    def __get_video_duration(video_path):
        """Возвращает длительность видеоролика"""
        probe = ffmpeg.probe(video_path)
        duration = float(probe["format"]["duration"])
        return duration

    def create_concat_video_list(self):
        """Формирует список всех видео для финального ролика"""
        # присоединение первого ролика в список генерации
        concat_video_list = [self.first_video_path]
        duration = self.__get_video_duration(self.first_video_path)

        # присоединение второго ролика в список генерации если требуется
        if self.second_video_path:
            duration += self.__get_video_duration(self.second_video_path)
            concat_video_list.append(self.second_video_path)

        # присоединение роликов из списка в рандомном порядке до достижения требуемой длины
        while duration <= self.target_duration and self.video_list:
            video = random.choice(self.video_list)
            concat_video_list.append(video)
            self.video_list.remove(video)
            duration += self.__get_video_duration(video)
        return concat_video_list

    def create_video_file(self, concat_video_list):
        """Формирует файл с путями к видеороликам"""
        try:
            # попытка создания папки с видео в mts
            os.makedirs(self.mts_files_path)
        except FileExistsError:
            pass

        if os.path.isfile(self.all_videos_file_path):
            os.remove(self.all_videos_file_path)

        with open(self.all_videos_file_path, "w") as f:
            for video_path in concat_video_list:
                output_file = video_path

                # если файл не требуемого формата, в папке mts_files создается видео mts
                if not video_path.endswith(".mts"):
                    video_name = os.path.splitext(os.path.basename(video_path))[0]
                    output_file = '{}{}'.format(os.path.join(self.__get_abs_path(self.mts_files_path), video_name),
                                                '.mts')
                    if not os.path.isfile(output_file):
                        try:
                            sp.run(f'ffmpeg -i "{video_path}" -c:v libx264 "{output_file}"')
                        except Exception as e:
                            self.error_text = e
                f.write(f"file '{output_file}'\n")

    def create_command(self):
        """Генерирует команду для создания видеоролика"""
        result_command = f'ffmpeg -f concat -safe 0 -i {self.all_videos_file_path} -b:v {self.bitrate}k -s ' \
                         f'{self.__video_width}x{self.__video_height} -c:a copy {self.result_path}'
        return result_command

    def create_video(self):
        """Генерирует видеоролик по заданным параметрам"""
        concat_video_list = self.create_concat_video_list()
        self.create_video_file(concat_video_list)
        cmd = self.create_command()

        # генерация видеоролика
        ff = FfmpegProgress(cmd.split())

        def get_progress():
            """Получает информацию о статусе формирования видео в процентах"""
            try:
                for progress in ff.run_command_with_progress():
                    self.update_progress(int(progress))
            except Exception as e:
                self.error_text = e
            self.sb_root.destroy()
            self.sb_root.quit()

        # работа прогрессбара
        get_progress_to_bar = Thread(target=get_progress)
        get_progress_to_bar.start()

        self.sb_root.mainloop()

    def start_video_creation(self):
        """Генерирует видеоролик по заданным параметрам"""
        try:
            self.create_video()
        except ffmpeg.Error as e:
            self.error_text = e
        except Exception as e:
            self.error_text = e
        finally:
            os.remove(self.all_videos_file_path)
            return str(self.error_text).strip()
