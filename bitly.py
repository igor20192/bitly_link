import json
import logging
import requests
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    filename="exc_bitly.log", format="[%(asctime)s] [%(levelname)s] => %(message)s]"
)


class BitlyLinks:
    def __init__(self, token: str) -> None:
        self.url = input("Введите ссылку  : ")
        self.token = token
        self.headers = {"Authorization": self.token}

    def __shorten_link(self) -> str:
        try:
            data = {"long_url": self.url}
            response = requests.post(
                "https://api-ssl.bitly.com/v4/bitlinks",
                headers=self.headers,
                data=json.dumps(data),
            )
            response.raise_for_status()

            return f'Битлинк: {response.json()["id"]}'

        except requests.exceptions.RequestException as exc:
            logging.exception("%s", exc.__doc__)
            return f"ERROR: {exc.__doc__} > Проверьте введенные данные!"

    def __count_clicks(self) -> str:
        params = {"units": -1}
        try:
            response = requests.get(
                f"https://api-ssl.bitly.com/v4/bitlinks/{self.url}/clicks/summary",
                params=params,
                headers=self.headers,
            )
            response.raise_for_status()
            return f'По вашей ссылке прошли: {response.json()["total_clicks"]}раз(а)'

        except requests.exceptions.RequestException as exc:
            logging.exception("%s", exc.__doc__)
            return f"ERROR: {exc.__doc__} > Проверьте введенные данные!"

    def is_bitlink(self) -> str:
        response = requests.get(
            f"https://api-ssl.bitly.com/v4/bitlinks/{self.url}", headers=self.headers
        )
        if response.ok:
            return self.__count_clicks()
        return self.__shorten_link()


token = os.getenv("TOKEN")
if __name__ == "__main__":
    b = BitlyLinks(token)
    print(b.is_bitlink())
