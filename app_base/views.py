from django import contrib
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.http import HttpResponseRedirect, request, HttpResponse
from .forms import CadastroForms
from django.contrib import messages
from django.contrib.auth.models import User

from .models import ConferenciaVotos, Voto
from .pacotes.porcentagem import porcentagem_votos  # Pacote de porcentagem dos votos


# Pagina de login
def login_usuario(request):
    botao = request.GET.get('Next')  # Identifica qual foi o botão que foi clicado no HTML #

    # Função dos botões de menu.
    if botao == 'btn_votar':
        return redirect('login_usuario')
    elif botao == 'btn_enquete':
        return redirect('index')
    elif botao == 'btn_candidatos':
        return redirect('index')

    # Cadastra o usuario no banco de dados
    if request.method == "POST":
        cpf = request.POST['cpf']  # Puxa os dados do input HTML #

        # Confere e adiciona na tabela de conferencia de usuario #
        user_existente = ConferenciaVotos.objects.all() # pega um atributo do objeto
        lista_cpf = []
        for i in user_existente.values():
            lista_cpf.append(i.get('cpf_user'))

        # Confere se já existe CPF cadastrado #
        if lista_cpf.count(cpf) == 1:
            print('Repetido')
        else:
            user_cpf = ConferenciaVotos(
                cpf_user = cpf,
                conferir_voto = 0)
            user_cpf.save()

            # Adiciona o usuario para autenticação #
            user = User.objects.create_user(cpf, '', '123456')
            user.is_staff = True
            user.save()


    # login na pagina
    if request.method == "POST":
        username = request.POST["cpf"]
        password = str('123456')
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            print('Logado')
            login(request, usuario)  # Loga no user do django
            return redirect('votar')
        else:
            form_login = AuthenticationForm()
    else:
        form_login = AuthenticationForm()
    return render(request, 'login.html', {'cpf': form_login})


def index(request):
    if request.GET.get('Next') == 'btn_votar':
        # faz o logout do user
        logout(request)
        return redirect('votar')


    votos_computados = Voto.objects.all()  # pega um atributo do objeto

    lista_votos_bolsonaro = []
    lista_votos_ciro_gomes = []
    lista_votos_joao_doria = []
    lista_votos_lula = []
    lista_votos_mandeta = []
    lista_votos_branco = []
    lista_votos_nao_sabe = []
    lista_total_votos = []

    try:
        for i in votos_computados.values():
            if i.get('voto_bolsonaro') == 1:
                lista_votos_bolsonaro.append(i.get('voto_bolsonaro'))

            if i.get('voto_ciro_gomes') == 1:
                lista_votos_ciro_gomes.append(i.get('voto_ciro_gomes'))
            
            if i.get('voto_joao_doria') == 1:
                lista_votos_joao_doria.append(i.get('voto_joao_doria'))

            if i.get('voto_lula') == 1:
                lista_votos_lula.append(i.get('voto_lula'))

            if i.get('voto_mandeta') == 1:
                lista_votos_mandeta.append(i.get('voto_mandeta'))

            if i.get('voto_branco') == 1:
                lista_votos_branco.append(i.get('voto_branco'))

            if i.get('voto_nao_sabe') == 1:
                lista_votos_nao_sabe.append(i.get('voto_nao_sabe'))

            lista_total_votos.append(i.get('voto_branco'))


        # c_1 = Bolsonaro
        # c_2 = Ciro Gomes
        # c_3 = João Doria
        # c_4 = Lula
        # c_5 = Mandeta
        # c_6 = Em branco
        # c_7 = Não sabe

        c_1 = len(lista_votos_bolsonaro)
        c_2 = len(lista_votos_ciro_gomes)
        c_3 = len(lista_votos_joao_doria)
        c_4 = len(lista_votos_lula)
        c_5 = len(lista_votos_mandeta)
        c_6 = len(lista_votos_branco)
        c_7 = len(lista_votos_nao_sabe)

        lista_porcentagem_pronta = porcentagem_votos(c_1, c_2, c_3, c_4, c_5, c_6, c_7)

        print(lista_porcentagem_pronta)

        porcentagem = {
            'bolsonaro':lista_porcentagem_pronta[0],
            'ciro':lista_porcentagem_pronta[1],
            'doria':lista_porcentagem_pronta[2],
            'lula':lista_porcentagem_pronta[3],
            'mandeta':lista_porcentagem_pronta[4],
            'branco':lista_porcentagem_pronta[5],
            'nao_sabe':lista_porcentagem_pronta[6],
            'total_votos':len(lista_total_votos),
        }

        return render(request, 'index.html', porcentagem)

    except:
        porcentagem = {
            'bolsonaro':'0',
            'ciro':'0',
            'doria':'0',
            'lula':'0',
            'mandeta':'0',
            'branco':'0',
            'nao_sabe':'0',
            'total_votos':'0',
        }

        return render(request, 'index.html', porcentagem)


@login_required(login_url='/login')
def votar(request):
    if request.GET.get('Next') == 'btn_votar':
        # faz o logout do user
        logout(request)
        return redirect('votar')

    def voto(c_1, c_2, c_3, c_4, c_5, c_branco, c_nao_sabe):
        votacao = Voto(
            voto_lula=c_4,
            voto_bolsonaro=c_1,
            voto_ciro_gomes=c_2,
            voto_mandeta=c_5,
            voto_joao_doria=c_3,
            voto_branco=c_branco,
            voto_nao_sabe=c_nao_sabe
        )  # Inserir na tabela #
        votacao.save()

    # Puxa os dados do usuario do banco de dados para saber se ja foi votado
    # cpf = ConferenciaVotos.objects.values('cpf_user', 'conferir_voto')[0]
    identificador_votos = list(ConferenciaVotos.objects.values_list('id', 'cpf_user','conferir_voto'))

    # Identificar se o usuario já votou com aquele CPF 
    for i in range(len(identificador_votos)):
        if str(request.user) == identificador_votos[i][1]:
            if identificador_votos[i][2] == 1:
                print('Já votou')
                logout(request)  # faz o logout do user #
                return redirect('index')  # Leva para a pagina das enquetes
            else:
                candidato = request.GET.get('Next')  # Identifica qual foi o botão que foi clicado no HTML #

                # Computa no banco de dados que o user já votou
                def computar_voto(id_user):
                    # Atualiza o banco de dados (Atributo conferir_voto de 0 para 1)
                    ConferenciaVotos.objects.filter(id=id_user).update(conferir_voto=1)
                
                # ID do usuario que está logado
                id_user = identificador_votos[i][0]

                if candidato == 'bolsonaro':
                    voto(1,0,0,0,0,0,0)
                    logout(request)  # faz o logout do user
                    computar_voto(id_user)
                    return redirect('index')

                elif candidato == 'ciro_gomes':
                    voto(0,1,0,0,0,0,0)
                    logout(request)
                    computar_voto(id_user)
                    return redirect('index')

                elif candidato == 'joao_doria':
                    voto(0,0,1,0,0,0,0)
                    logout(request)
                    computar_voto(id_user)
                    return redirect('index')

                elif candidato == 'lula':
                    voto(0,0,0,1,0,0,0)
                    logout(request)
                    computar_voto(id_user)
                    return redirect('index')

                elif candidato == 'mandeta':
                    voto(0,0,0,0,1,0,0)
                    logout(request)
                    computar_voto(id_user)
                    return redirect('index')

                elif candidato == 'branco':
                    voto(0,0,0,0,0,1,0)
                    logout(request)
                    computar_voto(id_user)
                    return redirect('index')

                elif candidato == 'nao_sabe':
                    voto(0,0,0,0,0,0,1)
                    logout(request)
                    computar_voto(id_user)
                    return redirect('index')
                
                elif candidato == 'outro_cpf':
                    logout(request)
                    return redirect('login_usuario')
        else:
            pass


    return render(request, 'votar.html')
