from managers.auth_manager import AuthManager
from managers.cinema_manager import CinemaManager
from managers.review_manager import ReviewManager
from models.review import ReviewNota


class SistemaFacade:
    def __init__(self):
        self.__auth = AuthManager()
        self.__reviews = ReviewManager()

    def login(self, email, senha):
        return self.__auth.login(email, senha)

    def criar_conta(self, nome, email, senha):
        return self.__auth.create_account(nome, email, senha)

    def alterar_senha(self, email, nova_senha):
        return self.__auth.update_password(email, nova_senha)

    def obter_usuario(self, email):
        return self.__auth.get_account(email)

    def reservar(self, user, cinema, filme, horario, assento, cupom, metodo):
        cinema_mgr = CinemaManager(user)
        return cinema_mgr.reservar_assento(cinema, filme, horario, assento, cupom, metodo)

    def listar_cinemas(self, user):
        return CinemaManager(user).listar_cinemas()

    def listar_filmes(self, user, cinema):
        return CinemaManager(user).listar_filmes(cinema)

    def listar_horarios(self, user, cinema, filme):
        return CinemaManager(user).listar_horarios(cinema, filme)

    def listar_assentos(self, user, cinema, filme):
        return CinemaManager(user).listar_assentos(cinema, filme)

    def avaliar(self, email, filme, nota, comentario):
        review = ReviewNota(email, filme, comentario, nota)
        self.__reviews.submit(review)

    def listar_reviews(self, filme):
        return self.__reviews.listar(filme)
