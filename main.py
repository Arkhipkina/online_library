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


def get_url_image(response):
    soup = BeautifulSoup(response.text, 'lxml')
    img_tag = soup.find(class_="bookimage").find("img")["src"]
    imgpath = urljoin("https://tululu.org/", img_tag)
    return imgpath


def dowload_image(imgpath, filename, folder="books_image"):
    response = requests.get(imgpath)
    response.raise_for_status()
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)


def get_comments(response):
    soup = BeautifulSoup(response.text, 'lxml')
    comments_tag = soup.find_all(class_="texts")
    all_comments = [comment_book.find(class_="black").text for comment_book in comments_tag]
    print(all_comments)



def main():
    Path("books").mkdir(parents=True, exist_ok=True)
    Path("books_image").mkdir(parents=True, exist_ok=True)
    Path("books_comments").mkdir(parents=True, exist_ok=True)


    for id in range(1, 11):
        url_for_downloading = f"https://tululu.org/txt.php?id={id}"
        filename = f'books/book_{id}.txt'
        response_for_downloading = requests.get(url_for_downloading)
        response_for_downloading.raise_for_status()
        try:
            check_for_redirect(response_for_downloading)
        except requests.exceptions.HTTPError:
            continue
        page_url = f"https://tululu.org/b{id}"
        page_response = requests.get(page_url)
        page_response.raise_for_status()
        filename = get_books_name(page_response)
        download_txt(page_response, f"{id}. {filename}.txt")
        imgpath = get_url_image(page_response)
        if imgpath == "https://tululu.org/images/nopic.gif":
            filename = "nopic.gif"
        else:
            filename = f"{id}.png"
        dowload_image(imgpath, filename)
        get_comments(page_response)


if __name__ == "__main__":
    main()