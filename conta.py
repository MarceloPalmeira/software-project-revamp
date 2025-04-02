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

# Poderia por um @property no lugar de um get ou set
    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    
    def set_name(self, new_name):
        self.__name = new_name

    def set_email(self, new_email):
        if self.validate_email(new_email):
            self.__email = new_email
        else:
            print("Email inválido.")

    def set_password(self, new_password):
        self.__password = new_password

    
    @staticmethod
    def validate_email(email):
        return "@" in email

   # Função para criar conta
    def create_account(self):
        if not self.validate_email(self.__email):
            print("Email inválido.")
            return

        if self.__email in users:
            print("Conta já existente. Faça login.")
            return

        users[self.__email] = {'name': self.__name, 'password': self.__password, 'history': []}
        user_file.save(users)
        print("Conta criada com sucesso!")
        print()
        self.__menu(self)

    # Função para fazer login
    def login(self):
        if self.__email in users and users[self.__email]['password'] == self.__password:
            self.__name = users[self.__email]['name']
            print(f"Bem-vindo, {self.__name}!")
            print()
            self.__menu(self)
        else:
            print("Email ou senha incorretos.")
            print()
            return

    # Função para mostrar histórico
    def show_history(self):
        users = user_file.load()
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

   # Função para deleter alguma compra do histórico 
    def delete_history(self, entry_ticket):
        users[self.__email]["history"] = [entry for entry in users[self.__email]["history"] if entry["Ticket"] != entry_ticket]
        user_file.save(users)
        print("Reserva cancelada com sucesso!")
        self.__menu(self)

   # Função do menu da parte de contas do usuário
    def change_data(self):
        users = user_file.load()
        while True:
            option = input("Escolha uma opção:\n[1] Ver dados\n[2] Alterar senha\n[3] Ver Histórico\n[4] Cancelar Reserva\n[5] Sair\n=> ")
            if option == "1":
                print()
                print(f"Nome: {self.__name}\nE-mail: {self.__email}\nSenha: {users[self.__email]['password']}")
                print()
            elif option == "2":
                print()
                new_password = input("Digite a nova senha:\n")
                self.set_password(new_password)
                users[self.__email]["password"] = self.__password
                user_file.save(users)
                print("Senha atualizada com sucesso!")
                print()
            elif option == "3":
                self.show_history()
            elif option == "4":
                users = user_file.load()
                if not users[self.__email]['history']:
                    print("Você não tem nenhuma reserva no histórico.")
                    print()
                    return self.__menu(self)

                print("OBS.: Os ingressos só podem ser cancelados até 1h antes do filme.")
                print("Digite '0' a qualquer momento para retornar ao menu.")
                print()

                while True:
                    try:
                        ticket = input("Digite o código do ingresso que deseja cancelar:\n=> ")
                        if ticket == "0":
                            print()
                            return self.__menu(self)

                        for entry in users[self.__email]['history']:
                            if entry['Ticket'] == ticket:
                                current_time = datetime.now().strftime("%H:%M")
                                current_time_obj = datetime.strptime(current_time, "%H:%M").time()
                                schedule = entry['Horario_filme']
                                schedule_obj = datetime.strptime(schedule, "%H:%M") - timedelta(hours=1)
                                schedule_obj2 = schedule_obj.time()

                                if current_time_obj < schedule_obj2:
                                    self.delete_history(ticket)
                                else:
                                    print("Não é possível cancelar a compra. Tempo limite expirado.")
                                break
                        else:
                            print("Código inválido. Tente novamente.")
                            continue

                        break
                    except ValueError:
                        print("Entrada inválida. Digite um código válido.")
            elif option == "5":
                print()
                print("Voltando para o menu...")
                print()
                return self.__menu(self)
            else:
                print("Opção inválida.")
                print()
