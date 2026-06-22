from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L’email est obligatoire.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # hash du mot de passe
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    type_utilisateur = models.CharField(max_length=10, choices=[('etudiant', 'Étudiant'), ('recruteur', 'Recruteur')])
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['type_utilisateur']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.pk} {self.email}"


class Recruteur(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    nom_entreprise = models.CharField(max_length=100)
    adresse_entreprise = models.CharField(max_length=255, null=True, blank=True)
    site_internet = models.URLField(max_length=255, null=True, blank=True)
    contact = models.CharField(max_length=100, null=True, blank=True)
    forme_legale = models.CharField(max_length=50, null=True, blank=True)
    langue = models.CharField(max_length=50, null=True, blank=True)
    secteur = models.CharField(max_length=100, null=True, blank=True)
    logo = models.CharField(max_length=255, default='assets/logo_entreprise.svg')

    def __str__(self):
        return self.nom_entreprise

class Etudiant(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    age = models.DateField(null=True, blank=True)
    sexe = models.CharField(max_length=255, null=True, blank=True)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    adresse = models.CharField(max_length=255, null=True, blank=True)
    niveau_etude = models.CharField(max_length=100, null=True, blank=True)
    specialiter = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"
