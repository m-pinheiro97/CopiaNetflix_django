from django.shortcuts import redirect, reverse
from .models import Filme, Usuario
from .forms import CriarContaForm, FormHomepage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView


# Create your views here.

# def homepage(request):
#     return render(request, "homepage.html")

class Homepage(FormView):
    template_name = "homepage.html"
    form_class = FormHomepage

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('filme:homefilmes')
        else:
            return super().get(request, *args, **kwargs)  # redirecionar para homepage

    def get_success_url(self):
        email = self.request.POST.get("email")
        usuarios = Usuario.objects.filter(email=email)
        if usuarios:
            return reverse('filme:login')
        else:
            return reverse('filme:criarconta')


class Homefilmes(LoginRequiredMixin, ListView):
    template_name = "homefilmes.html"
    model = Filme
    # object_list -> lista de itens do modelo


class Detalhesfilme(LoginRequiredMixin, DetailView):
    template_name = "detalhesfilme.html"
    model = Filme
    # object -> 1 item do modelo

    # Número de Visualizações
    def get(self, request, *args, **kwargs):
        filme = self.get_object()  # recebendo qual filme está sendo acessado
        filme.visualizacoes += 1
        filme.save()  # salvando informação no bd
        usuario = request.user
        usuario.filmes_assistidos.add(filme)
        return super().get(request, *args, **kwargs)
        # redireciona o usuário para a url final

    # Relação de filmes a partir da categoria
    # filtrar filmes com a mesma categoria
    # self.get_object() -> objeto acessado
    # para limitar qtd de filmes relacionados (ex: [0:5] exibir 5 filmes apenas)
    def get_context_data(self, **kwargs):
        context = super(Detalhesfilme, self).get_context_data(**kwargs)
        filmes_relacionados = Filme.objects.filter(categoria=self.get_object().categoria)[0:5]
        context['filmes_relacionados'] = filmes_relacionados
        return context


class Pesquisafilme(LoginRequiredMixin, ListView):
    template_name = "pesquisa.html"
    model = Filme

    # object_list
    def get_queryset(self):
        termo = self.request.GET.get('query')
        if termo:
            object_list = self.model.objects.filter(titulo__icontains=termo)
            return object_list
        else:
            return None


class Paginaperfil(LoginRequiredMixin, UpdateView):
    template_name = "editarperfil.html"
    model = Usuario
    fields = ['first_name', 'last_name', 'email']

    def get_success_url(self):
        return reverse('filme:editarperfil')


class Criarconta(FormView):
    template_name = "criarconta.html"
    form_class = CriarContaForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('filme:login')

# def homefilmes(request):
#     context = {}
#     lista_filmes = Filme.objects.all()
#     context['lista_filmes'] = lista_filmes
#     return render(request, "homefilmes.html", context)
