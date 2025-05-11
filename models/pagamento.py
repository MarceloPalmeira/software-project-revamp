from abc import ABC, abstractmethod
import uuid

class Payment(ABC):
    def __init__(self, valor: float):
        self.valor = valor

    @abstractmethod
    def processar_pagamento(self) -> str:
        pass


class CartaoPayment(Payment):
    def __init__(self, valor: float, tipo: str = "crédito"):
        super().__init__(valor)
        self.tipo = tipo
        self.nome = ""
        self.numero = ""
        self.validade = ""
        self.cvv = ""

    def preencher_dados(self, nome: str, numero: str, validade: str, cvv: str):
        self.nome = nome
        self.numero = numero
        self.validade = validade
        self.cvv = cvv

    def processar_pagamento(self) -> str:
        return f"Pagamento de R${self.valor:.2f} realizado com cartão de {self.tipo}."


class DinheiroPayment(Payment):
    def __init__(self, valor: float):
        super().__init__(valor)
        self.codigo_pedido = str(uuid.uuid4())[:10]

    def processar_pagamento(self) -> str:
        return f"Apresente o código {self.codigo_pedido} no caixa e pague R${self.valor:.2f}."


class PixPayment(Payment):
    def __init__(self, valor: float):
        super().__init__(valor)
        self.chave_pix = str(uuid.uuid4())

    def processar_pagamento(self) -> str:
        return f"Transfira R${self.valor:.2f} para a chave PIX: {self.chave_pix}."
