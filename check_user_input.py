import os


def validate_duration(duration_str):
    """Проверка введенной длительности итогового видеоролика"""
    if not duration_str:
        return "Поле длительности видео должно быть заполнено"
    try:
        duration = float(duration_str)
    except ValueError:
        return "Введенное значение длительности видео должно быть положительным числом"
    except OverflowError:
        return "Введенное значение длительности видео слишком большое"
    if duration <= 0:
        return "Введенное значение длительности видео должно быть положительным числом"
    return ""


def validate_new_file_name(result_name, directory):
    """Проверка введенного названия нового видео"""
    if not all(c.isalnum() or c in ['-', '_', ' ', '.'] for c in result_name) or result_name.count('.') > 1:
        return "Название нового видео указано некорректно"
    if os.path.isfile(os.path.join(directory, result_name.partition('.')[0] + ".mp4")):
        return "Видео с таким названием уже существует в указанной папке"
    return ""


def validate_video_directory_path(video_directory_path, video_list):
    """Проверка выбранного пути, где хранятся видео для ролика"""
    if not video_directory_path:
        return "Поле папки с исходными видео должно быть заполнено"
    elif not video_list:
        return "В указанной папке нет ни одного видеоролика"
    return ""
