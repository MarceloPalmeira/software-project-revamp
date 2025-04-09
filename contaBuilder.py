from conta import Account

class AccountBuilder:
    def __init__(self):
        self.__name = None
        self.__email = None
        self.__password = None
        self.__menu = None

    def set_name(self, name):
        self.__name = name
        return self

    def set_email(self, email):
        self.__email = email
        return self

    def set_password(self, password):
        self.__password = password
        return self

    def set_menu(self, menu):
        self.__menu = menu
        return self

    def build(self):
        if not self.__name or not self.__email or not self.__password:
            raise ValueError("Faltam informações necessárias para criar a conta!")
        return Account(self.__name, self.__email, self.__password, self.__menu)
