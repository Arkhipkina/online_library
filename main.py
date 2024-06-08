import requests
import os.path
import argparse
import time
from urllib.parse import urljoin
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(response):
    if response.history: 
        raise requests.exceptions.HTTPError


def download_txt(response, filename, folder="books"):
    filename = sanitize_filename(filename)
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


def dowload_image(imgurl, filename, folder="books_image"):
    response = requests.get(imgurl)
    response.raise_for_status()
    filepath = os.path.join(folder, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)


def parse_book_page(response, page_url):
    soup = BeautifulSoup(response.text, 'lxml')

    title_tag = soup.find(id="content").find("h1")
    title_text = title_tag.text
    book_title, book_author = title_text.split(" :: ")
    book_title = book_title.strip()
    book_author = book_author.strip()

    genre_tags = soup.find("span", class_="d_book").find_all("a")
    genres = [genre_books.text for genre_books in genre_tags]

    comments_tag = soup.find_all(class_="texts")
    all_comments = [comment_book.find(class_="black").text for comment_book in comments_tag]

    img_tag = soup.find(class_="bookimage").find("img")["src"]
    imgurl = urljoin(page_url, img_tag)

    book_page = {
        "Title": book_title,
        "Author": book_author,
        "Genre": genres,
        "Comments": all_comments,
        "Imgurl": imgurl
    }

    return book_page


def get_optional_arguments():
    parser = argparse.ArgumentParser(description='downloading books from online library')
    parser.add_argument("-s", "--start_id", help='add start id of book', default=1, type=int)
    parser.add_argument("-e", "--end_id", help='add end id of book', default=10, type=int)
    args = parser.parse_args()
    start_id = args.start_id
    end_id = args.end_id

    return start_id, end_id

def main():
    Path("books").mkdir(parents=True, exist_ok=True)
    Path("books_image").mkdir(parents=True, exist_ok=True)

    start_id, end_id = get_optional_arguments()
    for number in range(start_id, end_id+1):
        try:
            url_for_downloading = f"https://tululu.org/txt.php"
            params = {'id': number}
            
            filename = f'books/book_{number}.txt'
            
            response_for_downloading = requests.get(url_for_downloading, params=params)
            response_for_downloading.raise_for_status()

            check_for_redirect(response_for_downloading)

            page_url = f"https://tululu.org/b{number}"

            page_response = requests.get(page_url)
            page_response.raise_for_status()
            check_for_redirect(page_response)

            download_txt(response_for_downloading, f"{number}. {filename}")
            
            book_page = parse_book_page(page_response, page_url)
            imgurl = book_page['Imgurl']

            if imgurl == "https://tululu.org/images/nopic.gif":
                filename_image = "nopic.gif"
            else:
                filename_image = f"{number}.png"

            dowload_image(imgurl, filename_image)
        except requests.exceptions.HTTPError:
            print('Книги не существует.')
        except requests.exceptions.ConnectionError:
            print('Проверьте подключение к интернету.')
            time.sleep(5)



if __name__ == "__main__":
    main()