import ffmpeg
import random
import threading
import tkinter as tk
from tkinter import ttk


class VideoConcatenator:
    def __init__(self, result_directory_path, first_video_path, second_video_path,
                 target_duration, bitrate, result_name, video_list):
        self.__video_width = 1920                               # требуемая ширина видео
        self.__video_height = 1080                              # требуемая высота видео
        self.__sar = '1/1'                                      # sar итогового видео
        
        self.video_list = video_list                            # список видео для генерации финального ролика
        self.result_directory_path = result_directory_path      # папка для финального видео
        self.first_video_path = first_video_path                # путь к первому видео для финального ролика
        self.second_video_path = second_video_path              # путь ко второму видео для финального ролика
        self.target_duration = target_duration                  # требуемая длина финального видео
        self.bitrate = bitrate                                  # битрейт   
        self.result_name = result_name                          # название финального видеоролика

        self.sb_root = None                                     # root для отображения прогресса генерации ролика
        self.progress_bar = None                                # progress bar для отображения прогресса генерации ролика

        self.video_creation_complete = False                    # флаг завершения генерации видеоролика
        self.error_text = ""                                    # резульат генерации ролика

        self.__init_status_bar()

    def __init_status_bar(self):
        """Инициализирует виджеты для отображения процесса создания видеоролика"""
        self.sb_root = tk.Tk()
        self.sb_root.title("Генерация видео")
        self.progress_bar = ttk.Progressbar(self.sb_root, length=300, mode="determinate")
        self.progress_bar.pack(pady=20)

    @staticmethod
    def __get_video_duration(video_path):
        """Возвращает длительность видеоролика"""
        probe = ffmpeg.probe(video_path)
        duration = float(probe["format"]["duration"])
        return duration

    def update_progress(self, progress):
        """Обновляет progress_bar для отображения прогресса генерации ролика"""
        self.progress_bar['value'] = progress
        self.sb_root.update_idletasks()

    def create_video(self):
        """Генерирует видеоролик по заданным параметрам"""
        self.error_text = ""
        try:
            # присоединение первого ролика в список генерации
            concat_video_list = [ffmpeg.input(self.first_video_path)]
            duration = self.__get_video_duration(self.first_video_path)
            pb_duration = 2

            # присоединение второго ролика в список генерации если требуется
            if self.second_video_path:
                duration += self.__get_video_duration(self.second_video_path)
                concat_video_list.append(ffmpeg.input(self.second_video_path))
                pb_duration += 1

            # присоединение роликов из списка в рандомном порядке до достижения требуемой длины
            while duration <= self.target_duration and self.video_list:
                video = random.choice(self.video_list)
                concat_video_list.append(ffmpeg.input(video))
                self.video_list.remove(video)
                duration += self.__get_video_duration(video)
                pb_duration += 1

            # установка максимального значения шкалы progress bar
            self.progress_bar["maximum"] = pb_duration

            scaled_videos = []  # список видео, соответствующих заданным условиям

            # подгон видеороликов под размер 1920х1080 и sar 1:1
            for index, video_input in enumerate(concat_video_list, start=1):
                scaled_stream = video_input.filter('scale', f'{self.__video_width}x{self.__video_height}')\
                    .filter('setsar', self.__sar)
                # ffmpeg.output(scaled_stream, output_file, b=f"{self.bitrate}k").run()
                scaled_videos.append(scaled_stream)
                self.update_progress(index)

            # генерация пути к финальному ролику
            output_file = self.result_directory_path + f'/{self.result_name}.mp4'

            # генерация ролика
            ffmpeg.concat(*scaled_videos).output(output_file, b=f"{self.bitrate}k").run()

            # завершение шкалы progress bar
            self.update_progress(pb_duration)

        except ffmpeg.Error as e:
            self.error_text = str(e)
        except Exception as e:
            self.error_text = str(e)
        finally:
            self.sb_root.destroy()
            self.video_creation_complete = True
            return

    def start_video_creation(self):
        """Генерирует видеоролик по заданным параметрам"""

        # создание нового потока для создания видео
        video_thread = threading.Thread(target=self.create_video)
        video_thread.start()

        def check_completion():
            """Отслеживает процесс завершения процесса генерации ролика"""
            while True:
                if self.video_creation_complete:
                    self.sb_root.quit()
                    break

        completion_thread = threading.Thread(target=check_completion)
        completion_thread.start()

        self.sb_root.mainloop()
        return self.error_text
