from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User # banco de dados de usuários
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth

# Create your views here.
def cadastro(request):
    #print(request.META)
    #return HttpResponse('Vasco da Gama')
    if request.method == "GET":
        return render(request, 'cadastro.html')
    
    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        # Verificações de senha
        if senha != confirmar_senha:
            messages.add_message(request,constants.ERROR, 'Senhas devem ser iguais')
            return redirect('/usuarios/cadastro')
        
        if len(senha) < 6:
            messages.add_message(request, constants.ERROR, 'A senha deve possuir pelo menos 6 caracteres')
            return redirect('/usuarios/cadastro')
        
        # Verificar se ja existe usuário com mesmo nome
        users = User.objects.filter(username=username)
        print(users.exists())

        if users.exists():
            messages.add_message(request,constants.ERROR, 'Já existe nome de usuário')
            return redirect('/usuarios/cadastro')

        # Criação de usuários no banco de dados de usuários
        user = User.objects.create_user(
            username=username,
            email=email,
            password=senha
        )

        return redirect('/usuarios/login')
    
# criação da view de login
def login_view(request):
    if request.method == "GET":
        return render(request,'login.html')
    
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = auth.authenticate(request, username=username, password = senha) # Autentificação

        if user:
            # Liberar acesso
            auth.login(request, user)
            return redirect('/pacientes/home') # Vai para pagina de login
        
        messages.add_message(request,constants.ERROR,"Usuário ou senha inválido")
        return redirect('/usuarios/login')
            
# criação do logout

def sair(request):    
    auth.logout(request)    
    return redirect('/usuarios/login')
