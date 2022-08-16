from .models import Filme


def filmes_recentes(request):
    lista_filmes = Filme.objects.all().order_by('-data_criacao')[0:6]
    if lista_filmes:
        filme_destaque = lista_filmes[0]
    else:
        filme_destaque = None
    return {"lista_filmes_recentes": lista_filmes, "filme_destaque": filme_destaque}


def filmes_populares(request):
    lista_filmes = Filme.objects.all().order_by('-visualizacoes')[0:6]
    return {"lista_filmes_populares": lista_filmes}

