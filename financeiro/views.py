from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.urls import reverse
from django.utils import timezone
from django.utils.formats import localize
from django.db.models.functions import TruncMonth

from datetime import date
from decimal import Decimal
from collections import defaultdict

from .forms import ClienteForm, CategoriaForm, ContaForm
from .models import Cliente, Categoria, Conta
from .filters import ContaFilter

import json
import locale

def home(request):
    return render(request, 'financeiro/base.html')

def formatar_documento(id):
    id = ''.join(filter(str.isdigit, id))
    
    if len(id) == 11:
        return f"{id[:3]}.{id[3:6]}.{id[6:9]}-{id[9:]}"
    elif len(id) == 14:
        return f"{id[:2]}.{id[2:5]}.{id[5:8]}/{id[8:12]}-{id[12:]}"
    else:
        return "Número inválido: precisa ter 11 dígitos (CPF) ou 14 dígitos (CNPJ)."

def formatar_telefone(numero: str) -> str:
    # Remove espaços e caracteres não numéricos
    numero = ''.join(filter(str.isdigit, numero))
    
    if len(numero) == 10:
        return f"({numero[:2]}) {numero[2:6]}-{numero[6:]}"
    elif len(numero) == 11:
        return f"({numero[:2]}) {numero[2:3]} {numero[3:7]}-{numero[7:]}"
    else:
        return "Número inválido: precisa ter 10 ou 11 dígitos."

def cliente_list(request):
    if request.method == 'GET':
        form = ClienteForm()
        clientes = Cliente.objects.all()
        for cliente in clientes:
            cliente.cpf_cnpj = formatar_documento(cliente.cpf_cnpj)
            cliente.telefone = formatar_telefone(cliente.telefone)
        return render(request, 'financeiro/cliente_list.html', {'clientes': clientes, 'form': form})
    else:
        if request.POST.get("btn"):
            id = request.POST["id"]
            if request.POST.get("btn") == "edit":
                cliente = Cliente.objects.get(pk=id)
                form = ClienteForm(instance=cliente)
                clientes = Cliente.objects.all()
                for cliente in clientes:
                    cliente.cpf_cnpj = formatar_documento(cliente.cpf_cnpj)
                    cliente.telefone = formatar_telefone(cliente.telefone)
                return render(request, 'financeiro/cliente_list.html', {'clientes': clientes, 'form': form, 'alt': True, "id":id})
            elif request.POST.get("btn") == "delete":
                clientes = Cliente.objects.all()
                for cliente in clientes:
                    cliente.cpf_cnpj = formatar_documento(cliente.cpf_cnpj)
                    cliente.telefone = formatar_telefone(cliente.telefone)
                return render(request, 'financeiro/cliente_list.html', {'clientes': clientes, 'delete': True, 'id': id})
        else:
            if request.POST['type'] == "alt":
                id = request.POST.get("id")  # vem do input hidden no form
                cliente = Cliente.objects.get(pk=id)

                form = ClienteForm(request.POST, instance=cliente)
                if form.is_valid():
                    form.save()
                    return redirect('cliente_list')

            elif request.POST['type'] == "save":
                form = ClienteForm(request.POST)

                if form.is_valid():
                    form.save()
                    return redirect('cliente_list')
            elif request.POST['type'] == "delete":
                id = request.POST["id"]
                cliente = Cliente.objects.get(pk=id)
                cliente.ativo = False
                cliente.save()
                
                clientes = Conta.objects.all()
                return redirect('cliente_list')
        """
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cliente_list')
        """


def categoria_list(request):
    if request.method == 'GET':
        form = CategoriaForm()
        categorias = Categoria.objects.all()
        return render(request, 'financeiro/categoria_list.html', {'categorias': categorias, 'form': form})
    else:
        if request.POST.get("btn"):
            id = request.POST["id"]
            if request.POST.get("btn") == "edit":
                categoria = Categoria.objects.get(pk=id)
                form = CategoriaForm(instance=categoria)
                categorias = Categoria.objects.all()
                return render(request, 'financeiro/categoria_list.html', {'categorias': categorias, 'form': form, 'alt': True, "id":id})
            elif request.POST.get("btn") == "delete":
                categorias = Categoria.objects.all()
                return render(request, 'financeiro/categoria_list.html', {'categorias': categorias, 'delete': True, 'id': id})
        else:
            if request.POST['type'] == "alt":
                id = request.POST.get("id")  # vem do input hidden no form
                categoria = Categoria.objects.get(pk=id)

                form = CategoriaForm(request.POST, instance=categoria)
                if form.is_valid():
                    form.save()
                    return redirect('categoria_list')

            elif request.POST['type'] == "save":
                form = CategoriaForm(request.POST)

                if form.is_valid():
                    form.save()
                    return redirect('categoria_list')
            elif request.POST['type'] == "delete":
                id = request.POST["id"]
                categoria = Categoria.objects.get(pk=id)
                
                categorias = Categoria.objects.all()
                return redirect('categoria_list')
        """form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categoria_list')"""


def conta_list(request):
    if request.method == 'GET':
        form = ContaForm()
        contas = Conta.objects.select_related('cliente', 'categoria').order_by("data_vencimento")
        conta_filter = ContaFilter(request.GET, queryset=contas)
        for conta in contas:
            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
            conta.valor = locale.currency(conta.valor, grouping=True, symbol="R$")
        return render(request, 'financeiro/conta_list.html', {'contas': contas, 'form': form, 'filter': conta_filter})
    else:
        if request.POST.get("btn_order"):
            order = "cre"
            contas = Conta.objects.select_related('cliente', 'categoria')
            if request.POST.get("btn_order") == request.POST.get("order_by"):

                if request.POST.get("order") == "dec":
                    contas = Conta.objects.select_related('cliente', 'categoria').order_by(request.POST.get("btn_order"))
                    order = "cre"
                elif request.POST.get("order") == "cre":
                    contas = Conta.objects.select_related('cliente', 'categoria').order_by(request.POST.get("btn_order")).reverse()
                    order = "dec"
            else:
                order = "cre"
                contas = Conta.objects.select_related('cliente', 'categoria').order_by(request.POST.get("btn_order"))
            
            conta_filter = ContaFilter(request.GET, queryset=contas)
            form = ContaForm()
            order_by = request.POST.get("btn_order")
            
            for conta in contas:
                locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
                conta.valor = locale.currency(conta.valor, grouping=True, symbol="R$")
        
            return render(request, 'financeiro/conta_list.html', {'contas': contas, 'form': form, 'filter': conta_filter, "order_by" : order_by, "order": order})
        elif request.POST.get("btn"):
            id = request.POST["id"]
            if request.POST.get("btn") == "edit":
                conta = Conta.objects.get(pk=id)
                form = ContaForm(instance=conta)
                contas = Conta.objects.select_related('cliente', 'categoria')
                conta_filter = ContaFilter(request.GET, queryset=contas)
                for conta in contas:
                    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
                    conta.valor = locale.currency(conta.valor, grouping=True, symbol="R$")
            
                return render(request, 'financeiro/conta_list.html', {'contas': contas, 'form': form, 'alt': True, "id":id, 'filter': conta_filter})
            elif request.POST.get("btn") == "delete":
                contas = Conta.objects.select_related('cliente', 'categoria')
                conta_filter = ContaFilter(request.GET, queryset=contas)
                for conta in contas:
                    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
                    conta.valor = locale.currency(conta.valor, grouping=True, symbol="R$")
                return render(request, 'financeiro/conta_list.html', {'contas': contas, 'delete': True, 'id': id, 'filter': conta_filter})
                
        else:
            if request.POST['type'] == "alt":
                id = request.POST.get("id")  # vem do input hidden no form
                try:
                    conta = Conta.objects.get(pk=id)  # busca conta existente
                except Conta.DoesNotExist:
                    conta = None  # se não existir, pode criar

                form = ContaForm(request.POST, instance=conta)
                if form.is_valid():
                    form.save()
                    return redirect('conta_list')

            elif request.POST['type'] == "save":
                form = ContaForm(request.POST)

                if form.is_valid():
                    form.save()
                    return redirect('conta_list')
            elif request.POST['type'] == "delete":
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