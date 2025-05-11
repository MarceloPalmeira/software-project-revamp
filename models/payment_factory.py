from models.pagamento import Payment, CartaoPayment, PixPayment, DinheiroPayment


class PaymentFactory:
    @staticmethod
    def create(tipo: str, valor: float) -> Payment:
        tipo = tipo.lower()

        if tipo == "cartao":
            pagamento = CartaoPayment(valor)
            pagamento.preencher_dados("Usuário", "0000000000000000", "12/29", "123")  # simulação
            return pagamento
        elif tipo == "pix":
            return PixPayment(valor)
        elif tipo == "dinheiro":
            return DinheiroPayment(valor)
        else:
            raise ValueError(f"Método de pagamento inválido: {tipo}")
