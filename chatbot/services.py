import json
import re
import time
import urllib.request
import urllib.error
from django.conf import settings
from library.models import Livre

FALLBACK_MODELS = [
    'gemini-flash-latest',
    'gemini-pro',
    'gemini-1.0',
]


def get_library_context() -> str:
    livres = Livre.objects.select_related('categorie').all()[:12]
    if not livres:
        return 'La bibliothèque est vide. Il n y a aucun livre à présenter pour le moment.'

    lines = [
        'Résumé de la bibliothèque :',
        'Voici les livres disponibles dans la base :',
    ]

    for livre in livres:
        lines.append(
            f"ID {livre.id} | {livre.titre} | {livre.auteur} | Catégorie : {livre.categorie.nom} | Statut : {livre.get_statut_display()} | Quantité : {livre.quantite_disponible}"
        )

    return '\n'.join(lines)


def build_prompt(question: str) -> str:
    context = get_library_context()
    return (
        'Tu es un assistant de bibliothèque. Utilise le contexte de la bibliothèque ci-dessous '
        'pour répondre à l utilisateur en français de façon claire et précise. N invente pas de livres. '
        'Si la question ne concerne pas la bibliothèque, indique que tu ne peux répondre que sur les livres existants.\n\n'
        f'{context}\n\nQuestion : {question}\nRéponse :'
    )


def extract_text_parts(value) -> list[str]:
    if isinstance(value, dict):
        texts = []
        if isinstance(value.get('text'), str):
            texts.append(value['text'])
        for nested in value.values():
            texts.extend(extract_text_parts(nested))
        return texts

    if isinstance(value, list):
        texts = []
        for item in value:
            texts.extend(extract_text_parts(item))
        return texts

    return []


def extract_generated_text(data: dict) -> str:
    candidates = data.get('candidates') or data.get('output') or []

    for candidate in candidates:
        if isinstance(candidate, dict):
            text = ''.join(extract_text_parts(candidate))
            if text.strip():
                return text.strip()

    return ''


def build_request(model_name: str, body: dict, api_key: str) -> urllib.request.Request:
    return urllib.request.Request(
        f'https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent',
        data=json.dumps(body).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'X-goog-api-key': api_key,
        },
        method='POST'
    )


def call_model(model_name: str, body: dict, api_key: str) -> str:
    request = build_request(model_name, body, api_key)
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            raw = response.read().decode('utf-8')
            data = json.loads(raw)
    except urllib.error.HTTPError as error:
        message = error.read().decode('utf-8', errors='ignore')
        raise RuntimeError(f'Erreur API Gemini ({error.code}) sur {model_name} : {message}')
    except urllib.error.URLError as error:
        raise RuntimeError(f'Erreur de connexion à Gemini sur {model_name} : {error.reason}')

    text = extract_generated_text(data)
    if not text:
        raise RuntimeError(f'Aucune réponse valide reçue du service IA pour {model_name}.')

    return text.strip()


def local_response(question: str) -> str:
    question_normalized = question.lower()
    match_id = re.search(r'\b(?:id|identifiant)\s*(\d+)\b', question_normalized)
    if match_id:
        livre_id = int(match_id.group(1))
        livre = Livre.objects.select_related('categorie').filter(id=livre_id).first()
        if livre:
            return (
                f"Oui, le livre avec l ID {livre.id} existe.\n" 
                f"Titre : {livre.titre}\n" 
                f"Auteur : {livre.auteur}\n" 
                f"Catégorie : {livre.categorie.nom}\n" 
                f"Statut : {livre.get_statut_display()} ({livre.quantite_disponible} exemplaire(s))"
            )
        return f"Aucun livre trouvé avec l ID {livre_id}."

    if 'victor hugo' in question_normalized or 'auteur' in question_normalized:
        livres = Livre.objects.select_related('categorie').filter(auteur__icontains='victor hugo')
        if livres:
            lines = [
                'Victor Hugo est dans notre catalogue. Voici ses oeuvres :'
            ]
            for livre in livres:
                lines.append(
                    f"- {livre.titre} — {livre.get_statut_display()} ({livre.quantite_disponible} exemplaire(s))"
                )
            return '\n'.join(lines)

    if 'disponible' in question_normalized or 'emprunté' in question_normalized or 'statut' in question_normalized:
        livres = Livre.objects.select_related('categorie').all()
        found = livres.filter(titre__icontains=question_normalized) | livres.filter(auteur__icontains=question_normalized)
        if found.exists():
            livre = found.first()
            return (
                f"{livre.titre} de {livre.auteur} est actuellement {livre.get_statut_display()}.\n"
                f"Catégorie : {livre.categorie.nom} — Quantité disponible : {livre.quantite_disponible}."
            )
        found = livres.filter(titre__icontains=question_normalized)
        if found.exists():
            livre = found.first()
            return (
                f"{livre.titre} de {livre.auteur} est actuellement {livre.get_statut_display()}.\n"
                f"Quantité disponible : {livre.quantite_disponible}."
            )

    if 'roman' in question_normalized or 'romantique' in question_normalized:
        recommandations = Livre.objects.filter(categorie__nom__icontains='roman', statut='disponible')[:5]
        if recommandations:
            lines = ['Voici quelques romans disponibles :']
            for livre in recommandations:
                lines.append(f"- {livre.titre} — {livre.auteur} — Disponible ({livre.quantite_disponible})")
            return '\n'.join(lines)

    if 'cherche un livre de' in question_normalized or 'je cherche' in question_normalized:
        mots = re.findall(r'[a-zA-ZÀ-ÿ]+', question_normalized)
        if len(mots) > 4:
            auteur = ' '.join(mots[-3:])
            livres = Livre.objects.filter(auteur__icontains=auteur)
            if livres.exists():
                lines = [f"Voici les livres trouvés pour {auteur} :"]
                for livre in livres:
                    lines.append(f"- {livre.titre} — {livre.get_statut_display()}")
                return '\n'.join(lines)

    livres = Livre.objects.filter(statut='disponible')[:5]
    if livres.exists():
        lines = ['Je n ai pas pu interroger l API IA, mais voici quelques titres disponibles :']
        for livre in livres:
            lines.append(f"- {livre.titre} — {livre.auteur} — Disponible")
        return '\n'.join(lines)

    return 'Le chatbot ne peut pas répondre automatiquement pour le moment. Réessayez dans quelques instants.'


def call_gemini(question: str) -> str:
    api_key = getattr(settings, 'GOOGLE_GENERATIVE_API_KEY', None)
    if not api_key:
        raise RuntimeError('La clé API Google Gemini est manquante. Vérifiez bibliotheque/settings.py.')

    body = {
        'contents': [
            {
                'parts': [
                    {
                        'text': build_prompt(question)
                    }
                ]
            }
        ]
    }

    last_error = None
    for index, model_name in enumerate(FALLBACK_MODELS, start=1):
        try:
            return call_model(model_name, body, api_key)
        except RuntimeError as error:
            last_error = error
            error_text = str(error).upper()
            if '503' in error_text or 'UNAVAILABLE' in error_text:
                if index < len(FALLBACK_MODELS):
                    time.sleep(1)
                    continue
                break
            if '404' in error_text or '401' in error_text or 'NOT_FOUND' in error_text:
                continue
            if index < len(FALLBACK_MODELS):
                time.sleep(1)
                continue
            break

    return local_response(question)
