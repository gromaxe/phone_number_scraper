import requests
from bs4 import BeautifulSoup
import re


def find_phone_numbers(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()

        # первый вариант регулярки, 8-___-___-__-__
        phone_regex = re.compile(r'8[\s]*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})')
        phones = phone_regex.findall(text)

        formatted_phones = set(['8{}{}{}{}'.format(*phone) for phone in phones])

        return list(formatted_phones)
    except requests.RequestException as e:
        print(f"Ошибка при загрузке страницы {url}: {e}")
        return []


if __name__ == "__main__":
    urls = [
        "https://hands.ru/company/about",
        "https://repetitors.info"
    ]

    phone_numbers = {}
    for url in urls:
        phones = find_phone_numbers(url)
        if phones:
            phone_numbers[url] = phones
            print(f"Номера телефонов на {url}: {phones}")
        else:
            print(f"Номера телефонов на {url} не найдены.")

