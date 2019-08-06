from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string


def random(request):
    stg = get_random_string(length=14)
    
    request.session['count'] += 1

    context = {
        "stg" : stg,

    }
    return render(request, 'random_word/random.html', context)

def reset(request): 
    request.session['count'] = 0

    return redirect('/random') 