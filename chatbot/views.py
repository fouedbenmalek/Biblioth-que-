from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .services import call_gemini


@login_required
def chat(request):
    question = ''
    response = None

    if request.method == 'POST':
        question = request.POST.get('question', '').strip()
        if question:
            try:
                response = call_gemini(question)
            except Exception as error:
                response = None
                messages.error(request, f"Erreur IA : {error}")
        else:
            messages.warning(request, "Veuillez poser une question au chatbot.")

    return render(request, 'chatbot/chat.html', {
        'question': question,
        'response': response,
    })
