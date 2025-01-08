from ..entities import Account
from ..exception import NoMoreAccountException

class AccountManager:
    
    current_account_index: int
    account_data: list[Account]
    
    def __init__(self):
        self.account_data = []
        self.current_account_index = 0
        
    def add(self, account: Account):
        self.account_data.append(account)
        
    def get_current(self) -> Account:
        return self.account_data[self.current_account_index]
    
    def switch(self):
        if len(self.account_data) <= self.current_account_index:
            raise NoMoreAccountException
        print('[!] Switch account...')
        self.current_account_index += 1