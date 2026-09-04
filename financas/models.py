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

class Transacao(models.Model):
    TIPO_TRANSACAO = [
        ('ENTRADA', 'Entrada (Aposentadoria/Pensão)'),
        ('SAIDA', 'Saída (Despesa Comprovada)'),
        ('TRANSF_INTERNA', 'Transferência entre Contas'),
        ('SAQUE', 'Saque para Caixa Físico'),
        ('DEPOSITO', 'Depósito em Conta Bancária'),
        ('REEMBOLSO_CURADOR', 'Reembolso ao Curador'),
    ]

    data = models.DateField(verbose_name="Data da Transação")
    tipo = models.CharField(max_length=25, choices=TIPO_TRANSACAO, verbose_name="Tipo")
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor (R$)")
    
    # Relacionamentos de Contas
    conta_origem = models.ForeignKey(ContaBancaria, on_delete=models.PROTECT, null=True, blank=True, related_name='transacoes_saida', verbose_name="Conta de Origem")
    conta_destino = models.ForeignKey(ContaBancaria, on_delete=models.PROTECT, null=True, blank=True, related_name='transacoes_entrada', verbose_name="Conta de Destino")
    
    # Regra de Crédito do Curador
    pago_pelo_curador = models.BooleanField(default=False, verbose_name="Pago com recursos próprios do curador?")
    
    # Detalhes do Favorecido / Gasto
    favorecido_nome = models.CharField(max_length=150, blank=True, null=True, verbose_name="Nome do Prestador / Estabelecimento")
    favorecido_cpf_cnpj = models.CharField(max_length=20, blank=True, null=True, verbose_name="CPF/CNPJ")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição Detalhada")

    def __str__(self):
        return f"{self.data} - {self.get_tipo_display()} - R$ {self.valor}"