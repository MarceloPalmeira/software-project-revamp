from database.files import FileManager
from models.review import ReviewTexto, ReviewNota, ReviewTag

class ReviewManager:
    def __init__(self):
        self.__file = FileManager("review.json")
        self.__data = self.__file.load()

    def submit(self, review_obj):
        if "Movies" not in self.__data:
            self.__data["Movies"] = {}

        if review_obj.filme not in self.__data["Movies"]:
            self.__data["Movies"][review_obj.filme] = []

        self.__data["Movies"][review_obj.filme].append(review_obj.to_dict())
        self.__file.save(self.__data)

    def listar(self, filme: str) -> list[dict]:
        return self.__data.get("Movies", {}).get(filme, [])
