from django.shortcuts import render, redirect
from django.db.models import Sum
from django.utils import timezone
from django.db.models.functions import TruncMonth

from decimal import Decimal

from contas.models import Conta

import json


def dashboard(request):
    hoje = timezone.now().date()
    contas = Conta.objects.filter(data_vencimento__year=hoje.year)

    # Totais gerais
    total_entrada = contas.filter(tipo='R').aggregate(Sum('valor'))['valor__sum'] or 0
    total_saida = contas.filter(tipo='P').aggregate(Sum('valor'))['valor__sum'] or 0
    saldo = total_entrada - total_saida

    # Agrupamento por mês e tipo
    totais_mensais = contas.annotate(mes=TruncMonth('data_vencimento')).values('mes', 'tipo').annotate(total=Sum('valor')).order_by('mes')

    # Estrutura do resumo mensal
    resumo = []
    for item in totais_mensais:
        mes = item['mes'].strftime('%b/%y')
        entrada = item['total'] if item['tipo'] == 'R' else 0
        saida = item['total'] if item['tipo'] == 'P' else 0

        encontrado = next((r for r in resumo if r['mes'] == mes), None)
        if encontrado:
            if item['tipo'] == 'R':
                encontrado['entrada'] += entrada
            else:
                encontrado['saida'] += saida
        else:
            resumo.append({
                'mes': mes,
                'entrada': entrada,
                'saida': saida,
            })

    # Calcular saldo de cada mês
    for r in resumo:
        r['saldo'] = r['entrada'] - r['saida']

    labels = [r['mes'] for r in resumo]
    entradas = [float(r['entrada']) if isinstance(r['entrada'], Decimal) else r['entrada'] for r in resumo]
    saidas = [float(r['saida']) if isinstance(r['saida'], Decimal) else r['saida'] for r in resumo]

    context = {
        'total_entrada': float(total_entrada) if isinstance(total_entrada, Decimal) else total_entrada,
        'total_saida': float(total_saida) if isinstance(total_saida, Decimal) else total_saida,
        'saldo': float(saldo) if isinstance(saldo, Decimal) else saldo,
        'resumo_mensal': resumo,
        'labels_json': json.dumps(labels),
        'entradas_json': json.dumps(entradas),
        'saidas_json': json.dumps(saidas),
    }
    return render(request, 'dashboard/dashboard.html', context)




from django.shortcuts import render
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import datetime
import json
from decimal import Decimal

# ajuste o import caso sua app/model esteja em outro local
from contas.models import Conta


def dashboard_view(request):
    today = timezone.localdate()

    # queryset base (pode filtrar por usuário se houver multi-tenant)
    contas_qs = Conta.objects.select_related('cliente', 'categoria').all()

    # Totais gerais
    total_entrada = contas_qs.filter(tipo='R').aggregate(total=Sum('valor'))['total'] or 0
    total_saida = contas_qs.filter(tipo='P').aggregate(total=Sum('valor'))['total'] or 0
    saldo = (total_entrada or 0) - (total_saida or 0)

    # Resumo mensal (últimos 6 meses)
    meses_qs = contas_qs.annotate(mes=TruncMonth('data_vencimento')) \
                       .values('mes', 'tipo') \
                       .annotate(total=Sum('valor')) \
                       .order_by('mes')

    resumo = {}  # { 'Aug/25': {'entrada':0, 'saida':0}, ... }
    for item in meses_qs:
        if not item['mes']:
            continue
        mes_str = item['mes'].strftime('%b/%y')  # ex: Aug/25
        if mes_str not in resumo:
            resumo[mes_str] = {'entrada': 0, 'saida': 0}
        if item['tipo'] == 'R':
            resumo[mes_str]['entrada'] += item['total'] or 0
        else:
            resumo[mes_str]['saida'] += item['total'] or 0

    # garantir ordem dos últimos 6 meses mesmo se não houver dados
    labels = []
    entradas = []
    saidas = []
    # cria lista dos últimos 6 meses (maior -> menor)
    for i in range(5, -1, -1):
        m = (today.replace(day=1) - timezone.timedelta(days=1)).replace(day=1)  # fallback
    # melhor construir cronologicamente:
    months = []
    for i in range(5, -1, -1):
        dt = (today.replace(day=1) - timezone.timedelta(days=0)).replace(day=1)
        # calculo simples de mês-por-mês:
        year = today.year
        month = today.month - i
        while month <= 0:
            month += 12
            year -= 1
        months.append(datetime(year, month, 1))

    for dt in months:
        key = dt.strftime('%b/%y')
        labels.append(key)
        entradas.append(float(resumo.get(key, {}).get('entrada', 0) or 0))
        saidas.append(float(resumo.get(key, {}).get('saida', 0) or 0))

    # Top categorias (maiores despesas e receitas)
    top_cat = contas_qs.values('categoria__nome') \
                      .annotate(total=Sum('valor')) \
                      .order_by('-total')[:8]
    top_categories = [
        {'categoria': item['categoria__nome'] or 'Sem categoria', 'total': float(item['total'] or 0)}
        for item in top_cat
    ]

    # Últimos lançamentos (10)
    recentes_qs = contas_qs.order_by('-data_vencimento')[:10]
    recentes = [{
        'id': c.id,
        'tipo': c.get_tipo_display(),
        'cliente': str(c.cliente),
        'categoria': c.categoria.nome if c.categoria else '—',
        'valor': float(c.valor),
        'data_vencimento': c.data_vencimento,
        'data_pagamento': c.data_pagamento,
        'status': c.status
    } for c in recentes_qs]

    # JSON para o Chart.js (já convertendo Decimals)
    labels_json = json.dumps(labels)
    entradas_json = json.dumps(entradas)
    saidas_json = json.dumps(saidas)

    context = {
        'total_entrada': float(total_entrada or 0),
        'total_saida': float(total_saida or 0),
        'saldo': float(saldo or 0),
        'labels_json': labels_json,
        'entradas_json': entradas_json,
        'saidas_json': saidas_json,
        'top_categories': top_categories,
        'recentes': recentes,
    }
    return render(request, 'dashboard/dashboard2.html', context)

