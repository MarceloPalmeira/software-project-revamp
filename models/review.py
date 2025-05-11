from abc import ABC, abstractmethod

class ReviewBase(ABC):
    def __init__(self, usuario: str, filme: str):
        self.usuario = usuario
        self.filme = filme

    @abstractmethod
    def to_dict(self) -> dict:
        pass


class ReviewTexto(ReviewBase):
    def __init__(self, usuario: str, filme: str, texto: str):
        super().__init__(usuario, filme)
        self.texto = texto

    def to_dict(self):
        return {
            "usuario": self.usuario,
            "review": self.texto
        }


class ReviewNota(ReviewTexto):
    def __init__(self, usuario: str, filme: str, texto: str, nota: float):
        super().__init__(usuario, filme, texto)
        self.nota = round(nota, 1)

    def to_dict(self):
        data = super().to_dict()
        data["rating"] = self.nota
        return data


class ReviewTag(ReviewNota):
    def __init__(self, usuario: str, filme: str, texto: str, nota: float, tags: list[str]):
        super().__init__(usuario, filme, texto, nota)
        self.tags = tags

    def to_dict(self):
        data = super().to_dict()
        data["tags"] = self.tags
        return data
