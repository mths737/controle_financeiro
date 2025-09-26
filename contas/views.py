from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Case, When, Value, IntegerField
from django.contrib import messages
from datetime import date, datetime, timezone

from .forms import ContaForm
from .models import Conta
from .filters import ContaFilter


def get_contas_queryset():
    """Query otimizada das contas."""
    return Conta.objects.select_related('cliente', 'categoria')


def ordenar_contas(queryset, order_by, order_direction):
    """Aplica ordenação nas contas."""
    today = date.today()

    if order_by == "status":
        queryset = queryset.annotate(
            status_order=Case(
                When(data_pagamento__isnull=False, then=Value(1)),  # Pago
                When(data_vencimento__lt=today, then=Value(3)),     # Atrasado
                default=Value(2),                                   # Pendente
                output_field=IntegerField(),
            )
        )
        field = "status_order"
    else:
        order_fields_map = {
            "tipo": "tipo",
            "cliente": "cliente__nome",
            "categoria": "categoria__nome",
            "valor": "valor",
            "data_vencimento": "data_vencimento",
            "data_pagamento": "data_pagamento",
        }
        field = order_fields_map.get(order_by, "data_vencimento")

    return queryset.order_by(field if order_direction == "cre" else f"-{field}")

def marcar_como_pago(request, pk):
    """
    Marca a conta como paga usando a data enviada em POST (YYYY-MM-DD).
    Se não for enviada data_pagamento, usa a data atual (timezone.localdate()).
    Método: POST. Retorna para a listagem de contas.
    """
    conta = get_object_or_404(Conta, pk=pk)

    if request.method != "POST":
        return redirect('contas:conta_list')

    data_str = request.POST.get('data_pagamento', '').strip()

    # Se vier vazio -> marca com a data de hoje
    if data_str == '':
        conta.data_pagamento = timezone.localdate()
        conta.save()
        messages.success(request, "Conta marcada como paga (data: hoje).")
        return redirect('contas:conta_list')

    # Se vier preenchido -> tenta parsear YYYY-MM-DD
    try:
        parsed = datetime.strptime(data_str, '%Y-%m-%d').date()
    except ValueError:
        messages.error(request, "Formato de data inválido. Use AAAA-MM-DD.")
        return redirect('contas:conta_list')

    conta.data_pagamento = parsed
    conta.save()
    messages.success(request, f"Conta marcada como paga (data: {parsed.strftime('%d/%m/%Y')}).")
    return redirect('contas:conta_list')


def conta_list(request):
    contas_qs = get_contas_queryset()

    # 🔹 GET → listagem com filtro
    if request.method == "GET":
        conta_filter = ContaFilter(request.GET, queryset=contas_qs)
        form = ContaForm()
        form.fields.pop('data_pagamento', None)
        
        return render(request, "contas/conta_list.html", {
            "contas": conta_filter.qs,
            "form": form,
            "filter": conta_filter,
            'advanced_filter': True,
        })

    # 🔹 POST → decide ação
    action = request.POST.get("btn") or request.POST.get("type") or request.POST.get("btn_order")

    # Ordenação
    if request.POST.get("btn_order"):
        btn_order = request.POST.get("btn_order")
        current_order = request.POST.get("order", "cre")
        current_order_by = request.POST.get("order_by")

        new_order = "dec" if btn_order == current_order_by and current_order == "cre" else "cre"
        contas_qs = ordenar_contas(contas_qs, btn_order, new_order)
        conta_filter = ContaFilter(request.GET, queryset=contas_qs)
        form = ContaForm()
        

        return render(request, "contas/conta_list.html", {
            "contas": contas_qs,
            "form": form,
            "filter": conta_filter,
            "order_by": btn_order,
            "order": new_order,
            'advanced_filter': True,
        })

    # Editar
    if action == "edit":
        conta = get_object_or_404(Conta, pk=request.POST["id"])
        form = ContaForm(instance=conta)
        if not conta.data_pagamento:
            form.fields.pop('data_pagamento', None)
        conta_filter = ContaFilter(request.GET, queryset=contas_qs)
        return render(request, "contas/conta_list.html", {
            "contas": conta_filter.qs,
            "form": form,
            "alt": True,
            "id": conta.id,
            "filter": conta_filter,
            'advanced_filter': True,
        })

    # Excluir (confirmação)
    if action == "delete":
        conta_filter = ContaFilter(request.GET, queryset=contas_qs)
        return render(request, "contas/conta_list.html", {
            "contas": conta_filter.qs,
            "delete": True,
            "id": request.POST["id"],
            "filter": conta_filter,
            'advanced_filter': True,
        })

    # Salvar edição
    if action == "alt":
        conta = get_object_or_404(Conta, pk=request.POST.get("id"))
        form = ContaForm(request.POST, instance=conta)
        #form.Meta.exclude.append['data_pagamento']

        if form.is_valid():
            form.save()
            messages.success(request, "Conta alterada com sucesso!")
            return redirect("contas:conta_list")

    # Criar
    if action == "save":
        form = ContaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Conta cadastrada com sucesso!")
            return redirect("contas:conta_list")

    # Confirmar exclusão
    if action == "delete_confirm":
        conta = get_object_or_404(Conta, pk=request.POST["id"])
        conta.delete()
        messages.success(request, "Conta excluída com sucesso!")
        return redirect("contas:conta_list")