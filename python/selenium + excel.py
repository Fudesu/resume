# Программа скачивает с ресурса БФО отчёт по введённому ИНН и проводит необходимый расчёт параметров на основе полученных данных, 
# которые записывает в итоговый .xlsx файл.

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import zipfile
import os
import pandas as pd
import warnings
from pathlib import Path

warnings.filterwarnings(action='ignore', message='.*future.*')
warnings.filterwarnings(action='ignore', message='.*default.*')

def excel(file):

    path = file
    df = pd.DataFrame()
    df1 = pd.DataFrame()
    try:
        df = pd.read_excel(f"{path}", sheet_name=2)
        df1 = pd.read_excel(f"{path}", sheet_name=1)
        # Коды необходимых параметров для расчёта
        cells = ('2110', '2400', '2100', '2120', '2210', '2220', '2330', '2350', '2410', '1200', '1250', '1300', '1500', '1600')

        df = df[df.apply(lambda row: row.str.startswith(cells).any(), axis=1)]
        df = df.dropna(axis=1, how='all').iloc[:, -4:].set_axis(['1', '2', '3', '4'], axis=1)
        df1 = df1[df1.apply(lambda row: row.str.startswith(cells).any(), axis=1)]
        df1 = df1.dropna(axis=1, how='all').iloc[:, -5:].set_axis(['1', '2', '3', '4', '5'], axis=1)
    except:
        print('Файл не найден. Что-то пошло не так.')


    symbols = [' ', '(', ')']
    columns = ['3', '4']
    columns1 = ['3', '4' , '5']

    # Удаление лишних символов
    for symbol in symbols:
        for column in columns:
            df[column] = df[column].apply(lambda x: x.replace(symbol, ''))
    for symbol in symbols:
        for column in columns1:
            df1[column] = df1[column].apply(lambda x: x.replace(symbol, ''))
    # Рассчёт необходимых показателей
    try:
        return_on_sales = str(round((float(df.loc[df['2'] == '2400']['3']) / float(df.loc[df['2'] == '2110']['3']) * 100), 3)) + '%'
    except:
        return_on_sales = 'Недостаточно данных для расчёта'
    try:
        gross_margin = str(round((float(df.loc[df['2'] == '2100']['3']) / float(df.loc[df['2'] == '2110']['3']) * 100), 3)) + '%'
    except:
        gross_margin = 'Недостаточно данных для расчёта'
    try:
        cost_effectiveness = str(round((float(df.loc[df['2'] == '2400']['3'] / 
                                              (float(df.loc[df['2'] == '2120']['3'] + float(df.loc[df['2'] == '2210']['3'])) + 
                                               float(df.loc[df['2'] == '2220']['3']) + 
                                               float(df.loc[df['2'] == '2330']['3']) + 
                                               float(df.loc[df['2'] == '2350']['3']) + 
                                               float(df.loc[df['2'] == '2410']['3']))) * 100), 3)) + '%'
    except:
        cost_effectiveness = 'Недостаточно данных для расчёта'
    try:
        return_on_capital = str(
            round((float(df.loc[df['2'] == '2100']['3']) / float(df1.loc[df1['2'] == '1300']['3']) * 100), 3)) + '%'
    except:
        return_on_capital = 'Недостаточно данных для расчёта'
    try:
        current_liquidity_ratio = str(
            round((float(df1.loc[df1['2'] == '1200']['3']) / float(df1.loc[df1['2'] == '1500']['3'])), 3))
    except:
        current_liquidity_ratio = 'Недостаточно данных для расчёта'
    try:
        absolute_liquidity_ratio = str(
            round((float(df1.loc[df1['2'] == '1250']['3']) / float(df1.loc[df1['2'] == '1500']['3'])), 3))
    except:
        absolute_liquidity_ratio = 'Недостаточно данных для расчёта'
    try:
        asset_turnover = str(round((float(df.loc[df['2'] == '2110']['3']) * 2 / 
                                    (float(df1.loc[df1['2'] == '1600']['3']) + 
                                     float(df1.loc[df1['2'] == '1600']['4']))), 3))
    except:
        asset_turnover = 'Недостаточно данных для расчёта'

    df_return = pd.DataFrame([('Рентабельность продаж', return_on_sales), ('Валовая маржа', gross_margin), ('Рентабельность затрат', cost_effectiveness),
                             ('Рентабельность капитала', return_on_capital), ('Коэффициент текущей ликвидности', current_liquidity_ratio),
                              ('Коэффициент абсолютной ликвидности', absolute_liquidity_ratio), ('Оборачиваемость активов', asset_turnover)],
                             columns=['Наименование', 'Значение'])

    print('Введите желаемое имя итогового файла с расчётами')
    new_file = input()
    with pd.ExcelWriter(f'{new_file}.xlsx', engine='openpyxl') as writer:
        df_return.to_excel(writer, sheet_name='Sheet1', index=False)
        auto_adjust_columns(writer, 'Sheet1', df_return)
    print(f'Файл с полученными значениями находится в папке программы с именем "{new_file}"')
    download()

def auto_adjust_columns(writer, sheet_name, df):
    worksheet = writer.sheets[sheet_name]

    for idx, col in enumerate(df.columns):
        # Находим максимальную длину в колонке
        max_len = max(
            df[col].astype(str).apply(len).max(),  # Данные
            len(str(col))  # Заголовок
        )
        # Устанавливаем ширину (+ небольшой запас)
        worksheet.column_dimensions[chr(65 + idx)].width = max_len + 2

def download():
    print('Введите ИНН организации')
    NHH = input()
    # Настройка Selenium
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Фоновый режим
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Открываем страницу
        driver.get(f"https://bo.nalog.gov.ru/search?query={NHH}")
        time.sleep(5)  # Ждём загрузки JS

        # Ищем кнопки и выполняем переход
        driver.find_element(By.XPATH, '//*[@id="short-info"]/div[2]/button').click()
        time.sleep(5)
        button = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div/div[2]/div[2]/a')
        file_url = button.get_attribute("href")
        driver.get(f"{file_url}")
        time.sleep(5)
        driver.find_element(By.XPATH, '//*[@id="root"]/main/div[2]/div[1]/div/div/div[2]/div/div[1]/div[2]/div/button').click()
        driver.find_element(By.XPATH, '//*[@id="root"]/main/div[2]/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div/div/div[2]/form/div[1]/button[1]').click()
        driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div/div/div[3]/button/span').click()
        time.sleep(10)
        driver.quit()


    except Exception as e:
        print("Ошибка. Возможно такой организации нет на сайте.")
        driver.quit()
        download()
    

    search_term = NHH
    downloads_path = Path(str(Path.home() / "Downloads")) # Текущая директория
    current_path = Path(".")

    found_files = [str(f) for f in downloads_path.rglob("*") if search_term in str(f).lower()]
    found_files = str(found_files[0])
    print(found_files)


    with zipfile.ZipFile(found_files, 'r') as zip_ref:
        zip_ref.extractall('.')  # Извлечь всё в указанную папку

    file = [str(f) for f in current_path.rglob("*") if search_term in str(f).lower()]
    file = str(file[0])
    print(file)
    excel(file)
download()
