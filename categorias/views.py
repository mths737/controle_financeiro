from django.shortcuts import render, redirect

from .forms import CategoriaForm
from .models import Categoria


def categoria_list(request):
    if request.method == 'GET':
        form = CategoriaForm()
        categorias = Categoria.objects.all()
        return render(request, 'categorias/categoria_list.html', {'categorias': categorias, 'form': form})
    else:
        if request.POST.get("btn"):
            id = request.POST["id"]
            if request.POST.get("btn") == "edit":
                categoria = Categoria.objects.get(pk=id)
                form = CategoriaForm(instance=categoria)
                categorias = Categoria.objects.all()
                return render(request, 'categorias/categoria_list.html', {'categorias': categorias, 'form': form, 'alt': True, "id":id})
            elif request.POST.get("btn") == "delete":
                categorias = Categoria.objects.all()
                return render(request, 'categorias/categoria_list.html', {'categorias': categorias, 'delete': True, 'id': id})
        else:
            if request.POST.get("btn_order"):
                btn_order = request.POST.get("btn_order")
                current_order_by = request.POST.get("order_by")
                current_order = request.POST.get("order", "cre")

                categorias_qs = Categoria.objects.all()

                # toggle da direção (cre -> dec -> cre)
                if btn_order == current_order_by:
                    new_order = "dec" if current_order == "cre" else "cre"
                else:
                    new_order = "cre"

                # mapeia nomes amigáveis para campos do banco
                order_fields_map = {
                    "nome": "nome",
                }
                order_field = order_fields_map.get(btn_order, "nome")

                if new_order == "cre":
                    categorias = categorias_qs.order_by(order_field)
                else:
                    categorias = categorias_qs.order_by(f"-{order_field}")

                form = CategoriaForm()

                return render(request, 'categorias/categoria_list.html', {
                    'categorias': categorias,
                    'form': form,
                    'order_by': btn_order,
                    'order': new_order,
                })
            elif request.POST.get("btn"):
                if request.POST['type'] == "alt":
                    id = request.POST.get("id")  # vem do input hidden no form
                    categoria = Categoria.objects.get(pk=id)
                    form = CategoriaForm(request.POST, instance=categoria)
                    if form.is_valid():
                        form.save()
                        return redirect('categorias:categoria_list')
                elif request.POST['type'] == "save":
                    form = CategoriaForm(request.POST)
                    if form.is_valid():
                        form.save()
                        return redirect('categorias:categoria_list')
                elif request.POST['type'] == "delete":
                    id = request.POST["id"]
                    categoria = Categoria.objects.get(pk=id)
                    categorias = Categoria.objects.all()
                    return redirect('categorias:categoria_list')

