class Account:
    def __init__(self, name: str, email: str, password: str):
        self.__name = name
        self.__email = email
        self.__password = password
        self.__history = []

    @property
    def name(self):
        return self.__name

    @property
    def email(self):
        return self.__email

    @property
    def password(self):
        return self.__password

    @property
    def history(self):
        return self.__history

    def set_password(self, new_password):
        self.__password = new_password

    def add_history(self, ingresso):
        self.__history.append(ingresso)

    def remove_history_by_code(self, code):
        self.__history = [h for h in self.__history if h['Ticket'] != code]


class AccountBuilder:
    def __init__(self):
        self._name = None
        self._email = None
        self._password = None

    def set_name(self, name: str):
        self._name = name
        return self

    def set_email(self, email: str):
        self._email = email
        return self

    def set_password(self, password: str):
        self._password = password
        return self

    def build(self):
        if not self._name or not self._email or not self._password:
            raise ValueError("Todos os campos são obrigatórios para criar uma conta.")
        return Account(self._name, self._email, self._password)
