import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import requests

def open_browser(profile_number: int):
    """
    Открывает браузер с указанным профилем через API.

    Args:
        profile_number (int): Номер профиля для открытия.

    Returns:
        dict | bool: JSON ответ с данными профиля, если запрос успешен. Иначе возвращает False.
    """
    params = {
        'serial_number': profile_number,
        'open_tabs': 1
    }

    response = requests.get('http://local.adspower.net:50325/api/v1/browser/start', params=params)
    if response.status_code == 200:
        return response.json()  # Возвращает JSON ответ с данными профиля
    else:
        return False  # Возвращает False в случае ошибки

def close_browser(profile_number: int):
    """
    Закрывает браузер с указанным профилем через API.

    Args:
        profile_number (int): Номер профиля для закрытия.

    Returns:
        bool: True если запрос успешен, иначе False.
    """
    params = {
        'serial_number': profile_number
    }
    response = requests.get('http://local.adspower.net:50325/api/v1/browser/stop', params=params)
    if response.status_code == 200:
        return True  # Возвращает True если запрос успешен
    else:
        return False  # Возвращает False в случае ошибки

def check_browser_status(profile_number: int):
    """
    Проверяет, активен ли браузер с указанным профилем через API.

    Args:
        profile_number (int): Номер профиля для проверки.

    Returns:
        bool: True если браузер активен, иначе False.
    """
    params = {
        'serial_number': profile_number
    }
    response = requests.get('http://local.adspower.net:50325/api/v1/browser/active', params=params)
    if response.status_code == 200:
        return True  # Возвращает True если браузер активен
    else:
        return False  # Возвращает False в случае ошибки

def start_profile(profile_number: int) -> webdriver.Chrome:
    """
    Запускает профиль и возвращает драйвер браузера.

    Args:
        profile_number (int): Номер профиля для запуска.

    Returns:
        webdriver.Chrome: Объект драйвера браузера.
    """
    profile_data = open_browser(profile_number)
    if profile_data:
        # Извлекает путь к драйверу и порт Selenium из данных профиля
        chrome_driver = profile_data['data']['webdriver']
        selenium_port = profile_data['data']['ws']['selenium']

        service = Service(executable_path=chrome_driver)

        options = Options()
        # Настраивает опции для подключения к удалённому браузеру
        options.add_experimental_option('debuggerAddress', selenium_port)

        driver = webdriver.Chrome(options=options, service=service)
        return driver  # Возвращает объект драйвера браузера

def read_profiles(file_path: str):
    """
    Читает файл с профилями и возвращает список профилей.

    Args:
        file_path (str): Путь к файлу с профилями.

    Returns:
        list: Список профилей.
    """
    with open(file_path, 'r') as f:
        profiles = f.read().splitlines()  # Читает строки файла и возвращает их в виде списка
    return profiles

def read_sites(file_path: str):
    """
    Читает файл с сайтами и возвращает список сайтов.

    Args:
        file_path (str): Путь к файлу с сайтами.

    Returns:
        list: Список сайтов.
    """
    with open(file_path, 'r') as f:
        sites = f.read().splitlines()  # Читает строки файла и возвращает их в виде списка
    return sites

def visit_random_site(driver, sites, num_sites=5):
    """
    Посещает случайные сайты из списка.

    Args:
        driver (webdriver.Chrome): Объект драйвера браузера.
        sites (list): Список сайтов для посещения.
        num_sites (int): Количество сайтов для посещения. По умолчанию 5.
    """
    random_sites = random.sample(sites, num_sites)  # Выбирает случайные сайты из списка
    for site in random_sites:
        driver.get(site)  # Переходит на сайт
        time.sleep(random.uniform(10, 15))  # Ждет случайное время от 10 до 15 секунд

