from models.user import Account, AccountBuilder
from database.files import FileManager

class AuthManager:
    def __init__(self):
        self.__users_file = FileManager("users.json")
        self.__users_data = self.__users_file.load()

    def login(self, email: str, password: str) -> Account | None:
        user = self.__users_data.get(email)
        if user and user["password"] == password:
            return AccountBuilder()\
                .set_name(user["name"])\
                .set_email(email)\
                .set_password(password)\
                .build()
        return None

    def create_account(self, name: str, email: str, password: str) -> tuple[bool, str]:
        if email in self.__users_data:
            return False, "Email já cadastrado."

        account = AccountBuilder()\
            .set_name(name)\
            .set_email(email)\
            .set_password(password)\
            .build()

        self.__users_data[email] = {
            "name": account.name,
            "password": account.password,
            "history": []
        }
        self.__users_file.save(self.__users_data)
        return True, "Conta criada com sucesso."

    def get_account(self, email: str) -> Account | None:
        user = self.__users_data.get(email)
        if user:
            acc = AccountBuilder()\
                .set_name(user["name"])\
                .set_email(email)\
                .set_password(user["password"])\
                .build()
            acc._Account__history = user.get("history", [])
            return acc
        return None

    def update_password(self, email: str, new_password: str) -> str:
        if email not in self.__users_data:
            return "Usuário não encontrado."
        self.__users_data[email]["password"] = new_password
        self.__users_file.save(self.__users_data)
        return "Senha atualizada com sucesso."

    def update_history(self, account: Account):
        self.__users_data[account.email]["history"] = account.history
        self.__users_file.save(self.__users_data)
