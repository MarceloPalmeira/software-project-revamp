from conta import Account  
from movies import CinemaManager
from review import Review
# Menu principal
def menu(user):
    while True:
        try:
            print("-------- MENU -------")
            choice = int(input("Escolha uma opção:\n[1] Perfil\n[2] Ver cinemas\n[3] Fazer review\n[4] Ver reviews\n[5] Sair\n=> "))
            if choice == 1:
                user.change_data()
                break
            elif choice == 2:
                manager = CinemaManager("cinemas.json", "users.json", user,menu)
                manager.available_cinemas()
                break
            elif choice == 3:
                while True:
                    try:
                        print()
                        number = int(input("Qual filme deseja avaliar:\n[1] De volta Para O Futuro\n[2] Elvis\n[3] Grease\n[4] High School Musical\n[5] Mamma Mia\n[6] O Rei Do Show\n=> "))
                        if number in [1,2,3,4,5,6]:
                            
                            review = Review(number,user)
                            review.options(menu)
                            break 
                        else:
                            print("Opção inválida. Por favor, escolha um número entre 1 e 6.")
                    except ValueError:
                        print("Opção Inválida. Tente novamente.")
                break
            elif choice == 4:
                while True:
                    try:
                        print()
                        number = int(input("Qual filme deseja ver as avaliações:\n[1] De volta Para O Futuro\n[2] Elvis\n[3] Grease\n[4] High School Musical\n[5] Mamma Mia\n[6] O Rei Do Show\n=> "))
                        if number in [1,2,3,4,5,6]:
                            
                            review = Review(number,user)
                            review.show_reviews(menu)
                            break 
                        else:
                            print("Opção inválida. Por favor, escolha um número entre 1 e 6.")
                    except ValueError:
                        print("Opção Inválida. Tente novamente.")
                break
                
            elif choice == 5:
                print("Saindo...")
                return
            else:
                print("Opção inválida.")
        except ValueError:
            print("Opção inválida.")

def main_menu():
# Menu inicial
    while True:
        choice = input("Escolha uma opção:\n[1] Criar conta\n[2] Log-in\n[3] Sair\n=> ")
        if choice == "1":
            print()
            name = input("Digite seu nome: ")
            email = input("Digite seu email: ")
            password = input("Digite sua senha: ")
            print()
            account = Account(name, email, password,menu)
            
            account.create_account()
        elif choice == "2":
            print()
            email = input("Digite seu email: ")
            password = input("Digite sua senha: ")
            print()
            account = Account(name=None,email=email, password=password,menu=menu)
            account.login()
        elif choice == "3":
            print()
            print("Saindo...")
            print()
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main_menu() 
