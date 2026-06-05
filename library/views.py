import csv

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Count
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

from .models import Livre, Categorie, Emprunt
from .forms import LivreForm, CategorieForm
from .forms_emprunt import EmpruntForm
from .forms_auth import SignUpForm, ProfileForm

@login_required
def liste_livres(request):

    livres = Livre.objects.select_related(
        'categorie'
    ).all()

    recherche = request.GET.get('recherche')

    if recherche:
        livres = livres.filter(
            Q(titre__icontains=recherche) |
            Q(auteur__icontains=recherche) |
            Q(categorie__nom__icontains=recherche) |
            Q(id__icontains=recherche)
        )

    paginator = Paginator(
        livres,
        10
    )

    page = request.GET.get('page')

    livres = paginator.get_page(page)

    total_livres = Livre.objects.count()

    disponibles = Livre.objects.filter(
        statut='disponible'
    ).count()

    empruntes = Livre.objects.filter(
        statut='emprunte'
    ).count()

    reserves = Livre.objects.filter(
        statut='reserve'
    ).count()

    categories_count = Categorie.objects.count()

    livres_par_categorie = (
        Livre.objects
        .values('categorie__nom')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    return render(
        request,
        'library/liste_livres.html',
        {
            'livres': livres,
            'total_livres': total_livres,
            'disponibles': disponibles,
            'empruntes': empruntes,
            'reserves': reserves,
            'categories_count': categories_count,
            'livres_par_categorie': livres_par_categorie,
        }
    )

@login_required
def ajouter_livre(request):
    form = LivreForm(request.POST or None)

    if form.is_valid():
        form.save()

        messages.success(
            request,
            "Livre ajouté avec succès."
        )

        return redirect('liste_livres')

    return render(
        request,
        'library/form_livre.html',
        {'form': form}
    )


@login_required
def liste_categories(request):
    categories = Categorie.objects.all().order_by('nom')
    form = CategorieForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Catégorie ajoutée avec succès.')
        return redirect('liste_categories')

    return render(
        request,
        'library/categories.html',
        {
            'categories': categories,
            'form': form,
        }
    )


@login_required
def modifier_livre(request, pk):
    livre = get_object_or_404(Livre, pk=pk)

    form = LivreForm(
        request.POST or None,
        instance=livre
    )

    if form.is_valid():
        form.save()

        messages.success(
            request,
            "Livre modifié avec succès."
        )

        return redirect('liste_livres')

    return render(
        request,
        'library/form_livre.html',
        {'form': form}
    )


@login_required
def supprimer_livre(request, pk):
    livre = get_object_or_404(Livre, pk=pk)

    if request.method == 'POST':

        livre.delete()

        messages.success(
            request,
            "Livre supprimé avec succès."
        )

        return redirect('liste_livres')

    return render(
        request,
        'library/supprimer_livre.html',
        {'livre': livre}
    )


@login_required
def detail_livre(request, pk):
    livre = get_object_or_404(Livre, pk=pk)

    return render(
        request,
        'library/detail_livre.html',
        {'livre': livre}
    )
@login_required
def liste_emprunts(request):
    emprunts = Emprunt.objects.select_related('livre').all()
    recherche = request.GET.get('recherche', '').strip()
    statut = request.GET.get('statut', '')

    if recherche:
        emprunts = emprunts.filter(
            Q(livre__titre__icontains=recherche) |
            Q(nom_emprunteur__icontains=recherche)
        )

    if statut == 'en_cours':
        emprunts = emprunts.filter(retourne=False)
    elif statut == 'termine':
        emprunts = emprunts.filter(retourne=True)

    return render(
        request,
        'library/liste_emprunts.html',
        {
            'emprunts': emprunts,
            'request': request,
        }
    )


@login_required
def ajouter_emprunt(request):
    form = EmpruntForm(
        request.POST or None
    )

    if form.is_valid():

        emprunt = form.save()

        emprunt.livre.statut = 'emprunte'
        emprunt.livre.save()

        messages.success(
            request,
            "Emprunt enregistré avec succès."
        )

        return redirect(
            'liste_emprunts'
        )

    return render(
        request,
        'library/form_emprunt.html',
        {
            'form': form
        }
    )


@login_required
def retourner_livre(request, pk):

    emprunt = get_object_or_404(
        Emprunt,
        pk=pk
    )

    emprunt.retourne = True
    emprunt.save()

    livre = emprunt.livre
    livre.statut = 'disponible'
    livre.save()

    messages.success(
        request,
        "Livre retourné avec succès."
    )

    return redirect(
        'liste_emprunts'
    )
@login_required
def export_excel(request):
    livres = Livre.objects.select_related('categorie').all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="livres.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Titre', 'Auteur', 'Catégorie', 'Année', 'Quantité', 'Statut'])

    for livre in livres:
        writer.writerow([
            livre.id,
            livre.titre,
            livre.auteur,
            livre.categorie.nom,
            livre.annee_publication,
            livre.quantite_disponible,
            livre.get_statut_display(),
        ])

    return response

@login_required
def export_pdf(request):
    return HttpResponse('Export PDF n est pas encore disponible. Utilisez l export CSV.')


def logout_view(request):
    logout(request)
    messages.success(request, 'Vous êtes bien déconnecté.')
    return redirect('login')


def signup(request):
    if request.user.is_authenticated:
        return redirect('liste_livres')

    form = SignUpForm(request.POST or None)

    if form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Bienvenue ! Votre compte a bien été créé.')
        return redirect('liste_livres')

    return render(request, 'library/signup.html', {'form': form})


@login_required
def profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)

    if form.is_valid():
        form.save()
        messages.success(request, 'Votre profil a bien été mis à jour.')
        return redirect('profile')

    return render(request, 'library/profile.html', {'form': form})