from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Configuracao
from .forms import ConfiguracaoForm
from django.contrib.auth.decorators import login_required

@login_required
def configuracao_view(request):
    configuracao, _ = Configuracao.objects.get_or_create(id=1)

    if request.method == 'POST':
        form = ConfiguracaoForm(request.POST, request.FILES, instance=configuracao)
        if form.is_valid():
            form.save()
            messages.success(request, "Dados atualizados com sucesso!")
            return redirect('configuracoes:configuracao')
    else:
        form = ConfiguracaoForm(instance=configuracao)

    return render(request, 'configuracoes/configuracao.html', {'form': form, 'configuracoes': True})