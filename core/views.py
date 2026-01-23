# from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
from .models import Session, Document
import requests
from functools import wraps
import jwt
from django.conf import settings

#imports pra funcionar o crud de sessões e documentos - 👆👆ADICIONADO ACIMA 
#from django.shortcuts import get_object_or_404
#from .models import Session, Document

API_REGISTRO = "https://usuarioapi-production.up.railway.app/api/registro/"
API_LOGIN = "https://usuarioapi-production.up.railway.app/api/login/"



###################################CRUD DE Usuario#####################################
def login_view(request):
    if request.method == "POST":
        payload = {
            "email": request.POST["email"],
            "password": request.POST["password"],
        }

        response = requests.post(API_LOGIN, json=payload)

        if response.status_code == 200:
            data = response.json()

            access = data["access"]

            # decodifica o JWT
            decoded = jwt.decode(
                access,
                options={"verify_signature": False}
            )

            user_id = decoded["user_id"]

            # busca os dados do usuário
            user_response = requests.get(
                f"https://usuarioapi-production.up.railway.app/api/usuarios/{user_id}/",
                headers={
                    "Authorization": f"Bearer {access}"
                }
            )

            if user_response.status_code == 200:
                user_data = user_response.json()

                request.session["username"] = user_data["username"]
                request.session["email"] = user_data["email"]
            else:
                request.session["username"] = "Usuário"

            # salva tokens e id
            request.session["access_token"] = access
            request.session["refresh_token"] = data["refresh"]
            request.session["user_id"] = user_id

            return redirect("home")

        return render(request, "login.html", {
            "error": "Email ou senha inválidos"
        })

    return render(request, "login.html")


def cadastro_view(request):
    if request.method == "POST":
        payload = {
            "username": request.POST["username"],
            "email": request.POST["email"],
            "password": request.POST["password"],
        }

        response = requests.post(API_REGISTRO, json=payload)

        if response.status_code == 201:
            return redirect("login")

        return render(request, "cadastro.html", {
            "error": response.json()
        })
    return render(request, 'cadastro.html')


def jwt_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("access_token"):
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return wrapper

@jwt_required
def perfil_usuario(request):
    user_id = request.session["user_id"]
    access = request.session["access_token"]

    response = requests.get(
        f"https://usuarioapi-production.up.railway.app/api/usuarios/{user_id}/",
        headers={
            "Authorization": f"Bearer {access}"
        }
    )

    if response.status_code != 200:
        return render(request, "perfil.html", {
            "error": "Não foi possível carregar os dados do usuário"
        })

    user = response.json()

    return render(request, "perfil.html", {
        "user": user
    })

@jwt_required
def atualizar_usuario(request):
    user_id = request.session["user_id"]
    access = request.session["access_token"]

    if request.method == "POST":
        payload = {
            "username": request.POST.get("username"),
            "email": request.POST.get("email"),
        }

        response = requests.put(
            f"https://usuarioapi-production.up.railway.app/api/usuarios/{user_id}/",
            json=payload,
            headers={
                "Authorization": f"Bearer {access}"
            }
        )

        if response.status_code == 200:
            data = response.json()

            # Atualiza dados salvos na sessão (importante)
            request.session["username"] = data["username"]
            request.session["email"] = data["email"]

            return redirect("perfil")

        return render(request, "perfil.html", {
            "error": "Erro ao atualizar os dados",
            "user": payload
        })

    return redirect("perfil")

@jwt_required
def excluir_usuario(request):
    if request.method != "POST":
        return redirect("perfil")

    user_id = request.session.get("user_id")
    access = request.session.get("access_token")

    response = requests.delete(
        f"https://usuarioapi-production.up.railway.app/api/usuarios/{user_id}/",
        headers={
            "Authorization": f"Bearer {access}"
        }
    )

    if response.status_code == 204:
        # remove tudo da sessão
        request.session.flush()
        return redirect("login")

    return render(request, "perfil.html", {
        "error": "Não foi possível excluir a conta. Tente novamente."
    })


def logout_view(request):
    request.session.flush()
    return redirect("login")

###################################Pagina inicial#####################################



@jwt_required
def home(request):
    user_id = request.session["user_id"]
    sessions = Session.objects.filter(owner_id=user_id)
    return render(request, 'home.html', {'sessions': sessions})


###################################CRUD DE SSESSÕES#####################################

# CRIAR SESSÃO #
@jwt_required
def create_session(request):
    if request.method == 'POST':
        title = request.POST.get('title')

        if title:
            Session.objects.create(
                title=title,
                owner_id=request.session["user_id"]
            )

        return redirect('home')

    return render(request, 'create_session.html')


# EDITAR SESSÃO #
@jwt_required
def edit_session(request, session_id):
    session = get_object_or_404(Session, id=session_id, owner_id=request.session["user_id"])

    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            session.title = title
            session.save()
        return redirect('home')

    return render(request, 'edit_session.html', {'session': session})

# DELETAR SESSÃO #
@jwt_required
def delete_session(request, session_id):
    session = get_object_or_404(Session, id=session_id, owner_id=request.session["user_id"])
    session.delete()
    return redirect('home')

# DETALHES DA SESSÃO #
@jwt_required
def session_detail(request, session_id):
    session = get_object_or_404(Session, id=session_id, owner_id=request.session["user_id"])
    documents = session.documents.all()

    return render(
        request,
        'session_detail.html',
        {
            'session': session,
            'documents': documents
        }
    )

###################################CRUD DE DOCUMENTOS#####################################

# CRIAR DOCUMENTO #
@jwt_required
def create_document(request, session_id):
    session = get_object_or_404(Session, id=session_id, owner_id=request.session["user_id"])

    if request.method == 'POST':
        Document.objects.create(
            session=session,
            owner_id=request.session["user_id"],
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            file=request.FILES.get('file')
        )
        return redirect('session_detail', session_id=session.id)

    return render(request, 'create_document.html', {'session': session})

# EDITAR DOCUMENTO #
@jwt_required
def edit_document(request, document_id):
    document = get_object_or_404(Document, id=document_id, owner_id=request.session["user_id"])

    if request.method == 'POST':
        document.title = request.POST.get('title')
        document.description = request.POST.get('description')
        document.save()

        return redirect('session_detail', session_id=document.session.id)

    return render(request, 'edit_document.html', {'document': document})

# DELETAR DOCUMENTO #
@jwt_required
def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id, owner_id=request.session["user_id"])
    session_id = document.session.id
    document.delete()
    return redirect('session_detail', session_id=session_id)
