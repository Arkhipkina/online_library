import requests
import os.path
from urllib.parse import urljoin
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(response):
    if response.history: 
        raise requests.exceptions.HTTPError


def get_books_name(response):
        soup = BeautifulSoup(response.text, 'lxml')
        title_tag = soup.find(id="content").find("h1")
        title_text = title_tag.text
        book_title, book_author = title_text.split(" :: ")
        book_title = book_title.strip()
        return book_title


def download_txt(response, filename, folder="books"):
    filename = sanitize_filename(filename)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


def get_url_image(response, title):
    soup = BeautifulSoup(response.text, 'lxml')
    img = soup.find(class_="bookimage").find("img")["src"]
    imgpath = urljoin("https://tululu.org/", img)
    print(f"Заголовок: {title} \n {imgpath} \n")
    return imgpath


def dowload_image(imgpath, filename, folder="image_books"):
    response = requests.get(imgpath)
    response.raise_for_status()
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)



def main():
    Path("books").mkdir(parents=True, exist_ok=True)
    Path("image_books").mkdir(parents=True, exist_ok=True)


    for id in range(1, 11):
        url = f"https://tululu.org/txt.php?id={id}"
        filename = f'books/book_{id}.txt'
        response = requests.get(url)
        response.raise_for_status()
        try:
            check_for_redirect(response)
        except requests.exceptions.HTTPError:
            continue
        url_for_name = f"https://tululu.org/b{id}"
        response_for_name = requests.get(url_for_name)
        response_for_name.raise_for_status()
        filename = get_books_name(response_for_name)
        download_txt(response, f"{id}. {filename}.txt")
        imgpath = get_url_image(response_for_name, filename)
        if imgpath == "https://tululu.org/images/nopic.gif":
            filename = "nopic.gif"
        else:
            filename = f"{id}.png"
        dowload_image(imgpath, filename)


if __name__ == "__main__":
    main()