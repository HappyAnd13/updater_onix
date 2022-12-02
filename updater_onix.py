from tqdm import tqdm
import requests
import cgi
import sys

print("Updater_Onix version 0.01 (c) 2022, HappyAnd_13")

#url = sys.argv[1]
url="https://raw.githubusercontent.com/HappyAnd13/updater_onix/main/README.md"
# установим значение в 1024 байт за один раз
buffer_size = 1024
# загрузка тела ответа по кускам
response = requests.get(url, stream=True)
# получим размер файла
file_size = int(response.headers.get("Content-Length", 0))

# получим имя файла
default_filename = url.split("/")[-1]

# получим заголовок content disposition, обозначающий что файл #предназначен для скачивания
content_disposition = response.headers.get("Content-Disposition")

# если данный элемент существует
if content_disposition:
    # разбираем заголовок с помощью cgi
    value, params = cgi.parse_header(content_disposition)

    # извлекаем имя файла из content disposition
    filename = params.get("filename", default_filename)
else:
    # если же content dispotion не доступен то используем имя из url
    filename = default_filename
    # индикатор выполнения отражает количество загруженных байт
progress = tqdm(response.iter_content(buffer_size), f"Загрузка {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    for data in progress.iterable:
        # запись данных прочитанных из файла
        f.write(data)
        # update the progress bar manually
        progress.update(len(data))
