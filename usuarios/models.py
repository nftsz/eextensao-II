from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Sessao do Admin: Cadastros
class UsuarioManager(BaseUserManager):
    def create_user(self, cpf, nome, password=None, **extra_fields):
        if not cpf:
            raise ValueError('O CPF é obrigatório')
        user = self.model(cpf=cpf, nome=nome, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cpf, nome, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(cpf, nome, password, **extra_fields)


# Sessao da UBS: UBS solicitante da OCI
class UBS(models.Model):
    nome = models.CharField(max_length=150, unique=True)
    codigo = models.CharField(max_length=20, unique=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    regional = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.nome} ({self.codigo})"
    
    class Meta:
        verbose_name_plural = "UBS"

# Sessao do Usuario: Cadastro dos usuarios do sistema (Gestor da UBS por ex)
class Usuario(AbstractBaseUser, PermissionsMixin):
    cpf = models.CharField(max_length=11, unique=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True, default='Não informado')
    sobrenome = models.CharField(max_length=100, blank=True, null=True)
    ubs = models.ForeignKey(UBS, on_delete=models.SET_NULL, null=True, blank=True)
    cargo = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['nome', 'sobrenome', 'email']

    objects = UsuarioManager()

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"
    

# Sessao dos Medicos: Profisiional Executante da OCI
class ProfissionalExecutante(models.Model):
    nome = models.CharField(max_length=100)
    especialidade = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.nome} ({self.especialidade})" if self.especialidade else self.nome
    
    class Meta:
        verbose_name = "Medico"

