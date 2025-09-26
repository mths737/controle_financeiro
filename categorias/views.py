from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import CategoriaForm
from .models import Categoria
from .filters import CategoriaFilter


def categoria_list(request):
    categorias_qs = Categoria.objects.all()
    categoria_filter = CategoriaFilter(request.GET, queryset=categorias_qs)
    form = CategoriaForm()
    context = {
        'filter': categoria_filter,
        'form': form,
        'categorias': categorias_qs,
    }

    # POST actions
    if request.method == 'POST':
        # Ordenação
        if request.POST.get("btn_order"):
            btn_order = request.POST.get("btn_order")
            current_order_by = request.POST.get("order_by")
            current_order = request.POST.get("order", "cre")

            # Toggle da direção
            new_order = "dec" if (btn_order == current_order_by and current_order == "cre") else "cre"

            # Mapear campos
            order_fields_map = {
                "nome": "nome",
            }
            order_field = order_fields_map.get(btn_order, "nome")

            categorias = categorias_qs.order_by(order_field if new_order == "cre" else f"-{order_field}")

            context.update({
                'categorias': categorias,
                'order_by': btn_order,
                'order': new_order,
            })
            return render(request, 'categorias/categoria_list.html', context)

        # Ações de edição/exclusão
        elif request.POST.get("btn"):
            btn_type = request.POST.get("btn")
            id = request.POST.get("id")
            categoria = get_object_or_404(Categoria, pk=id)

            # Editar
            if btn_type == "edit":
                form = CategoriaForm(instance=categoria)
                context.update({
                    'form': form,
                    'alt': True,
                    'id': id,
                })
                return render(request, 'categorias/categoria_list.html', context)

            # Deletar
            elif btn_type == "delete":
                context.update({
                    'delete': True,
                    'id': id,
                })
                return render(request, 'categorias/categoria_list.html', context)

        # Salvar alterações, criar ou deletar via type
        elif request.POST.get("type"):
            type_action = request.POST.get("type")

            if type_action == "alt":
                id = request.POST.get("id")
                categoria = get_object_or_404(Categoria, pk=id)
                form = CategoriaForm(request.POST, instance=categoria)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Categoria alterada com sucesso!")
                    return redirect('categorias:categoria_list')

            elif type_action == "save":
                form = CategoriaForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Categoria cadastrada com sucesso!")
                    return redirect('categorias:categoria_list')

            elif type_action == "delete":
                id = request.POST.get("id")
                categoria = get_object_or_404(Categoria, pk=id)
                categoria.delete()
                messages.success(request, "Categoria excluída com sucesso!")
                return redirect('categorias:categoria_list')

    # GET request
    return render(request, 'categorias/categoria_list.html', context)