import logging
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from facade.sistema_facade import SistemaFacade

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="umasecretmuitosegura123")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

sistema = SistemaFacade()

# Home
@app.get("/")
def home(request: Request):
    email = request.session.get("user_email")
    user = sistema.obter_usuario(email) if email else None
    return templates.TemplateResponse("home.html", {"request": request, "user": user})


# Autenticação
@app.get("/login")
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(request: Request, email: str = Form(...), password: str = Form(...)):
    user = sistema.login(email, password)
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
    sucesso, msg = sistema.criar_conta(nome, email, senha)
    if sucesso:
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse("cadastro.html", {"request": request, "erro": msg})


# Menu
@app.get("/menu")
def menu(request: Request):
    if not request.session.get("user_email"):
        return RedirectResponse(url="/login", status_code=302)
    return templates.TemplateResponse("menu.html", {"request": request})


# Reserva de cinema
@app.get("/cinemas")
def escolher_cinema(request: Request):
    email = request.session.get("user_email")
    if not email:
        return RedirectResponse(url="/login", status_code=302)
    user = sistema.obter_usuario(email)
    cinemas = sistema.listar_cinemas(user)
    return templates.TemplateResponse("cinema_escolher.html", {"request": request, "cinemas": cinemas})

@app.post("/cinemas/filmes")
def escolher_filme(request: Request, cinema: str = Form(...)):
    email = request.session.get("user_email")
    user = sistema.obter_usuario(email)
    filmes = sistema.listar_filmes(user, cinema)
    return templates.TemplateResponse("cinema_filmes.html", {"request": request, "cinema": cinema, "filmes": filmes})

@app.post("/cinemas/horarios")
def escolher_horario(request: Request, cinema: str = Form(...), filme: str = Form(...)):
    email = request.session.get("user_email")
    user = sistema.obter_usuario(email)
    horarios = sistema.listar_horarios(user, cinema, filme)
    return templates.TemplateResponse("cinema_horarios.html", {"request": request, "cinema": cinema, "filme": filme, "horarios": horarios})

@app.post("/cinemas/assentos")
def escolher_assentos(request: Request, cinema: str = Form(...), filme: str = Form(...), horario: str = Form(...)):
    email = request.session.get("user_email")
    user = sistema.obter_usuario(email)
    assentos = sistema.listar_assentos(user, cinema, filme)
    return templates.TemplateResponse("cinema_assentos.html", {
        "request": request, "cinema": cinema, "filme": filme, "horario": horario, "assentos": assentos
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
    user = sistema.obter_usuario(email)
    sucesso, mensagem = sistema.reservar(user, cinema, filme, horario, assento, cupom, metodo)
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

    user = sistema.obter_usuario(email)
    msg = ""

    if acao == "ver":
        return templates.TemplateResponse("perfil.html", {"request": request, "dados": user, "email": email})
    elif acao == "senha":
        msg = sistema.alterar_senha(email, nova_senha)
    elif acao == "historico":
        return templates.TemplateResponse("perfil.html", {"request": request, "historico": user.history, "email": email})
    elif acao == "cancelar":
        user.remove_history_by_code(cancelar)
        sistema.obter_usuario(email)  # Reatualizar (se precisar salvar)
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
    sistema.avaliar(email, filme, nota, comentario)
    return templates.TemplateResponse("resumo.html", {"request": request, "mensagem": "Obrigado pela sua avaliação!"})


# Ver avaliações
@app.get("/reviews")
def ver_reviews(request: Request, filme: str = ""):
    if filme:
        avaliacoes = sistema.listar_reviews(filme)
        return templates.TemplateResponse("reviews.html", {"request": request, "filme": filme, "avaliacoes": avaliacoes})
    return templates.TemplateResponse("reviews_buscar.html", {"request": request})
