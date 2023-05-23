import ffmpeg
import random
import subprocess


class VideoConcatenator:
    def __init__(self, result_directory_path, first_video_path, second_video_path,
                 target_duration, bitrate, result_name, video_list) :
        self.__video_width = 1920  # требуемая ширина видео
        self.__video_height = 1080  # требуемая высота видео
        self.__sar = '1/1'  # sar итогового видео

        self.video_list = video_list  # список видео для генерации финального ролика
        self.result_directory_path = result_directory_path  # папка для финального видео
        self.first_video_path = first_video_path  # путь к первому видео для финального ролика
        self.second_video_path = second_video_path  # путь ко второму видео для финального ролика
        self.target_duration = target_duration  # требуемая длина финального видео
        self.bitrate = bitrate  # битрейт
        self.result_name = result_name  # название финального видеоролика

        self.error_text = ""  # резульат генерации ролика

    @staticmethod
    def __get_video_duration(video_path):
        """Возвращает длительность видеоролика"""
        probe = ffmpeg.probe(video_path)
        duration = float(probe["format"]["duration"])
        return duration

    def create_command(self, concat_video_list, output_file):
        video_input = ""
        video_streams = ""
        video_streams_es = ""
        n = len(concat_video_list)
        for i, video in enumerate(concat_video_list) :
            video_input += f"-i {video} "
            video_streams += f"[{i}:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:-1:-1,setsar=1,fps=30,format=yuv420p[v{i}];"
            video_streams_es += f"[v{i}][{i}:a]"
        result_command = f'ffmpeg {video_input} -filter_complex ' \
                         f'"{video_streams}{video_streams_es}concat=n={n}:v=1:a=1[v][a]" ' \
                         f'-map "[v]" -map "[a]" -c:v libx264 -b:v {self.bitrate}k -c:a aac -movflags +faststart {output_file}'
        return result_command

    def create_video(self):
        """Генерирует видеоролик по заданным параметрам"""
        self.error_text = ""
        try:
            # присоединение первого ролика в список генерации
            concat_video_list = [self.first_video_path]
            duration = self.__get_video_duration(self.first_video_path)
            pb_duration = 2

            # присоединение второго ролика в список генерации если требуется
            if self.second_video_path:
                duration += self.__get_video_duration(self.second_video_path)
                concat_video_list.append(self.second_video_path)
                pb_duration += 1

            # присоединение роликов из списка в рандомном порядке до достижения требуемой длины
            while duration <= self.target_duration and self.video_list:
                video = random.choice(self.video_list)
                concat_video_list.append(video)
                self.video_list.remove(video)
                duration += self.__get_video_duration(video)
                pb_duration += 1

            # генерация пути к финальному ролику
            output_file = self.result_directory_path + f'/{self.result_name}.mp4'

            filename = "data/tempfile.txt"
            with open(filename, 'w') as f:
                for video in concat_video_list :
                    print(f"file '{video}'", file=f)

            # генерация ролика
            subprocess.run(self.create_command(concat_video_list, output_file))

        except ffmpeg.Error as e:
            self.error_text = str(e)
        except Exception as e:
            self.error_text = str(e)
        finally:
            return

    def start_video_creation(self):
        """Генерирует видеоролик по заданным параметрам"""
        self.create_video()
        return self.error_text
