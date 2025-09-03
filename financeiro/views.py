from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.utils import timezone
from django.utils.formats import localize
from django.db.models.functions import TruncMonth

from datetime import date
from decimal import Decimal
from collections import defaultdict

from .forms import ClienteForm, CategoriaForm, ContaForm
from .models import Cliente, Categoria, Conta

import json
import locale

def home(request):
    return render(request, 'financeiro/base.html')

def cliente_list(request):
    if request.method == 'GET':
        form = ClienteForm()
        clientes = Cliente.objects.all()
        return render(request, 'financeiro/cliente_list.html', {'clientes': clientes, 'form': form})
    else:
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cliente_list')


def categoria_list(request):
    if request.method == 'GET':
        form = CategoriaForm()
        categorias = Categoria.objects.all()
        return render(request, 'financeiro/categoria_list.html', {'categorias': categorias, 'form': form})
    else:
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categoria_list')


def conta_list(request):
    if request.method == 'GET':
        form = ContaForm()
        contas = Conta.objects.select_related('cliente', 'categoria')
        for conta in contas:
            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
            conta.valor = locale.currency(conta.valor, grouping=True, symbol="R$")
        return render(request, 'financeiro/conta_list.html', {'contas': contas, 'form': form})
    else:
        if request.POST.get("btn"):
            id = request.POST["id"]
            if request.POST.get("btn") == "edit":
                conta = Conta.objects.get(pk=id)
                form = ContaForm(instance=conta)
                contas = Conta.objects.select_related('cliente', 'categoria')
            
                return render(request, 'financeiro/conta_list.html', {'contas': contas, 'form': form, 'alt_conta': True, "id":id})
            elif request.POST.get("btn") == "delete":
                contas = Conta.objects.select_related('cliente', 'categoria')
                return render(request, 'financeiro/conta_list.html', {'contas': contas, 'delete_conta': True, 'id': id})
        else:
            if request.POST['type'] == "alt_conta":
                id = request.POST.get("id")  # vem do input hidden no form
                conta = Conta.objects.get(pk=id)

                form = ContaForm(request.POST, instance=conta)
                if form.is_valid():
                    form.save()
                    return redirect('conta_list')

            elif request.POST['type'] == "save_conta":
                form = ContaForm(request.POST)

                if form.is_valid():
                    form.save()
                    return redirect('conta_list')
            elif request.POST['type'] == "delete_conta":
                id = request.POST["id"]
                conta = Conta.objects.get(pk=id)
                conta.delete()
                
                contas = Conta.objects.select_related('cliente', 'categoria')
                return redirect('conta_list')


def marcar_como_pago(request, pk):
    conta = get_object_or_404(Conta, pk=pk)
    if request.method == 'POST':
        data_pagamento = request.POST.get('data_pagamento')
        if data_pagamento:
            conta.data_pagamento = data_pagamento
            conta.save()
    return redirect('conta_list')  # ajuste para o nome da sua URL de listagem

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
    return render(request, 'financeiro/dashboard.html', context)