from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from clientes.filters import ClienteFilter
from .forms import ClienteForm
from .models import Cliente


def formatar_documento(id):
    id = ''.join(filter(str.isdigit, id))
    if len(id) == 11:
        return f"{id[:3]}.{id[3:6]}.{id[6:9]}-{id[9:]}"
    elif len(id) == 14:
        return f"{id[:2]}.{id[2:5]}.{id[5:8]}/{id[8:12]}-{id[12:]}"
    return id


def formatar_telefone(numero: str) -> str:
    numero = ''.join(filter(str.isdigit, numero))
    if len(numero) == 10:
        return f"({numero[:2]}) {numero[2:6]}-{numero[6:]}"
    elif len(numero) == 11:
        return f"({numero[:2]}) {numero[2:3]} {numero[3:7]}-{numero[7:]}"
    return numero


def ordenar_clientes(queryset, order_by, order_direction):
    """
    Aplica ordenação no queryset de Cliente.
    order_by: string vinda do botão (ex: "nome", "cpf_cnpj", "telefone", "email", "ativo")
    order_direction: "cre" (crescente) ou "dec" (decrescente)
    """
    order_fields_map = {
        "nome": "nome",
        "cpf_cnpj": "cpf_cnpj",
        "telefone": "telefone",
        "email": "email",
        "ativo": "ativo",
    }

    field = order_fields_map.get(order_by, "nome")
    return queryset.order_by(field if order_direction == "cre" else f"-{field}")


@login_required()
def cliente_list(request):
    clientes_qs = Cliente.objects.all()
    cliente_filter = ClienteFilter(request.GET, queryset=clientes_qs)

    # aplica formatação amigável em todos
    for cliente in cliente_filter.qs:
        cliente.cpf_cnpj = formatar_documento(cliente.cpf_cnpj)
        cliente.telefone = formatar_telefone(cliente.telefone)

    form = ClienteForm()

    # === GET ===
    if request.method == 'GET':
        return render(request, 'clientes/cliente_list.html', {
            'clientes': cliente_filter.qs,
            'form': form,
            'filter': cliente_filter,
        })

    # === POST ===
    btn = request.POST.get("btn")
    action_type = request.POST.get("type")
    btn_order = request.POST.get("btn_order")

    # --- ordenação ---
    if btn_order:
        btn_order = request.POST.get("btn_order")
        current_order = request.POST.get("order", "cre")

        # toggle igual ao padrão que você já usa
        new_order = "dec" if (btn_order == request.POST.get("order_by") and current_order == "cre") else "cre"

        clientes_qs = ordenar_clientes(clientes_qs, btn_order, new_order)
        cliente_filter = ClienteFilter(request.GET, queryset=clientes_qs)

        # então renderiza com o queryset ordenado
        return render(request, 'clientes/cliente_list.html', {
            'clientes': clientes_qs,
            'form': form,
            'filter': cliente_filter,
            'order_by': btn_order,
            'order': new_order,
        })

    # --- editar (abrir form preenchido) ---
    if btn == "edit":
        cliente = get_object_or_404(Cliente, pk=request.POST.get("id"))
        form = ClienteForm(instance=cliente)
        return render(request, 'clientes/cliente_list.html', {
            'clientes': cliente_filter.qs,
            'form': form,
            'alt': True,
            'id': cliente.id,
            'filter': cliente_filter,
        })

    # --- deletar (abrir confirmação) ---
    if btn == "delete":
        return render(request, 'clientes/cliente_list.html', {
            'clientes': cliente_filter.qs,
            'delete': True,
            'id': request.POST.get("id"),
            'form': form,
            'filter': cliente_filter,
        })

    # --- salvar/atualizar/excluir ---
    if action_type == "alt":
        cliente = get_object_or_404(Cliente, pk=request.POST.get("id"))
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, f"Cliente {cliente.nome} atualizado com sucesso.")
        else:
            messages.error(request, "Erro ao atualizar cliente. Verifique os campos.")
        return redirect('clientes:cliente_list')

    elif action_type == "save":
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f"Cliente {cliente.nome} cadastrado com sucesso.")
        else:
            messages.error(request, "Erro ao cadastrar cliente. Verifique os campos.")
        return redirect('clientes:cliente_list')

    elif action_type == "delete":
        cliente = get_object_or_404(Cliente, pk=request.POST.get("id"))
        cliente.ativo = False
        cliente.save()
        messages.warning(request, f"Cliente {cliente.nome} foi desativado.")
        return redirect('clientes:cliente_list')

    # fallback
    messages.error(request, "Ação inválida.")
    return redirect('clientes:cliente_list')