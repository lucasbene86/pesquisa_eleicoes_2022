from django.db import models
from django.db.models.fields import DecimalField

# Create your models here.
class ConferenciaVotos(models.Model):
    cpf_user = models.CharField('CPF', max_length=14)
    conferir_voto = models.IntegerField('Voto')

class Voto(models.Model):
    voto_lula = models.IntegerField('Voto lula')
    voto_bolsonaro = models.IntegerField('Voto bolsonaro')
    voto_ciro_gomes = models.IntegerField('Voto ciro gomes')
    voto_mandeta = models.IntegerField('Voto mandeta')
    voto_joao_doria = models.IntegerField('Voto joao foria')
    voto_branco = models.IntegerField('Voto branco')
    voto_nao_sabe = models.IntegerField('Voto não sabe')
