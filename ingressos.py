import os
import smtplib
import uuid
import qrcode
from email.message import EmailMessage



SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "icinema.ufal@gmail.com" 
EMAIL_PASSWORD = "bfvj iotl rcaj ixgk"


if not EMAIL_SENDER or not EMAIL_PASSWORD:
    raise ValueError(
        "Credenciais de e-mail não encontradas. "
        "Verifique se as variáveis de ambiente EMAIL_SENDER e EMAIL_PASSWORD estão configuradas."
    )

class EmailManager:
    
    def __init__(self, smtp_server, smtp_port, email_sender, email_password):
        
        self.__smtp_server = smtp_server
        self.__smtp_port = smtp_port
        self.__email_sender = email_sender
        self.__email_password = email_password
# Função que envia email
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
            print("E-mail enviado com sucesso!")
        except smtplib.SMTPException as e:
            print(f"Erro ao enviar e-mail: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")

class IngressoManager(EmailManager):
   
    def __init__(self):
        
        super().__init__(SMTP_SERVER, SMTP_PORT, EMAIL_SENDER, EMAIL_PASSWORD)
# Gera o qrcode do ingresso
    def gerar_ingresso(self, user, cinema, filme, cadeiras, horario_filme):
        
        if not user or not cinema or not filme or not cadeiras or not horario_filme:
            raise ValueError("Todos os campos são obrigatórios.")

        email = user.get_email()
        codigo_ingresso = str(uuid.uuid4())[:8]
        detalhes_ingresso = (
            f"Ingresso: {codigo_ingresso}\n"
            f"Cinema: {cinema}\n"
            f"Filme: {filme}\n"
            f"Cadeira(s): {', '.join(cadeiras)}\n"
            f"Horário do Filme: {horario_filme}"
        )

        qr = qrcode.make(detalhes_ingresso)
        os.makedirs("ingressos", exist_ok=True)
        qr_path = f"ingressos/{codigo_ingresso}.png"
        qr.save(qr_path)

        ingresso = {
            "id": codigo_ingresso,
            "Cinema": cinema,
            "Filme": filme,
            "Cadeiras": cadeiras,
            "Horario_filme": horario_filme,
            "QR Code": qr_path
        }

        self.enviar_email(
            email,
            "Seu ingresso de cinema",
            f"Olá!\n\nAqui está o seu ingresso:\n\n{detalhes_ingresso}\n\nApresente o QR Code na entrada do cinema.",
            qr_path
        )

        print(f"Ingresso gerado e enviado para {email}! Código: {codigo_ingresso}")
        return ingresso
