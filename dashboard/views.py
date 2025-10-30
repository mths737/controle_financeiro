# views.py (ex: app dashboard ou contas)
from datetime import timedelta, date
from django.shortcuts import render
from django.db.models import Sum, Q
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import json

from contas.models import Conta  # ajuste o import se o app tiver outro nome
# from .models import Conta  # se a view estiver no mesmo app


@login_required()
def dashboard_view(request):
    """
    Dashboard que usa o modelo Conta.
    GET param: periodo (dias) - default 30
    """

    # período em dias (string vindo do select)
    periodo = request.GET.get("periodo", "30")
    try:
        dias = int(periodo)
    except ValueError:
        dias = 30
        periodo = "30"

    hoje = timezone.localdate()  # data atual
    inicio = hoje - timedelta(days=dias-1)  # inclui hoje (ex: dias=30 -> 30 dias incluindo hoje)
    # período anterior de mesmo tamanho
    inicio_anterior = inicio - timedelta(days=dias)
    fim_anterior = inicio - timedelta(days=1)

    # queryset base no período atual
    contas_periodo = Conta.objects.select_related('cliente', 'categoria').filter(
        data_vencimento__range=(inicio, hoje)
    )

    # totais atuais
    total_entrada = contas_periodo.filter(tipo='R', data_pagamento__isnull=False).aggregate(total=Sum('valor'))['total'] or 0
    total_saida = contas_periodo.filter(tipo='P', data_pagamento__isnull=False).aggregate(total=Sum('valor'))['total'] or 0
    saldo = total_entrada - total_saida

    # período anterior
    contas_anteriores = Conta.objects.filter(data_vencimento__range=(inicio_anterior, fim_anterior))
    entrada_ant = contas_anteriores.filter(tipo='R').aggregate(total=Sum('valor'))['total'] or 0
    saida_ant = contas_anteriores.filter(tipo='P').aggregate(total=Sum('valor'))['total'] or 0
    saldo_ant = entrada_ant - saida_ant

    # função para calcular variação percentual (retorna float)
    def variacao(atual, anterior):
        if anterior == 0:
            if atual == 0:
                return 0.0
            return 100.0
        return ((float(atual) - float(anterior)) / float(anterior)) * 100.0

    entrada_variacao = variacao(total_entrada, entrada_ant)
    saida_variacao = variacao(total_saida, saida_ant)
    saldo_variacao = variacao(saldo, saldo_ant)

    # === Dados para o gráfico: série diária para o período selecionado ===
    labels = []
    entradas_por_dia = []
    saidas_por_dia = []

    for i in range(dias):
        dia = inicio + timedelta(days=i)
        labels.append(dia.strftime("%d/%m"))  # rótulo curto dd/mm

        soma_entradas = Conta.objects.filter(
            tipo='R', data_vencimento=dia
        ).aggregate(total=Sum('valor'))['total'] or 0

        soma_saidas = Conta.objects.filter(
            tipo='P', data_vencimento=dia
        ).aggregate(total=Sum('valor'))['total'] or 0

        entradas_por_dia.append(float(soma_entradas))
        saidas_por_dia.append(float(soma_saidas))

    # jsons para o template (Chart.js)
    labels_json = json.dumps(labels)
    entradas_json = json.dumps(entradas_por_dia)
    saidas_json = json.dumps(saidas_por_dia)

    # Top categorias (soma total no período, independente de tipo)
    top_qs = contas_periodo.values('categoria__nome').annotate(total=Sum('valor')).order_by('-total')[:6]
    # normalizar nome de categoria para fallback quando nulo
    top_categories = [
        {
            "categoria": item['categoria__nome'] or "Sem categoria",
            "total": item['total'] or 0
        }
        for item in top_qs
    ]

    # lançamentos recentes (ordena por vencimento decrescente e pega os 12 primeiros)
    recentes = contas_periodo.order_by('-data_vencimento')[:12]

    context = {
        "periodo": periodo,
        "total_entrada": total_entrada,
        "total_saida": total_saida,
        "saldo": saldo,
        "entrada_variacao": entrada_variacao,
        "saida_variacao": saida_variacao,
        "saldo_variacao": saldo_variacao,
        "labels_json": labels_json,
        "entradas_json": entradas_json,
        "saidas_json": saidas_json,
        "top_categories": top_categories,
        "recentes": recentes,
        "dashboard":True,
    }

    return render(request, "dashboard/dashboard.html", context)