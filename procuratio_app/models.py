from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.db import models
from django.contrib.auth.models import AbstractUser, User, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin,UserManager

sexe = (
    ("H","Homme"),
    ("F","Femme"),
)

class UManager(BaseUserManager):

    def create_superuser(self, username, password, email, **other_fields):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            is_superuser=True,
            is_staff=True,
        )
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **other_fields):
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class Utilisateur(AbstractUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    first_name = None
    last_name = None
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
        null=True
    )
    password = models.CharField(_('password'), max_length=128, null=True)
    image_profil = models.ImageField(null=True, default="default_img.webp", upload_to='profil_photo/', blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        ),
    )

    USERNAME_FIELD = 'username'

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to. A user will get all permissions '
                    'granted to each of their groups.'),
        related_name='utilisateur_groups'  # Added related_name to avoid clashes
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='utilisateur_permissions'  # Added related_name to avoid clashes
    )

    objects = UManager()

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'Utilisateurs'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def get_photo_url(self):
        if self.image_profil and hasattr(self.image_profil, 'url'):
            return self.image_profil.url
        else:
            return "/static/img/default_img.webp"


class Client(Utilisateur):
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    sexe = models.CharField(max_length=30, choices=sexe)
    adresse = models.CharField(max_length=100, blank=True)
    code_postal = models.CharField(blank=True, max_length=10, null=True)
    num_tel = models.CharField(max_length=30, blank=True)
    code_fidelite = models.CharField(max_length=150,blank=True,null=True,default='')
    fidelitycount = models.IntegerField(blank=True,null=True,default=0)
    fidelity=models.BooleanField(blank=False,null=True,default=False)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'Clients'


class ClientSession(models.Model):
    session_key = models.CharField(max_length=40, primary_key=True,blank=True)
    client = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    session_start = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'client_sessions'


type_produit = (
    ("shampoing", "shampoing"),
    ("peigne", "peigne"),
    ("miroir", "miroir"),
)

type_service = (
    ("coupe", "coupe"),
    ("rasage barbe", "rasage barbe"),
    ("couleur cheveux", "couleur cheveux"),
)

class Produit(models.Model):
    nom = models.CharField(max_length=150)
    marque = models.CharField(max_length=150, blank=True)
    type = models.CharField(max_length=30,choices=type_produit)
    photo = models.ImageField(null=True, upload_to='produit/', blank=True)
    qte = models.IntegerField()
    prix = models.FloatField()

    class Meta:
        db_table = 'Produits'

    def __str__(self):
        return self.nom

class Service(models.Model):
    nom = models.CharField(max_length=150)
    type = models.CharField(max_length=30,choices=type_service)
    photo = models.ImageField(null=True, upload_to='service/', blank=True)
    prix = models.FloatField()

    class Meta:
        db_table = 'Services'

    def __str__(self):
        return self.nom

type_paiement = (
    ('carte-bancaire', 'Carte bancaire'),
    ('especes', 'Espèces'),
)

class Transaction(models.Model):
    id_client = models.ForeignKey(Client,on_delete=models.CASCADE)
    produits_list = models.JSONField(blank=True, null=True)
    #services_list = models.ManyToManyField(Service,blank=True)
    dateT = models.DateTimeField(auto_now_add=True, blank=True)
    MT = models.FloatField()
    MP = models.CharField(max_length=150,choices=type_paiement)

    class Meta:
        db_table = 'Transaction'


class HistoriqueA(models.Model):
    id_client = models.ForeignKey(Client,on_delete=models.CASCADE)
    id_transaction = models.ForeignKey(Transaction,on_delete=models.CASCADE)

class RendezVous(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateTimeField(blank=True,null=True)
    client = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    reservation_date = models.DateTimeField(auto_now_add=True,null=True)


    class Meta:
        db_table = 'RendezVous'

    def __str__(self):
        return f"{self.service} - {self.date_disponible} - {self.client}"

"""
class User():
    username = models.CharField(max_length=150,unique=True,null=True)
    password = models.CharField(max_length=128, null=True)
    email = models.CharField(max_length=150)


class Admin(User):
    nom = models.CharField(max_length=150)
    prenom = models.CharField(max_length=150)


class Client(User):
    nom = models.CharField(max_length=150)
    prenom = models.CharField(max_length=150)
    adresse = models.CharField(max_length=150)


class Produit():
    nom = models.CharField(max_length=150)
    qte = models.IntegerField()
    prix = models.FloatField()

type_service = (
    ("Bronze", "Bronze"),
    ("Silver", "Silver"),
)

class Service():
    nom = models.CharField(max_length=150)
    type = models.CharField(max_length=30,choices=type_service)
    prix = models.FloatField()

class Transaction():
    id_client = models.ForeignKey(Client,on_delete=models.CASCADE)
    produits_list = models.ManyToManyField(Produit)
    services_list = models.ManyToManyField(Service)
    dateT = models.DateTimeField(auto_now_add=True, blank=True)
    MT = models.FloatField()
    MP = models.CharField(max_length=150)

class CampagnePub():
    message = models.CharField(max_length=200)

class RendezVous():
    date = models.DateTimeField()

class HistoriqueA():
    MT = models.FloatField()
"""