from database.files import FileManager
from models.pagamento import CartaoPayment, PixPayment, DinheiroPayment
from ingressos.ingressos import IngressoManager
from models.user import Account
from models.payment_factory import PaymentFactory

class CinemaManager:
    def __init__(self, user: Account):
        self.__user = user
        self.__cinemas_data = FileManager("cinemas.json").load()
        self.__users_data = FileManager("users.json").load()
        self.__file_cinemas = FileManager("cinemas.json")
        self.__file_users = FileManager("users.json")

    def listar_cinemas(self):
        return list(self.__cinemas_data.keys())

    def listar_filmes(self, cinema_nome: str):
        return self.__cinemas_data[cinema_nome]["Movies"]

    def listar_horarios(self, cinema_nome: str, filme: str):
        return self.__cinemas_data[cinema_nome]["schedule"][filme]

    def listar_assentos(self, cinema_nome: str, filme: str):
        return self.__cinemas_data[cinema_nome]["seat"][filme]

    def reservar_assento(self, cinema_nome: str, filme: str, horario: str, assento: str, cupom: str, metodo: str):
        # Verificações
        assentos = self.__cinemas_data[cinema_nome]["seat"][filme]
        if assento not in assentos or assentos[assento] != "disponível":
            return False, "Assento inválido ou indisponível."

        # Reservar o assento
        assentos[assento] = "reservado"
        self.__file_cinemas.save(self.__cinemas_data)

        # Cálculo de preço
        total = 20.00
        if cupom.strip().upper() == "10CONTO":
            total *= 0.9

        # Processar pagamento com polimorfismo
        pagamento = PaymentFactory.create(metodo, total)
        confirmacao = pagamento.processar_pagamento()

        # Criar ingresso
        ingresso = {
            "Ticket": f"{self.__user.email[:3]}_{assento}",
            "Cinema": cinema_nome,
            "Filme": filme,
            "Cadeiras": [assento],
            "Horario_filme": horario,
            "Horario_compra": "agora",
            "Valor": f"R${total:.2f}",
            "Método": metodo
        }

        # Atualizar histórico do usuário
        self.__user.add_history(ingresso)
        self.__users_data[self.__user.email]["history"] = self.__user.history
        self.__file_users.save(self.__users_data)

        # Enviar ingresso por e-mail
        ingresso_manager = IngressoManager()
        ingresso_manager.gerar_ingresso(
            user=self.__user,
            cinema=cinema_nome,
            filme=filme,
            cadeiras=[assento],
            horario_filme=horario
)

        return True, confirmacao
