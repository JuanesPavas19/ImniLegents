#programado por: Juan Pavas, Andres Rua, Jose Valencia

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.core.exceptions import ValidationError
from .models import Libro, Nota, Review
from django .contrib import messages
from django.http import JsonResponse
from django.urls import reverse


#verificación de admin
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse

#signup
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .forms import LoginForm

#translation
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Create your views here.
#hola munod como estas


#HOME PAGE
class HomePageView(TemplateView):
    template_name = 'home.html'

#ABOUT PAGE


class AboutPageView(TemplateView):
    template_name = 'about.html'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": _("En esta tienda de libros, queremos que comprendas la importancia de leer y de tener hábitos de lectura"),
            "subtitle": _("¿Quiénes somos?"),
            "description": _("Somos un grupo de estudiantes preocupados por la falta de lectura que hay en la ciudad"),
        })

        return context

class LibroIndexView(View):
    template_name = 'libros/index.html'

    def get(self, request):
        viewData = {}
        viewData["title"] = _("Libros - Tienda")
        viewData["subtitle"] =  _("Listado de libros")
        viewData["libros"] = Libro.objects.all().order_by('precio') #funcionalidad 4

        return render(request, self.template_name, viewData)

class LibroShowView(View):
    template_name = 'libros/show.html'

    def get(self, request, id):
        try:
            libro_id = int(id)
            if libro_id < 1:
                raise ValueError(_("El id del libro debe ser mayor a 1"))
            libro = get_object_or_404(Libro, pk=libro_id)
        except (ValueError, IndexError):
            return HttpResponseRedirect(reverse('home'))

        viewData = {
            #"title": libro.Titulo + _(" - Tienda de Libros"),
            #"subtitle": libro.Titulo + _(" - Informacion del libro"),
            # "title": _("{} - Tienda de Libros").format(libro.Titulo),
            # "subtitle": _("{} - Informacion del libro").format(libro.Titulo),
            "title": _("Tienda de Libros - {}").format(libro.Titulo),
            "subtitle": _("Informacion del libro - {}").format(libro.Titulo),
            "libro": libro,
        }

        return render(request, self.template_name, viewData)
    

class LibroListView(ListView):
    model = Libro
    template_name = 'libro_list.html'
    context_object_name = 'libros'  # This will allow you to loop through 'products' in your template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Libros - Tienda en línea')
        context['subtitle'] = _('Lista de Libros')
        return context   


class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['Titulo', 'Autor', 'ISBN', 'Numero_paginas', 'Fecha_publicacion', 'Editorial', 'precio' ]

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio <= 0:
            raise ValidationError(_('El Precio debe ser mayor a Cero.'))
        return precio

class LibroCreateView(View):
    template_name = 'libros/create.html'
    
    def get(self, request):
        form = LibroForm()
        viewData = {}
        viewData["title"] = _("Crear Libro")
        viewData["form"] = form
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = LibroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            viewData = {}
            viewData["title"] = _("Crear Libro")
            viewData["form"] = form
        return render(request, self.template_name, viewData)

            

class LibroListView(ListView):
    model = Libro
    template_name = 'libro_list.html'
    context_object_name = 'libros'  # This will allow you to loop through 'products' in your template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Libros - Tienda en línea')
        context['subtitle'] = _('Lista de Libros')
        return context   

class LibroDeleteView(View):
    def get(self, request, id):
        libro = get_object_or_404(Libro, pk=id)
        libro.delete()
        return redirect('index') 
    

class NotaIndexView(View):
    template_name = 'notas/index.html'

    def get(self, request):
        viewData = {}
        viewData["title"] = _("Mis notas")
        viewData["subtitle"] = _("Notas")
        viewData["notas"] = Nota.objects.all()

        return render(request, self.template_name, viewData)

class NotaShowView(View):
    template_name = 'notas/show.html'

    def get(self, request, id):
        try:
            nota_id = int(id)
            if nota_id < 1:
                raise ValueError(_("El id de la nota debe ser mayor a 1"))
            nota = get_object_or_404(Nota, pk=nota_id)
        except (ValueError, IndexError):
            return HttpResponseRedirect(reverse('home'))
        
        viewData = {}
        nota = get_object_or_404(Nota, pk=nota_id)
        viewData["title"] = _("Mis notas - ") + nota.titulo_nota
        viewData["subtitle"] = _("Notas - ") + nota.titulo_nota
        viewData["nota"] = nota

        return render(request, self.template_name, viewData)
    
    
class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['titulo_nota', 'contenido_nota', 'fecha_creacion', 'fecha_modificacion']

class NotaCreateView(View):
    template_name = 'notas/create.html'

    def get(self, request):
        form = NotaForm()
        viewData = {}
        viewData["title"] = _("Crear Notas")
        viewData["form"] = form
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = NotaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('misnotas')

        else:
            viewData = {}
            viewData["title"] = _("Crear Notita")
            viewData["form"] = form
        return render(request, self.template_name, viewData)
    
class NotaListView(ListView):
    model = Nota
    template_name = 'nota_list.html'
    context_object_name = 'notas'  # This will allow you to loop through 'products' in your template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Nota - Tienda en línea')
        context['subtitle'] = _('Lista de notitas')
        # Revisar esta clase !!!
        return context
    
class NotaDeleteView(View):
    def get(self, request, id):
        nota = get_object_or_404(Nota, pk=id)
        nota.delete()
        return redirect('misnotas') 
    

class ReviewIndexView(View):
    template_name = 'reviews/index.html'

    def get(self, request):
        viewData = {}
        viewData["title"] = _("Mis Reviews")
        viewData["subtitle"] = _("Reviews")
        viewData["reviews"] = Review.objects.all()

        return render (request, self.template_name, viewData)

class ReviewShowView(View):
    template_name = 'reviews/show.html'

    def get(self, request, id):
        try:
            review_id = int(id)
            if review_id < 1:
                raise ValueError(_("El id de la review debe ser mayor a 1"))
            review = get_object_or_404(Review, pk=review_id)
        except (ValueError, IndexError):
            return HttpResponseRedirect (reverse('home'))
        
        viewData = {}
        review = get_object_or_404(Review, pk=review_id)
        viewData["title"] = _("Mis reviews - ") + review.Titulo_Review
        viewData["subtitle"] = _("Reviews - ") + review.Titulo_Review
        viewData["review"] = review

        return render (request, self.template_name, viewData)

    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['Titulo_Review','Contenido_Review', 'Fecha_Review']


class ReviewCreateView(View):
    template_name = 'reviews/create.html'

    def get(self, request):
        form = ReviewForm()
        viewData = {}
        viewData["title"] = _("Crear Review")
        viewData["form"] = form
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('misreviews')

        else:
            viewData = {}
            viewData["title"] = _("Crear Review")
            viewData["form"] = form
        return render(request, self.template_name, viewData)
    
class ReviewListView(ListView):
    model = Review
    template_name = 'review_list.html'
    context_object_name = 'reviews'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Review - Tienda en línea')
        context['subtitle'] = _('Lista de Reviews')
        return context  

class ReviewDeleteView(View):
    def get(self, request, id):
        review = get_object_or_404(Review, pk=id)
        review.delete()
        return redirect('misreviews')


class CartView(View):
    template_name = 'cart/index.html'
    
    def get(self, request):
        # Obtener los libros del carrito desde la sesión
        cart_libro_ids = request.session.get('cart_libro_ids', [])
        # Obtener los libros de la base de datos basados en los IDs en el carrito
        cart_libros = Libro.objects.filter(id__in=cart_libro_ids)

        available_libros = Libro.objects.exclude(id__in=cart_libro_ids)

        # Preparar los datos para la vista
        view_data = {
            'title': _('Carrito - Tienda en línea'),
            'subtitle': _('Carrito de Compras'),
            'cart_libros': cart_libros,
            'available_libros': available_libros,
        }

        return render(request, self.template_name, view_data)

    def post(self, request, libro_id):
        # Obtener los libros del carrito desde la sesión y agregar el nuevo libro
        cart_libro_ids = request.session.get('cart_libro_ids', [])
        cart_libro_ids.append(libro_id)
        request.session['cart_libro_ids'] = cart_libro_ids

        return redirect('cart_index')

class CartRemoveAllView(View):
    def post(self, request):
        # Eliminar todos los libros del carrito en la sesión
        if 'cart_libro_ids' in request.session:
            del request.session['cart_libro_ids']

        return redirect('cart_index')
    
    

# Verificación de administrador
def admin_check(user):
    return user.tipo_usuario == 'admin'

@user_passes_test(admin_check)
def admin_only_view(request):
    return HttpResponse(_("Esta vista solo es accesible para administradores."))

# Registro de usuario
class SignupView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'registration/SignUp.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        # Si el formulario no es válido, se renderiza de nuevo el template
        # pero esta vez con los errores de validación
        return render(request, 'registration/SignUp.html', {'form': form})

#login será con el defecto de django

# class UserLoginView(View):
#     def get(self, request):
#         form = LoginForm()
#         return render(request, 'registration/login.html', {'form': form})

#     def post(self, request):
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('index')  # Redirigir a alguna página de éxito
#             else:
#                 messages.error(request, 'Usuario o contraseña incorrectos.')
#         return render(request, 'registration/login.html', {'form': form})

def lista_libros (request):
    libros = Libro.objects.all()
    data = []
    for libro in libros:
        data.append({
            'titulo': libro.Titulo,
            'autor': libro.Autor,
            'ISBN': libro.ISBN,
            'numero_paginas': libro.Numero_paginas,
            'editorial': libro.Editorial,
            'fecha_publicacion': libro.Fecha_publicacion.strftime('%Y-%m-%d'),
            'precio': libro.precio,
            'enlace': request.build_absolute_uri(reverse('detalle_libro, args =[libro.pk]'))
        })
        return JsonResponse (data, safe=False)



def get_pokemon_data(request):
    url = 'https://pokeapi.co/api/v2/pokemon/'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        pokemon_list = []
        for pokemon in data.get('results', []):
            pokemon_url = pokemon.get('url')
            pokemon_response = requests.get(pokemon_url)
            if pokemon_response.status_code == 200:
                pokemon_data = pokemon_response.json()
                pokemon_info = {
                    'name': pokemon_data.get('name'),
                    'abilities': [ability.get('ability').get('name') for ability in pokemon_data.get('abilities', [])],
                    'types': [type.get('type').get('name') for type in pokemon_data.get('types', [])],
                    'weight': pokemon_data.get('weight'),
                    'height': pokemon_data.get('height'),
                    'image': pokemon_data.get('sprites', {}).get('front_default'),
                }
                pokemon_list.append(pokemon_info)
        return JsonResponse(pokemon_list, safe=False)
    else:
        return JsonResponse({'error': 'Failed to fetch data'}, status=500)