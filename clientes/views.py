import locale
from django.shortcuts import render, redirect

from .forms import ClienteForm
from .models import Cliente


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
        return render(request, 'clientes/cliente_list.html', {'clientes': clientes, 'form': form})
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
                return render(request, 'clientes/cliente_list.html', {'clientes': clientes, 'form': form, 'alt': True, "id":id})
            elif request.POST.get("btn") == "delete":
                clientes = Cliente.objects.all()
                for cliente in clientes:
                    cliente.cpf_cnpj = formatar_documento(cliente.cpf_cnpj)
                    cliente.telefone = formatar_telefone(cliente.telefone)
                return render(request, 'clientes/cliente_list.html', {'clientes': clientes, 'delete': True, 'id': id})
        else:
            if request.POST.get("btn_order"):
                btn_order = request.POST.get("btn_order")
                current_order_by = request.POST.get("order_by")
                current_order = request.POST.get("order", "cre")

                clientes_qs = Cliente.objects.all()

                # toggle da direção (cre -> dec -> cre)
                if btn_order == current_order_by:
                    new_order = "dec" if current_order == "cre" else "cre"
                else:
                    new_order = "cre"

                # mapeia nomes amigáveis para campos do banco
                order_fields_map = {
                    "nome": "nome",
                    "cpf_cnpj": "cpf_cnpj",
                    "telefone": "telefone",
                    "email": "email",
                }
                order_field = order_fields_map.get(btn_order, "nome")

                if new_order == "cre":
                    clientes = clientes_qs.order_by(order_field)
                else:
                    clientes = clientes_qs.order_by(f"-{order_field}")

                form = ClienteForm()

                return render(request, 'clientes/cliente_list.html', {
                    'clientes': clientes,
                    'form': form,
                    'order_by': btn_order,
                    'order': new_order,
                })
            elif request.POST.get("btn"):
                if request.POST['type'] == "alt":
                    id = request.POST.get("id")  # vem do input hidden no form
                    cliente = Cliente.objects.get(pk=id)
                    form = ClienteForm(request.POST, instance=cliente)
                    if form.is_valid():
                        form.save()
                        return redirect('clientes:cliente_list')
                elif request.POST['type'] == "save":
                    form = ClienteForm(request.POST)
                    if form.is_valid():
                        form.save()
                        return redirect('clientes:cliente_list')
                elif request.POST['type'] == "delete":
                    id = request.POST["id"]
                    cliente = Cliente.objects.get(pk=id)
                    cliente.ativo = False
                    cliente.save()

                    clientes = Cliente.objects.all()
                    return redirect('clientes:cliente_list')