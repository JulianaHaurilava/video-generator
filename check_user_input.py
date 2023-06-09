import os


def validate_bitrate(bitarate_str):
    """Проверка введенного битрейта итогового видеоролика"""
    if not bitarate_str:
        return "Поле битрейта должно быть заполнено"
    try:
        bitrate = int(bitarate_str)
    except ValueError:
        return "Введенное значение битрейта должно быть положительным числом"
    except OverflowError:
        return "Введенное значение битрейта слишком большое"
    if not 300 <= bitrate <= 10000:
        return "Введенное значение битрейта не лежит в диапазоне от 300 до 10000"
    return ""


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
    if not all(c.isalnum() or c in ['-', '_', '.', ' '] for c in result_name) or result_name.count('.') > 1:
        return "Название нового видео указано некорректно"
    if os.path.isfile(os.path.join(directory, result_name.partition('.')[0] + ".mts")):
        return "Видео с таким названием уже существует в указанной папке"
    return ""


def validate_result_directory_path(result_directory_path):
    """Проверка выбранного пути, для сохранения финального ролика"""
    if not os.path.exists(result_directory_path):
        return "Папка для сохранения финального ролика не найдена по введенному пути"
    if not result_directory_path:
        return "Поле папки для финального видеоролика должно быть заполнено"
    return ""


def validate_video_directory_path(video_directory_path, video_list):
    """Проверка выбранного пути, где хранятся видео для ролика"""
    if not os.path.exists(video_directory_path):
        return "Папка с видеороликами не найдена по введенному пути"
    if not video_directory_path:
        return "Поле папки с исходными видео должно быть заполнено"
    return ""
