import textwrap
from urllib.parse import urljoin


def parse_book_page(soup):
    title, author = soup.select_one('h1').text.split('::')
    title = textwrap.shorten(title.strip(), width=100)
    author = author.strip()
    raw_genres = soup.select_one('span.d_book').select('a')
    genres = [genre.text for genre in raw_genres]
    img_tag_url = soup.select_one('.bookimage img')['src']
    img_url = urljoin('http://tululu.org', img_tag_url)
    txt_tag_url = soup.select_one('[href^="/txt.php?id="]')['href']
    txt_url = urljoin('http://tululu.org', txt_tag_url)
    raw_comments = soup.select('.texts>.black')
    book_comments = [comments.text for comments in raw_comments]
    return {
        'title': title,
        'author': author,
        'genres': genres,
        'comments': book_comments,
        'img_url': img_url,
        'txt_url': txt_url,
    }