import calendar
import secrets
import string
from  datetime import datetime,timedelta

from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
import json

from django.contrib.sessions.models import Session
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from procuratio_app.decorators import unauthenticated_user,admin_only
from .forms import *
from django.http import HttpResponse, JsonResponse


@unauthenticated_user
def home(request):
    return render(request, 'index.html')


def login_register(request):
    return render(request, 'login_register/login.html')


def logoutU(request):
    logout(request)
    return redirect('loginA')

@admin_only
def adminboard(request):
    stock = Produit.objects.aggregate(Sum('qte')) or 0
    total_stock = stock['qte__sum'] if 'qte__sum' in stock else 0

    total_reservations = RendezVous.objects.count()
    total_transactions = Transaction.objects.count()
    total_revenue = Transaction.objects.aggregate(Sum('MT'))['MT__sum'] or 0

    revenue_by_day = Transaction.objects.annotate(day=TruncDate('dateT')).values('day').annotate(
        total_revenue=Sum('MT')).order_by('day')

    transactions_by_day = Transaction.objects.annotate(day=TruncDate('dateT')).values('day').annotate(
        total_transactions=Count('id')).order_by('day')

    reservations_by_day = RendezVous.objects.annotate(day=TruncDate('reservation_date')).values('day').annotate(
        total_reservations=Count('id')).order_by('day')

    sessions_by_day = ClientSession.objects.annotate(day=TruncDate('session_start')).values('day').annotate(
        total_sessions=Count('session_key')).order_by('day')

    context = {
        'total_stock':total_stock,
        'total_reservations':total_reservations,
        'total_transactions':total_transactions,
        'total_revenue':total_revenue,
        'transactions_by_day': transactions_by_day,
        'revenue_by_day': revenue_by_day,
        'reservations_by_day': reservations_by_day,
        'clients_by_day': sessions_by_day,
    }
    return render(request, 'dashboard_admin/pages/stats.html',context)

@unauthenticated_user
def productlist(request):
    produits = Produit.objects.all()
    context = {
        'produits':produits,
    }
    return render(request, 'dashboard_admin/pages/produits_p.html',context=context)

@unauthenticated_user
def servicelist(request):
    services = Service.objects.all()
    context = {
        'services': services,
    }
    return render(request, 'dashboard_admin/pages/services_p.html',context=context)

@unauthenticated_user
def reservationlist(request):
    reservations = RendezVous.objects.all()
    context = {
        'reservations': reservations,
    }
    return render(request, 'dashboard_admin/pages/reservations_p.html',context)

@unauthenticated_user
def clientlist(request):
    clients = Client.objects.all()
    context = {
        'clients': clients,
    }
    return render(request, 'dashboard_admin/pages/clients_p.html',context=context)


@unauthenticated_user
def produitlclient(request):
    produits = Produit.objects.all()
    context = {
        'produits': produits,
    }
    return render(request, 'dashboard_client/listproduits.html',context=context)

@unauthenticated_user
def servicesclient(request):
    services = Service.objects.all()
    context = {
        'services': services,
    }
    return render(request, 'dashboard_client/listservices.html',context=context)




def loginU(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            session_key = request.session.session_key

            if isinstance(user, Utilisateur):
                ClientSession.objects.get_or_create(session_key=session_key,client=user)
            if user.is_staff:
                return redirect('Adminboard')
            else:
                return redirect('index')
        else:
            error_message = 'Nom d\'utilisateur ou mot de passe incorrecte'
            messages.error(request, error_message)

    return render(request, "login_register/login.html",{'error_message': error_message})


def registerC(request):
    saved = False
    formClient = ClientForm(request.POST)

    if request.method == 'POST':

        if formClient.is_valid():
            register = formClient.save()
            user_group = Group.objects.get(id=2)
            register.groups.add(user_group)
            saved = True
            return redirect('loginA')
        else:
            formClient = ClientForm()
        if saved:
            messages.info(request, 'Votre compte a été creer avec succée ! Connectez-vous maintenant')

    context = {
        'formClient': formClient,
    }

    return render(request, 'login_register/register.html', context)

@unauthenticated_user
def profil_user(request):
    member = Utilisateur.objects.get(username=request.user.username)
    if request.method == 'POST':
        userForm = UserForm(request.POST, request.FILES, instance=member)
        if userForm.is_valid():

            userForm.save()
            messages.info(request, 'Profil Modifié avec succée !')

        else:
            messages.error(request, 'Une erreur est survenu !')

        response = {
            'data_is_valid': True
        }
        return JsonResponse(response)


    else:
        userForm = UserForm(instance=member)

        context = {
            'userForm': userForm
        }
        return render(request, 'dashboard_client/profile.html', context)


def resetPassword(request):
    if request.method == 'POST':
        formPassword = PasswordChangeCustomForm(request.user, request.POST)

        if formPassword.is_valid():
            user = formPassword.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Votre mot de passe a été bien changer')
            return redirect('logout')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci dessous')
    formPassword = PasswordChangeCustomForm(request.user)
    context = {
        'formPassword': formPassword,
    }
    return render(request, 'dashboard_client/reset_password.html', context)

def prendre_rendezvous(request, service_id):
    service = Service.objects.get(id=service_id)

    # Récupérez la date actuelle
    datenow = datetime.today()

    # Incrémentez la date actuelle de 14 jours pour obtenir une période de deux semaines
    end_date = datenow + timedelta(days=14)

    # Générez les dates pour la période spécifiée
    dates_disponibles = [(datenow + timedelta(days=i)).strftime('%Y-%m-%d') for i in range((end_date - datenow).days + 1)]

    # Récupérez les réservations existantes pour le service
    reservations_existantes = RendezVous.objects.all()

    # Filtrer les dates disponibles en fonction des réservations existantes
    dates_disponibles = [date for date in dates_disponibles if not reservations_existantes.filter(date=date)]

    context = {
        'dates_disponibles': dates_disponibles,
        'service': service
    }

    return render(request, "dashboard_client/rendez_vous.html", context)

def create_reservation(request):
    if request.method == 'POST':
        selected_date = request.POST.get('selected-date')
        service_name = request.POST.get('service-name')
        client = request.user
        service = Service.objects.get(nom=service_name)

        RendezVous.objects.create(client=client, service=service,date=selected_date)

    return redirect("user_reservations")

def listreservations(request):

    reservations = RendezVous.objects.filter(client=request.user)


    return render(request, 'dashboard_client/listreservations.html', {'reservations': reservations})

""" ============================== PARTIE CRUD ============================== """

def ajouterproduit(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('productlist')
    else:
        form = ProduitForm()

    return render(request, 'dashboard_admin/pages/produitCRUD/ajouterp.html', {'form': form})


def modifierproduit(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)

    if request.method == 'POST':
        form = ProduitForm(request.POST, instance=produit)
        if form.is_valid():
            form.save()
            return redirect('productlist')
    else:
        form = ProduitForm(instance=produit)

    return render(request, 'dashboard_admin/pages/produitCRUD/modifierp.html', {'form': form, 'produit': produit})


def supprimerproduit(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)

    if request.method == 'POST':
        produit.delete()
        return redirect('productlist')

    return render(request, 'dashboard_admin/pages/produitCRUD/supprimerp.html', {'produit': produit})


def ajouterservice(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('servicelist')
    else:
        form = ServiceForm()

    return render(request, 'dashboard_admin/pages/serviceCRUD/ajouters.html', {'form': form})


def modifierservice(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    if request.method == 'POST':
        form = ProduitForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('servicelist')
    else:
        form = ProduitForm(instance=service)

    return render(request, 'dashboard_admin/pages/serviceCRUD/modifiers.html', {'form': form, 'service': service})


def supprimerservice(request, service_id):
    service = get_object_or_404(Produit, id=service_id)

    if request.method == 'POST':
        service.delete()
        return redirect('servicelist')

    return render(request, 'dashboard_admin/pages/serviceCRUD/supprimers.html', {'service': service})

""" ============================== PARTIE ARTICLES ============================== """

def articlepage(request,article_id):
    if article_id == 1:
        return render(request,"dashboard_client/articles/article1.html")
    elif article_id == 2:
        return render(request,"dashboard_client/articles/article2.html")
    elif article_id == 3:
        return render(request, "dashboard_client/articles/article3.html")


""" ============================== PARTIE PANIER ============================== """
def add_to_cart(request):
    cart_p = {}
    cart_p[str(request.GET['id'])] = {
        'qty': request.GET['qty'],
        'image': request.GET['image'],
        'title': request.GET['title'],
        'price': request.GET['price'],
    }
    print(cart_p)
    if 'cartdata' in request.session:
        if str(request.GET['id']) in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_p[str(request.GET['id'])]['qty'])
            cart_data[str(request.GET['id'])]['price'] = float(cart_p[str(request.GET['id'])]['price'])
            cart_data.update(cart_data)
            request.session['cartdata'] = cart_data
        else:
            cart_data = request.session['cartdata']
            cart_data.update(cart_p)
            request.session['cartdata'] = cart_data
    else:
        request.session['cartdata'] = cart_p
    return JsonResponse({'data': request.session['cartdata'], 'totalitems': len(request.session['cartdata'])})


def view_cart(request):
    total_amt=0
    user_id = request.user.id
    client = get_object_or_404(Client, id=user_id)

    try:
        for p_id,item in request.session['cartdata'].items():
            total_amt+=int(item['qty'])*float(item['price'])
        if client.fidelity and check_valid_fidelity_code(user_id,client.code_fidelite):
            redu = float(total_amt * 0.3)
            total_amt -= redu

        context = {
                'items':request.session['cartdata'],
                'totalitems':len(request.session['cartdata']),
                'total_amt':total_amt,
                'fidelity_bool':client.fidelity,
            }

        return render(request, 'dashboard_client/panier/panierlist.html',context)
    except KeyError:
        return render(request, 'dashboard_client/panier/panierlist.html',{'total_amt':total_amt,'totalitems':0})


def delete_cart_item(request):
    p_id=str(request.GET['id'])
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data=request.session['cartdata']
            del request.session['cartdata'][p_id]
            request.session['cartdata']=cart_data
    total_amt=0
    for p_id,item in request.session['cartdata'].items():
        total_amt+=int(item['qty'])*float(item['price'])
    t=render_to_string('dashboard_client/panier/panierlist.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
    return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})


def update_cart_item(request):
    p_id=str(request.GET['id'])
    p_qty=request.GET['qty']
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data=request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty']=p_qty
            request.session['cartdata']=cart_data
    total_amt=0
    for p_id,item in request.session['cartdata'].items():
        total_amt+=int(item['qty'])*float(item['price'])
    t=render_to_string('dashboard_client/panier/panierlist.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
    return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})


def fidelity_update(request):
    fidelity_code = request.GET['fidelity_code']
    user_id = request.user.id
    client = get_object_or_404(Client, id=user_id)

    total_amt=0
    if fidelity_code and check_valid_fidelity_code(user_id,fidelity_code):
        # Apply the 30% discount if the fidelity code is valid
        messages.success(request, 'Fidelity code appliqué, vous bénéficiez de -30%')
        client.fidelity = 1
        client.save()
    else:
        messages.error(request, 'Fidelity code déja utilisé ou erroné, veuillez réssayez!')


    t = render_to_string('dashboard_client/panier/panierlist.html',
                         {'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']),
                          'total_amt': total_amt})
    return JsonResponse({'data': t, 'totalitems': len(request.session['cartdata'])})


def check_valid_fidelity_code(user_id,fidelity_code):
    user_id = user_id
    client = get_object_or_404(Client, id=user_id)

    if client.code_fidelite == fidelity_code:
        return True
    return False

""" ============================== PARTIE TRANSACTION ============================== """

def generate_fidelity_code(length=10):
    characters = string.ascii_uppercase + string.digits
    fidelity_code = ''.join(secrets.choice(characters) for _ in range(length))
    return fidelity_code
def checkout(request):
    total_amt = 0
    if request.method == 'POST':
        user_id = request.user.id
        cart_data = request.session.get('cartdata', {})
        type_payment = request.POST.get('type-payment')
        total_amount = request.POST.get('total-amount')
        client_instance = get_object_or_404(Client, id=user_id)

        if int(float(total_amount)) >= 100 and client_instance.code_fidelite == '':
            fidelity_code = generate_fidelity_code()
            client = get_object_or_404(Client, id=user_id)
            client.code_fidelite = fidelity_code
            client.save()

        if client_instance.fidelity:
            client = get_object_or_404(Client, id=user_id)
            client.fidelity=0
            client.code_fidelite=''
            client.fidelitycount += 1
            client.save()

        produits_list = []
        for p_id, item in cart_data.items():
            produit_info = {
                'id': p_id,
                'image': item['image'],
                'title': item['title'],
                'qty': item['qty'],
                'price': item['price'],
            }
            produits_list.append(produit_info)
        produits_list_json = json.dumps(produits_list)

        transaction = Transaction(
            id_client=client_instance,
            produits_list=produits_list_json,
            MT=total_amount,
            MP=type_payment,
            dateT=datetime.now()
        )
        transaction.save()

        produits_list_data = json.loads(transaction.produits_list)


        HistoriqueA.objects.create(id_client=client_instance, id_transaction=transaction)

        messages.success(request, 'Transaction effectuée avec succès!')


        return render(request, 'dashboard_client/panier/validation_page.html', {'transaction': transaction,'produits': produits_list_data})
    else:

        try:

            cart_data = request.session.get('cartdata', {})
            user_id=request.user.id
            client=get_object_or_404(Client,id=user_id)
            for p_id, item in request.session['cartdata'].items():
                total_amt += int(item['qty']) * float(item['price'])
            if client.fidelity and check_valid_fidelity_code(user_id, client.code_fidelite):
                redu = float(total_amt * 0.3)
                total_amt-=redu

            context = {
                'items': request.session['cartdata'],
                'totalitems': len(cart_data),
                'total_amt': total_amt,
                'client': request.user,
                'fidelity':client.fidelity,
            }
            return render(request, 'dashboard_client/panier/checkout.html', context=context)

        except KeyError:
            context = {
                'errmssg': 'il y\'a une erreur dans votre commande, veuillez réssayer',
                'total_amt': total_amt,
                'totalitems': 0,

            }
            return render(request, 'dashboard_client/panier/panierlist.html', context=context)


def historiqueA(request):
    if request.user.is_staff:
        transactions = Transaction.objects.all()
        template_path = 'dashboard_admin/pages/transactions_p.html'
    else:
        user_id = request.user.id
        client_instance = get_object_or_404(Client, id=user_id)
        transactions = Transaction.objects.filter(id_client=client_instance)
        for transaction in transactions:
            print(transaction.produits_list)
        template_path = 'dashboard_client/hist_achat.html'

    context = {
        'transactions': transactions,
    }

    return render(request, template_path, context=context)


def fidelityprog(request):
    user_id = request.user.id
    client_instance = get_object_or_404(Client, id=user_id)
    fidelity_code = None

    if client_instance:
        fidelity_code = client_instance.code_fidelite
        fidelity_count = client_instance.fidelitycount
    context = {
        'fidelity_code': fidelity_code,
        'fidelity_count': fidelity_count
    }

    return render(request,'dashboard_client/fidelity.html',context=context)