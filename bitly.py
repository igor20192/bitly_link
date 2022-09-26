import json
import logging
import requests
import os
from dotenv import load_dotenv

logging.basicConfig(
    filename="exc_bitly.log", format="[%(asctime)s] [%(levelname)s] => %(message)s]"
)


def shorten_link(url: str, token: str) -> str:
    try:
        data = {"long_url": url}
        response = requests.post(
            "https://api-ssl.bitly.com/v4/bitlinks",
            headers={"Authorization": token},
            data=json.dumps(data),
        )
        response.raise_for_status()

        return f'Битлинк: {response.json()["id"]}'

    except requests.exceptions.RequestException as exc:
        logging.exception("%s", exc.__doc__)
        return f"ERROR: {exc.__doc__} > Проверьте введенные данные!"


def count_clicks(bitlink: str, token: str) -> str:
    params = {"units": -1}
    try:
        response = requests.get(
            f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary",
            params=params,
            headers={"Authorization": token},
        )
        response.raise_for_status()
        return f'По вашей ссылке прошли: {response.json()["total_clicks"]}раз(а)'

    except requests.exceptions.RequestException as exc:
        logging.exception("%s", exc.__doc__)
        return f"ERROR: {exc.__doc__} > Проверьте введенные данные!"


def is_bitlink(url: str, token: str) -> str:
    response = requests.get(
        f"https://api-ssl.bitly.com/v4/bitlinks/{url}", headers={"Authorization": token}
    )
    if response.ok:
        return count_clicks(url, token)
    return shorten_link(url, token)


def main() -> None:
    token = os.getenv("BITLY_TOKEN ")
    url = input("Введите ссылку  : ")
    print(is_bitlink(url, token))


if __name__ == "__main__":
    load_dotenv()
    main()
