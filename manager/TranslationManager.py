import sys
import requests
from typing import TypedDict, Literal
from ..exception import ExpiredAccountException, NoMoreAccountException
from .AccountManager import AccountManager

class Config(TypedDict):
    translateMode: Literal["html", "text"]

class TranslationManager:

    config: Config
    translator_service_url: str
    account_manager: AccountManager

    def __init__(self, account_manager: AccountManager) -> None:
        super().__init__()
        self.account_manager = account_manager
        self.config = {"translateMode": "html"}
        self.translator_service_url = "https://api-b2b.backenster.com/b1/api/v3/translate"
        
    def generate_config(self, data: list[str]):
        return {
            "to": "mg_MG",
            "from": "en_US", 
            "data": data, 
            "platform": "api", 
            "translateMode": self.config["translateMode"]
        }

    def translate_sentences(self, sentences: list[str], token: str) -> list[str]:
        payload = self.generate_config(sentences)
        headers = {"Authorization": token,"accept": "application/json","content-type": "application/json"}
        response = requests.post(self.translator_service_url, json=payload, headers=headers)
        response = response.json()

        if response["err"] is not None:
            print(response)
            raise ExpiredAccountException

        return response["result"]

    def translate(self, sentences: list[str]) -> list[str]:
        try:
            account = self.account_manager.get_current()
            translated_sentence = self.translate_sentences(sentences, token=account.token)
            return translated_sentence
        except ExpiredAccountException:
            print(f'[!] {account.email} expired !!!')
            self.account_manager.switch()
            return self.translate(sentences)
        except NoMoreAccountException:
            print("[!] Dead !!!")
            sys.exit(1)
