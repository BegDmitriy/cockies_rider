import random
import time
from functions import *

def main():
    """
    Основная функция, которая управляет процессом чтения профилей и сайтов, перемешивает их в случайном порядке
    и для каждого профиля запускает браузер, посещает случайные сайты, а затем закрывает браузер.
    """
    # Файл с номерами профилей
    profile_file = 'data/profiles.txt'
    # Файл с популярными сайтами
    site_file = 'data/popular_sites.txt'

    # Чтение профилей из файла
    profiles = read_profiles(profile_file)
    # Чтение сайтов из файла
    sites = read_sites(site_file)

    # Перемешивание списка сайтов для случайного выбора
    random.shuffle(sites)
    # Перемешивание списка профилей для случайного порядка
    random.shuffle(profiles)

    # Проход по каждому профилю
    for profile_num in profiles:
        try:
            # Запуск профиля и получение драйвера браузера
            driver = start_profile(int(profile_num))
            # Посещение случайных сайтов
            visit_random_site(driver, sites)
        except Exception as e:
            # Обработка ошибок и вывод сообщения об ошибке
            print(f'Ошибка с профилем {profile_num}: {e}')
        finally:
            # Закрытие браузера
            close_browser(int(profile_num))

if __name__ == '__main__':
    # Запуск основной функции, если скрипт выполняется напрямую
    main()