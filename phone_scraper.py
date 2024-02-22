import requests
from bs4 import BeautifulSoup
import re


def find_phone_numbers(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()

        phone_regex = re.compile(
            r'(\+7|8|7)?[\s\-\.]*\(?\s*(\d{3})\s*\)?[\s\-\.]*(\d{1,3})[\s\-\.]*(\d{2})[\s\-\.]*(\d{2})'
        )
        raw_phones = phone_regex.findall(text)

        formatted_phones = set()  # отсеет повторы
        for raw_phone in raw_phones:
            digits = re.sub(r'\D', '', ''.join(raw_phone))

            if len(digits) not in (7, 10, 11):
                continue

            # Приведение к формату 8KKKNNNNNNN
            if len(digits) == 10:
                digits = '8' + digits
            elif len(digits) == 11 and digits[0] in ['7', '8']:
                digits = '8' + digits[1:]
            elif len(digits) == 7:
                digits = '8' + digits[1:]

            formatted_phones.add(digits)

        return list(formatted_phones)
    except requests.RequestException as e:
        print(f"Ошибка при загрузке страницы {url}: {e}")
        return []


if __name__ == "__main__":
    urls = [
        "https://hands.ru/company/about",
        "https://repetitors.info",
        "https://targetsms.ru/blog/1074-format-telefonnykh-nomerov"
    ]

    phone_numbers = {}
    for url in urls:
        phones = find_phone_numbers(url)
        if phones:
            phone_numbers[url] = phones
            print(f"Номера телефонов на {url}: {phones}")
        else:
            print(f"Номера телефонов на {url} не найдены.")
