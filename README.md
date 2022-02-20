# Парсер книг с сайта tululu.org

## Скрипт `parse_tululu_category.py`.

Скачивает книги в формате `txt`, картинки и файл с данными формат .json(краткое описание, комментарии, жанр, ссылка на книгу и картинку) к ним с [сайта   
БОЛЬШАЯ БЕСПЛАТНАЯ БИБЛИОТЕКА](http://tululu.org) в указанном диапазоне страниц, жанр ["Научная фантастика"](http://tululu.org/l55/).
**Качает только те книги которые есть на сайте и только в формате `txt`**

### Аргументы

Принимает аргументы

`--start_page` целое число(начало диапазона)

`--end_page` целое число(конец диапазона)

#### Пример:

```bash
python parse_tululu_category.py --start_page 1 --end_page 2
```
Скачает книги с первой страницы  в папку `books` картинки к ним в папку `images` и файл с данными в формате `.json` в папку скрипта

пример файла `.json`

```
[
    {
        "title": "Алиби",
        "author": "ИВАНОВ Сергей",
        "genres": [
            "Научная фантастика",
            "Прочие Детективы"
        ],
        "comments": [
            "Детский вариант анекдотов про Шерлока Холмса)",
            "Загадки я люблю.)))",
            "А мне понравилось, люблю, знаете ли, всякие загадочки, головоломочки, кроссвордики, Гимнастика ума, одним словом... \nВо всём можно найти положительные моменты, не разгадал загадку, так хоть гренки научился готовить отменные... :-)",
            "Очень поучительное для ребенка 10 лет."
        ],
        "img_url": "http://tululu.org/shots/239.jpg",
        "txt_url": "http://tululu.org/txt.php?id=239",
        "book_path": "/home/user/books/Алиби.txt",
        "img_src": "/home/user/images/239.jpg"
    }
]
```
Также принимает дополнительные аргументы

#### Примеры:

Пропускает загрузку книг
```
python parse_tululu_category.py --skip_txt
```

Пропускает загрузку картинок
```
python parse_tululu_category.py --skip_imgs
```

Принимает пользовательский путь для книг, картинок и файла с данными(формат .json)
```
python parse_tululu_category.py --dest_folder /home/user
```

Принимает пользовательский путь для файла с данными(формат .json)
```
python parse_tululu_category.py --json_path /home/user
```
**Все аргументы не обязательны если не указывать скачает все книги жанра ["Научная фантастика"](http://tululu.org/l55/) с 1 по 701 страницу**



## Скрипт `download_books.py`.

Скачивает книги и картинки к ним с [сайта
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


## Скрипт `render_website.`

Создает готовые web - страницы с книгами и  обложками к ним(если таковые имеются) по 20 книг на странице с работающей пагинацией и возможностью чтения книг. Можно запустить сайт локально будет доступен по адресу [http://127.0.0.1:5500/pages/index1.html](http//127.0.0.1:5500/pages/index1.html) или разместить на [GitHub Pages](https://pages.github.com/). 

[Подробная инструкция по работе на GitHub Pages](https://medium.com/nuances-of-programming/%D0%BA%D0%B0%D0%BA-%D1%81%D0%BE%D0%B7%D0%B4%D0%B0%D1%82%D1%8C-%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D1%8B%D0%B9-%D1%81%D0%B0%D0%B9%D1%82-%D0%BD%D0%B0-github-pages-e0f3c258ee22)

[Пример размещенного на GitHub Pages сайта с книгами](https://cadibob.github.io/Download_books/pages/index1.html)

Пример страницы

![](/example.png)

### Как запустить:
 
#### Аргументы

Принимает пользовательский путь для файла с данными(формат .json)

```bash
python render_website.py --json_path /home/user
```

Также можно указать колличество книг в каждой колонке, по умолчанию 10(20 книг на страницу)

```bash
python render_website.py --column_size 20
```

или без аргумента

```bash
python render_website.py
```
Запускает локальный сервер:

```
(user@learnpc:~/Python$ python render_website.py
[I 220219 22:00:59 server:335] Serving on http://127.0.0.1:5500
[I 220219 22:00:59 handlers:62] Start watching changes
[I 220219 22:00:59 handlers:64] Start detecting changes

```

### Как установить

Python3 должен быть уже установлен. 
Затем используйте `pip` или `pip3` для установки зависимостей:

```bash
pip install -r requirements.txt
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).