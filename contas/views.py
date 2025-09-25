from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Case, When, Value, IntegerField
from django.contrib import messages

from .forms import ContaForm
from .models import Conta
from .filters import ContaFilter

import locale
    
def get_contas():
    contas = Conta.objects.select_related('cliente', 'categoria')
    today = date.today()
    for conta in contas:
        if conta.data_pagamento:
            conta.status_calc = 'Pago'
        elif conta.data_vencimento < today:
            conta.status_calc = 'Atrasado'
        else:
            conta.status_calc = 'Pendente'
    return contas

def conta_list(request):
    if request.method == 'GET':
        form = ContaForm()
        contas = get_contas().order_by("data_vencimento")        
        conta_filter = ContaFilter(request.GET, queryset=contas)
        for conta in contas:
            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
            conta.valor = locale.currency(conta.valor, grouping=True, symbol="R$")
        return render(request, 'contas/conta_list.html', {'contas': contas, 'form': form, 'filter': conta_filter})
    else:
        if request.POST.get("btn_order"):
            btn_order = request.POST.get("btn_order")
            current_order_by = request.POST.get("order_by")
            current_order = request.POST.get("order", "cre")

            contas_qs = Conta.objects.select_related('cliente', 'categoria').all()

            # toggle da direção (cre -> dec -> cre)
            if btn_order == current_order_by:
                new_order = "dec" if current_order == "cre" else "cre"
            else:
                new_order = "cre"

            if btn_order == "status":
                today = date.today()
                contas_qs = contas_qs.annotate(
                    status_order=Case(
                        When(data_pagamento__isnull=False, then=Value(1)),   # Pago
                        When(data_vencimento__lt=today, then=Value(3)),     # Atrasado
                        default=Value(2),                                   # Pendente
                        output_field=IntegerField(),
                    )
                )
                order_field = "status_order"
            else:
                # mapeia nomes amigáveis para campos do banco
                order_fields_map = {
                    "tipo": "tipo",
                    "cliente": "cliente__nome",
                    "categoria": "categoria__nome",
                    "valor": "valor",
                    "data_vencimento": "data_vencimento",
                    "data_pagamento": "data_pagamento",
                }
                order_field = order_fields_map.get(btn_order, "data_vencimento")

            if new_order == "cre":
                contas = contas_qs.order_by(order_field)
            else:
                contas = contas_qs.order_by(f"-{order_field}")

            conta_filter = ContaFilter(request.GET, queryset=contas)
            form = ContaForm()

            for conta in contas:
                locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
                conta.valor = locale.currency(conta.valor, grouping=True, symbol="R$")

            return render(request, 'contas/conta_list.html', {
                'contas': contas,
                'form': form,
                'filter': conta_filter,
                'order_by': btn_order,
                'order': new_order,
            })
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
            
                return render(request, 'contas/conta_list.html', {'contas': contas, 'form': form, 'alt': True, "id":id, 'filter': conta_filter})
            elif request.POST.get("btn") == "delete":
                contas = Conta.objects.select_related('cliente', 'categoria')
                conta_filter = ContaFilter(request.GET, queryset=contas)
                for conta in contas:
                    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
                    conta.valor = locale.currency(conta.valor, grouping=True, symbol="R$")
                return render(request, 'contas/conta_list.html', {'contas': contas, 'delete': True, 'id': id, 'filter': conta_filter})
                
        else:
            if request.POST['type'] == "alt":
                contas = Conta.objects.select_related('cliente', 'categoria')
                conta_filter = ContaFilter(request.GET, queryset=contas)
                id = request.POST.get("id")  # vem do input hidden no form
                try:
                    conta = Conta.objects.get(pk=id)  # busca conta existente
                except Conta.DoesNotExist:
                    conta = None  # se não existir, pode criar

                form = ContaForm(request.POST, instance=conta)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Conta alterada com sucesso!")
                    return render(request, 'contas/conta_list.html', {'contas': contas, 'filter': conta_filter})

            elif request.POST['type'] == "save":
                form = ContaForm(request.POST)

                if form.is_valid():
                    form.save()
                    messages.success(request, "Conta cadastrada com sucesso!")
                    return redirect('contas:conta_list')
            elif request.POST['type'] == "delete":
                id = request.POST["id"]
                conta = Conta.objects.get(pk=id)
                conta.delete()
                messages.success(request, "Conta excluida com sucesso!")
                
                contas = Conta.objects.select_related('cliente', 'categoria')
                return redirect('contas:conta_list')


def marcar_como_pago(request, pk):
    conta = get_object_or_404(Conta, pk=pk)
    if request.method == 'POST':
        data_pagamento = request.POST.get('data_pagamento')
        if data_pagamento:
            conta.data_pagamento = data_pagamento
            conta.save()
    return redirect('contas:conta_list')  # ajuste para o nome da sua URL de listagem