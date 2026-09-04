from django.db import models

# Create your models here.
class ContaBancaria(models.Model):
    TIPO_CHOICES = [
        ('BANCO', 'Conta Bancária'),
        ('CAIXA', 'Caixa Físico (Dinheiro em Espécie)'),
    ]

    nome = models.CharField(max_length=100, verbose_name="Nome da Conta")
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='BANCO', verbose_name="Tipo de Conta")
    saldo_inicial = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Saldo Inicial")

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"