from files import FileManager
from datetime import datetime, timedelta

user_file = FileManager("users.json")
users = user_file.load()

class Account:
    def __init__(self, name, email, password, menu):
        self.__name = name
        self.__email = email
        self.__password = password
        self.__menu = menu

    # Função para criar conta (usando o AccountBuilder)
    def create_account(self):
        if not self.validate_email(self.__email):
            print("Email inválido.")
            return

        if self.__email in users:
            print("Conta já existente. Faça login.")
            return
        
        # Usando o AccountBuilder para criar a conta
        from contaBuilder import AccountBuilder  # Importando o AccountBuilder aqui para evitar import circular
        builder = AccountBuilder()
        account = builder.set_name(self.__name) \
                         .set_email(self.__email) \
                         .set_password(self.__password) \
                         .set_menu(self.__menu) \
                         .build()

        # Salvar o usuário na base de dados
        users[self.__email] = {'name': self.__name, 'password': self.__password, 'history': []}
        user_file.save(users)
        print("Conta criada com sucesso!")
        print()
        account.__menu(self)  # Passando 'self' para o método __menu

    @staticmethod
    def validate_email(email):
        return "@" in email

    def __menu(self, user):
        print(f"Bem-vindo, {user.__name}!")  # Usando 'user' para acessar os dados
        print("[1] Ver dados")
        print("[2] Alterar senha")
        print("[3] Ver histórico")
        print("[4] Cancelar reserva")
        print("[5] Sair")
        option = input("Escolha uma opção: ")
        if option == "1":
            print(f"Nome: {user.__name}\nE-mail: {user.__email}")
        elif option == "2":
            new_password = input("Digite a nova senha:\n")
            user.set_password(new_password)
            print("Senha atualizada com sucesso!")
        elif option == "3":
            user.show_history()
        elif option == "4":
            user.delete_history(input("Digite o código do ingresso que deseja cancelar:\n=> "))
        elif option == "5":
            print("Saindo...")
        else:
            print("Opção inválida.")
    
    def login(self):
        users = user_file.load()
        if self.__email in users and users[self.__email]['password'] == self.__password:
            self.__name = users[self.__email]['name']
            print(f"Bem-vindo, {self.__name}!")
            print()
            self.__menu(self)  # Passando 'self' para o método __menu
        else:
            print("Email ou senha incorretos.")
            print()

    def show_history(self):
        users = user_file.load()  # Carregando os dados dos usuários do arquivo
        if self.__email in users:
            user_history = users[self.__email]["history"]
            if not user_history:
                print("Nenhum histórico de reservas encontrado.")
                print()
            else:
                print(f"Histórico de reservas para {self.__name}:")
                for i, history_entry in enumerate(user_history, 1):
                    print(f"Reserva {i}:")
                    print(f"  Cinema: {history_entry['Cinema']}")
                    print(f"  Filme: {history_entry['Filme']}")
                    print(f"  Ingresso: {history_entry['Ticket']}")
                    print(f"  Cadeira(s): {', '.join(history_entry['Cadeiras'])}")
                    print(f"  Horário do Filme: {history_entry['Horario_filme']}")
                    print(f"  Horário da compra: {history_entry['Horario_compra']}")
                    print()
        else:
            print("Usuário não encontrado.")
            print()

    def delete_history(self, entry_ticket):
        users = user_file.load()  # Carregando os dados dos usuários do arquivo
        users[self.__email]["history"] = [entry for entry in users[self.__email]["history"] if entry["Ticket"] != entry_ticket]
        user_file.save(users)
        print("Reserva cancelada com sucesso!")
        self.__menu(self)  # Passando 'self' para o método __menu

    def change_data(self):
        users = user_file.load()  # Carregando os dados dos usuários do arquivo
        while True:
            option = input("Escolha uma opção:\n[1] Ver dados\n[2] Alterar senha\n[3] Ver Histórico\n[4] Cancelar Reserva\n[5] Sair\n=> ")
            if option == "1":
                print(f"Nome: {self.__name}\nE-mail: {self.__email}\nSenha: {users[self.__email]['password']}")
            elif option == "2":
                new_password = input("Digite a nova senha:\n")
                self.set_password(new_password)
                users[self.__email]["password"] = self.__password
                user_file.save(users)
                print("Senha atualizada com sucesso!")
            elif option == "3":
                self.show_history()
            elif option == "4":
                self.delete_history(input("Digite o código do ingresso que deseja cancelar:\n=> "))
            elif option == "5":
                print("Voltando para o menu...")
                return
            else:
                print("Opção inválida.")
                print()

    def set_password(self, new_password):
        self.__password = new_password

    def set_name(self, new_name):
        self.__name = new_name

    def set_email(self, new_email):
        if self.validate_email(new_email):
            self.__email = new_email
        else:
            print("Email inválido.")
