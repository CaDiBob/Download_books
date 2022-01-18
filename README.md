# Парсер книг с сайта tululu.org

Скрипт скачивает книги и картинки к ним с [сайта	
БОЛЬШАЯ БЕСПЛАТНАЯ БИБЛИОТЕКА](http://tululu.org) в формате `txt` указанном диапазоне `id`.

**Качает только те книги которые есть на сайте и только в формате `txt`**

### Аргументы

Принимает аргументы в виде целых чисел 

`--start_page стартовый id` по умолчанию = `1`

`--end_page конечный id` по умолчанию = `10`


##### Пример запуска:

```bash
python download_books.py 50 60
```
Создаст две папки `books` и `images` в корне скрипта, скачает книги с `id` от 50 до 60 в папку `books` и картинки к ним в папку `images`.


### Как установить

Python3 должен быть уже установлен. 
Затем используйте `pip` или `pip3` для установки зависимостей:

```bash
pip install -r requirements.txt
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).