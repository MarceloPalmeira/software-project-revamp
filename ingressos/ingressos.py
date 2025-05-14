import os
import smtplib
import uuid
import qrcode
from email.message import EmailMessage

# Configurações do servidor de e-mail
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "icinema.ufal@gmail.com"
EMAIL_PASSWORD = "bfvj iotl rcaj ixgk"  # 🔐 coloque no .env em produção!

# Segurança mínima para garantir variáveis válidas
if not EMAIL_SENDER or not EMAIL_PASSWORD:
    raise ValueError("EMAIL_SENDER ou EMAIL_PASSWORD ausente.")


class EmailManager:
    def __init__(self, smtp_server, smtp_port, email_sender, email_password):
        self.__smtp_server = smtp_server
        self.__smtp_port = smtp_port
        self.__email_sender = email_sender
        self.__email_password = email_password

    def enviar_email(self, destinatario, assunto, corpo, anexo_path=None):
        if not destinatario or not assunto or not corpo:
            raise ValueError("Destinatário, assunto e corpo são obrigatórios.")

        msg = EmailMessage()
        msg["Subject"] = assunto
        msg["From"] = self.__email_sender
        msg["To"] = destinatario
        msg.set_content(corpo)

        if anexo_path:
            if not os.path.exists(anexo_path):
                raise FileNotFoundError(f"Arquivo não encontrado: {anexo_path}")
            with open(anexo_path, "rb") as f:
                img_data = f.read()
                msg.add_attachment(img_data, maintype="image", subtype="png", filename="Ingresso_QR.png")

        try:
            with smtplib.SMTP(self.__smtp_server, self.__smtp_port) as server:
                server.starttls()
                server.login(self.__email_sender, self.__email_password)
                server.send_message(msg)
            print(f"📧 E-mail enviado com sucesso para {destinatario}!")
        except smtplib.SMTPException as e:
            print(f"Erro ao enviar e-mail SMTP: {e}")
        except Exception as e:
            print(f"Erro inesperado ao enviar e-mail: {e}")


class IngressoManager(EmailManager):
    def __init__(self):
        super().__init__(SMTP_SERVER, SMTP_PORT, EMAIL_SENDER, EMAIL_PASSWORD)

    def gerar_ingresso(self, user, cinema, filme, cadeiras, horario_filme):
        """
        Gera o ingresso em formato QR Code e envia para o usuário.
        Espera-se que 'user' seja um objeto com método get_email().
        """
        if not user or not cinema or not filme or not cadeiras or not horario_filme:
            raise ValueError("Todos os campos são obrigatórios para gerar o ingresso.")

        email = user.get_email() if hasattr(user, "get_email") else getattr(user, "email", None)
        if not email:
            raise ValueError("Usuário inválido: e-mail não encontrado.")

        codigo_ingresso = str(uuid.uuid4())[:8]
        detalhes = (
            f"Ingresso: {codigo_ingresso}\n"
            f"Cinema: {cinema}\n"
            f"Filme: {filme}\n"
            f"Cadeira(s): {', '.join(cadeiras)}\n"
            f"Horário do Filme: {horario_filme}"
        )

        # Gerar QR Code
        os.makedirs("ingressos", exist_ok=True)
        qr_path = f"ingressos/{codigo_ingresso}.png"
        qrcode.make(detalhes).save(qr_path)

        # Enviar e-mail
        self.enviar_email(
            destinatario=email,
            assunto="Seu ingresso de cinema",
            corpo=f"Olá!\n\nAqui está o seu ingresso:\n\n{detalhes}\n\nApresente o QR Code na entrada do cinema.",
            anexo_path=qr_path
        )

        print(f"Ingresso gerado e enviado para {email}! Código: {codigo_ingresso}")

        return {
            "id": codigo_ingresso,
            "Cinema": cinema,
            "Filme": filme,
            "Cadeiras": cadeiras,
            "Horario_filme": horario_filme,
            "QR Code": qr_path
        }
