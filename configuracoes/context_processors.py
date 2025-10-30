from configuracoes.models import Configuracao

def tema_context(request):
    try:
        config = Configuracao.objects.first()
        return {'tema': config.tema if config else 'light'}
    except:
        return {'tema': 'light'}