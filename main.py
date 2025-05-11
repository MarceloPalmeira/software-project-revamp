import logging
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from managers.auth_manager import AuthManager
from managers.cinema_manager import CinemaManager
from managers.review_manager import ReviewManager
from models.review import ReviewNota

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="umasecretmuitosegura123")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Home
@app.get("/")
def home(request: Request):
    email = request.session.get("user_email")
    user = AuthManager().get_account(email) if email else None
    return templates.TemplateResponse("home.html", {"request": request, "user": user})


# Autenticação
@app.get("/login")
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(request: Request, email: str = Form(...), password: str = Form(...)):
    auth = AuthManager()
    user = auth.login(email, password)
    if user:
        request.session["user_email"] = email
        return RedirectResponse(url="/menu", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request, "error": "Credenciais inválidas."})

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=302)


@app.get("/cadastro")
def cadastro_form(request: Request):
    return templates.TemplateResponse("cadastro.html", {"request": request})

@app.post("/cadastro")
def cadastro(request: Request, nome: str = Form(...), email: str = Form(...), senha: str = Form(...)):
    auth = AuthManager()
    sucesso, msg = auth.create_account(nome, email, senha)
    if sucesso:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse("cadastro.html", {"request": request, "erro": msg})


# Menu
@app.get("/menu")
def menu(request: Request):
    email = request.session.get("user_email")
    if not email:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse("menu.html", {"request": request})


# Reserva de cinema
@app.get("/cinemas")
def escolher_cinema(request: Request):
    email = request.session.get("user_email")
    if not email:
        return RedirectResponse(url="/login", status_code=302)
    user = AuthManager().get_account(email)
    cinema_mgr = CinemaManager(user)
    return templates.TemplateResponse("cinema_escolher.html", {
        "request": request,
        "cinemas": cinema_mgr.listar_cinemas()
    })

@app.post("/cinemas/filmes")
def escolher_filme(request: Request, cinema: str = Form(...)):
    email = request.session.get("user_email")
    user = AuthManager().get_account(email)
    cinema_mgr = CinemaManager(user)
    filmes = cinema_mgr.listar_filmes(cinema)
    return templates.TemplateResponse("cinema_filmes.html", {
        "request": request, "cinema": cinema, "filmes": filmes
    })

@app.post("/cinemas/horarios")
def escolher_horario(request: Request, cinema: str = Form(...), filme: str = Form(...)):
    email = request.session.get("user_email")
    user = AuthManager().get_account(email)
    cinema_mgr = CinemaManager(user)
    horarios = cinema_mgr.listar_horarios(cinema, filme)
    return templates.TemplateResponse("cinema_horarios.html", {
        "request": request, "cinema": cinema, "filme": filme, "horarios": horarios
    })

@app.post("/cinemas/assentos")
def escolher_assentos(request: Request, cinema: str = Form(...), filme: str = Form(...), horario: str = Form(...)):
    email = request.session.get("user_email")
    user = AuthManager().get_account(email)
    cinema_mgr = CinemaManager(user)
    assentos = cinema_mgr.listar_assentos(cinema, filme)
    return templates.TemplateResponse("cinema_assentos.html", {
        "request": request, "cinema": cinema, "filme": filme, "horario": horario,
        "assentos": assentos
    })

@app.post("/cinemas/pagamento")
def finalizar_reserva(
    request: Request,
    cinema: str = Form(...),
    filme: str = Form(...),
    horario: str = Form(...),
    assento: str = Form(...),
    cupom: str = Form(""),
    metodo: str = Form(...)
):
    email = request.session.get("user_email")
    user = AuthManager().get_account(email)
    cinema_mgr = CinemaManager(user)
    sucesso, mensagem = cinema_mgr.reservar_assento(cinema, filme, horario, assento, cupom, metodo)
    return templates.TemplateResponse("resumo.html", {"request": request, "mensagem": mensagem})


# Perfil
@app.get("/perfil")
def ver_perfil(request: Request):
    email = request.session.get("user_email")
    if not email:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse("perfil.html", {"request": request, "email": email})

@app.post("/perfil")
def perfil_acao(
    request: Request,
    acao: str = Form(...),
    nova_senha: str = Form(""),
    cancelar: str = Form("")
):
    email = request.session.get("user_email")
    if not email:
        return RedirectResponse(url="/login", status_code=302)

    auth = AuthManager()
    user = auth.get_account(email)
    msg = ""
    if acao == "ver":
        return templates.TemplateResponse("perfil.html", {"request": request, "dados": user, "email": email})
    elif acao == "senha":
        msg = auth.update_password(email, nova_senha)
    elif acao == "historico":
        return templates.TemplateResponse("perfil.html", {"request": request, "historico": user.history, "email": email})
    elif acao == "cancelar":
        user.remove_history_by_code(cancelar)
        auth.update_history(user)
        msg = "Reserva cancelada com sucesso."
    return templates.TemplateResponse("perfil.html", {"request": request, "msg": msg, "email": email})


# Avaliação
@app.get("/avaliar")
def avaliar_form(request: Request):
    return templates.TemplateResponse("avaliar.html", {"request": request})

@app.post("/avaliar")
def avaliar(request: Request, filme: str = Form(...), nota: float = Form(...), comentario: str = Form(...)):
    email = request.session.get("user_email")
    if not email:
        return RedirectResponse(url="/login", status_code=302)
    review_mgr = ReviewManager()
    review = ReviewNota(usuario=email, filme=filme, texto=comentario, nota=nota)
    review_mgr.submit(review)
    return templates.TemplateResponse("resumo.html", {"request": request, "mensagem": "Obrigado pela sua avaliação!"})


# Ver avaliações
@app.get("/reviews")
def ver_reviews(request: Request, filme: str = ""):
    review_mgr = ReviewManager()
    if filme:
        avaliacoes = review_mgr.listar(filme)
        return templates.TemplateResponse("reviews.html", {"request": request, "filme": filme, "avaliacoes": avaliacoes})
    return templates.TemplateResponse("reviews_buscar.html", {"request": request})
