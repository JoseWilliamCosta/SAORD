from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Session, Document

#imports pra funcionar o crud de sessões e documentos - 👆👆ADICIONADO ACIMA 
#from django.shortcuts import get_object_or_404
#from .models import Session, Document

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # ou qualquer página inicial
        else:
            return render(request, 'login.html', {
                'error': 'Usuário ou senha inválidos'
            })

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    sessions = Session.objects.filter(owner=request.user)
    return render(request, 'home.html', {'sessions': sessions})


###################################CRUD DE SSESSÕES#####################################

# CRIAR SESSÃO #
@login_required
def create_session(request):
    if request.method == 'POST':
        title = request.POST.get('title')

        if title:
            Session.objects.create(
                title=title,
                owner=request.user
            )

        return redirect('home')

    return render(request, 'create_session.html')


# EDITAR SESSÃO #
@login_required
def edit_session(request, session_id):
    session = get_object_or_404(Session, id=session_id, owner=request.user)

    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            session.title = title
            session.save()
        return redirect('home')

    return render(request, 'edit_session.html', {'session': session})

# DELETAR SESSÃO #
@login_required
def delete_session(request, session_id):
    session = get_object_or_404(Session, id=session_id, owner=request.user)
    session.delete()
    return redirect('home')

# DETALHES DA SESSÃO #
@login_required
def session_detail(request, session_id):
    session = get_object_or_404(Session, id=session_id, owner=request.user)
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
@login_required
def create_document(request, session_id):
    session = get_object_or_404(Session, id=session_id, owner=request.user)

    if request.method == 'POST':
        Document.objects.create(
            session=session,
            owner=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            file=request.FILES.get('file')
        )
        return redirect('session_detail', session_id=session.id)

    return render(request, 'create_document.html', {'session': session})

# EDITAR DOCUMENTO #
@login_required
def edit_document(request, document_id):
    document = get_object_or_404(Document, id=document_id, owner=request.user)

    if request.method == 'POST':
        document.title = request.POST.get('title')
        document.description = request.POST.get('description')
        document.save()

        return redirect('session_detail', session_id=document.session.id)

    return render(request, 'edit_document.html', {'document': document})

# DELETAR DOCUMENTO #
@login_required
def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id, owner=request.user)
    session_id = document.session.id
    document.delete()
    return redirect('session_detail', session_id=session_id)
