#programado por: Andres Rua
from django.urls import path, include
from .views import * # HomePageView, AboutPageView,LibroIndexView, LibroShowView, LibroCreateView,  LibroDeleteView, NotaIndexView, NotaShowView, NotaCreateView, NotaDeleteView
	
	
urlpatterns = [
	    path("", HomePageView.as_view(), name='home'),
        path('about/', AboutPageView.as_view(), name='about'),
        path('signup/', SignupView.as_view(), name='signup'),  # URL para la página de registro
        #path('accounts/', include('django.contrib.auth.urls')), #login, logout predeterminado de django #implementado en el urls principal
        #path('login/', UserLoginView.as_view(), name='login'),  # URL para la página de inicio de sesión

        path('libros/', LibroIndexView.as_view(), name='index'),
        path('libros/create', LibroCreateView.as_view(), name='form'),
    	path('libros/<str:id>', LibroShowView.as_view(), name='show'),
        path('libros/<int:id>/delete/', LibroDeleteView.as_view(), name='libro_delete'),

        path('notas/', NotaIndexView.as_view(), name='misnotas'),
        path('notas/create', NotaCreateView.as_view(), name='formota'),
    	path('notas/<str:id>', NotaShowView.as_view(), name='notas'),
        path('notas/<int:id>/delete/', NotaDeleteView.as_view(), name='nota_delete'),

        path('reviews/', ReviewIndexView.as_view(), name='misreviews'),
        path('reviews/create', ReviewCreateView.as_view(), name='forreview'),
    	path('reviews/<str:id>', ReviewShowView.as_view(), name='reviews'),
        path('reviews/<int:id>/delete/', ReviewDeleteView.as_view(), name='review_delete'),  

        path('cart/', CartView.as_view(), name='cart_index'),
        path('cart/add/<str:libro_id>', CartView.as_view(), name='cart_add'),
        path('cart/removeAll', CartRemoveAllView.as_view(), name='cart_removeAll'),

        path('finalizar-compra/', views.FinalizarCompraView.as_view(), name='finalizar_compra'),
        path('download-pdf/', views.download_pdf, name='download_pdf'),

        path('libros/json/', views.lista_libros, name='lista_libros_json'),
        path('apis/', views.get_pokemon_data, name='lista_pokemon'),
        path('check/', views.mostrar_cheque, name = 'check'),
]
]
