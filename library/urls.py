from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms_auth import CustomAuthenticationForm

urlpatterns = [
    path('', views.liste_livres, name='liste_livres'),

    path(
        'ajouter/',
        views.ajouter_livre,
        name='ajouter_livre'
    ),

    path(
        'modifier/<int:pk>/',
        views.modifier_livre,
        name='modifier_livre'
    ),

    path(
        'supprimer/<int:pk>/',
        views.supprimer_livre,
        name='supprimer_livre'
    ),

    path(
        'livre/<int:pk>/',
        views.detail_livre,
        name='detail_livre'
    ),

    path(
        'emprunts/',
        views.liste_emprunts,
        name='liste_emprunts'
    ),

    path(
        'emprunts/ajouter/',
        views.ajouter_emprunt,
        name='ajouter_emprunt'
    ),

    path(
        'emprunts/retour/<int:pk>/',
        views.retourner_livre,
        name='retourner_livre'
    ),

    path(
        'export/excel/',
        views.export_excel,
        name='export_excel'
    ),

    path(
        'export/pdf/',
        views.export_pdf,
        name='export_pdf'
    ),
    path(
        'categories/',
        views.liste_categories,
        name='liste_categories'
    ),
    path(
        'accounts/signup/',
        views.signup,
        name='signup'
    ),
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(
            template_name='library/login.html',
            authentication_form=CustomAuthenticationForm,
            redirect_authenticated_user=True
        ),
        name='login'
    ),
    path(
        'accounts/logout/',
        views.logout_view,
        name='logout'
    ),
    path(
        'accounts/profile/',
        views.profile,
        name='profile'
    ),
]