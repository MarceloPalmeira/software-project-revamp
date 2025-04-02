
from files import FileManager

review_file=FileManager("review.json")
movies_options=review_file.load()

class Review:
    def __init__(self, number,user):
        self.number = number
        self.user=user
        
#Função para mostrar as reviews dos filmes 
    def show_reviews(self,menu):
        movie = list(movies_options['Movies'].keys())[self.number - 1]
        reviews = movies_options["Movies"].get(movie, [])
    
        if not reviews:
            print()
            print(f"Nenhuma avaliação encontrada para o filme {movie}.")
            print()
            menu(self.user)
            return
        else:
            print()
            print(f"Avaliações para o filme {movie}:")
            for i, review in enumerate(reviews, 1):
                print(f"Avaliações:")
                print(f"  Usuário: {review['usuario']}")
                print(f"  Review: {review['review']}")
                print(f"  Nota: {review['rating']}/10")
                print()
            menu(self.user)
            return  

# Função para mostrar filmes disponíveis para avaliação e fazer a avaliação 
    def options(self,menu):
        while True:
            try:
                if self.number in [1,2,3,4,5,6]:
                    movie = list(movies_options['Movies'].keys())[self.number - 1]
                    name_movie = movie
                    print()
                    review_text = input(f"Digite sua review sobre {name_movie}:\n=> ")
                    while True:
                        try:
                            rating = float(input("Qual sua nota de 0 a 10:\n=> "))
                            if 0 <= rating <= 10:
                                print("Obrigado pela sua avaliação!")
                                print() 
                                read_user=FileManager("users.json") 
                                user_aux=read_user.load()
                                
                                email=self.user.get_email()  
                                
                                movies_options["Movies"][name_movie].append({
                                    "usuario": user_aux[email]["name"],
                                    "review": review_text,
                                    "rating": round(rating,1)
                                })
                                
                                
                                review_file.save(movies_options)
                              
                                menu(self.user)
                                break
                                
                            else:
                                print("Por favor, digite uma nota entre 0 e 10.")
                        except ValueError:
                            print("Entrada inválida.") 
                    break      
                else:  
                    print("Opção inválida. Tente novamente.")
                    print()
                    
            except ValueError:
                print("Opção inválida. Tente novamente.")
        
