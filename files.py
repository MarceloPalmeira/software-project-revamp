import json


class FileManager:
    def __init__(self, file_path):
        self.file_path = file_path
# Carrega arquivos .json
    def load(self):   
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Arquivo {self.file_path} não encontrado.")
            return {}
       
# Salva arquivos .json
    def save(self, data):
        
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar o arquivo {self.file_path}: {e}")
