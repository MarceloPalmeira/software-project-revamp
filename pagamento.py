from abc import ABC, abstractmethod
import uuid

class Payment(ABC):
    @abstractmethod
    def process_payment(self, amount):     
        pass
    
    def Card_data(self,type):
        card_name = input("Digite o nome no cartão: ")
        card_number = input("Digite o número do cartão: ")
        expiry_date = input("Digite a data de validade (MM/AA): ")
        cvv = int(input("Digite o CVV: "))
        return {
            "card_type": type,
            "card_name": card_name,
            "card_number": card_number,
            "expiry_date": expiry_date,
            "cvv": cvv
        }

class  CardPayment(Payment):
    def process_payment(self, amount):
        while True:
            try:
                choice = int(input("Qual o tipo do cartão:\n[1] Crédito\n[2] Débito\n"))
                if choice == 1:
                    print("Digite as informações do cartão:")
                    card_details = self.Card_data("Crédito")
                    print(f"Processando pagamento de R${amount:.2f} via cartão de crédito.")
                    
                    break
                elif choice == 2:
                    print("Digite as informações do cartão:")
                    card_details = self.Card_data("Débito")  
                    print(f"Processando pagamento de R${amount:.2f} via cartão de débito.")
                    
                    break
                else:
                    print("Opção inválida. Tente novamente.")
            except ValueError:
                print("Opção inválida. Digite um número.")    
                  
class CashPayment(Payment):
    def process_payment(self, amount):
        order = str(uuid.uuid4())[:10]
        print(f"Aqui está o código do seu pedido: {order}. Apresente ele no caixe e realize seu pagamento.")
        print(f"Total: R${amount:.2f}")
        


class PixPayment(Payment):
    def process_payment(self, amount):
        key =str(uuid.uuid4())
        print(f"Para finalizar o pedido tranfira o pagamento para essa chave PIX: {key}")
        print(f"Total: R${amount:.2f}")
        

