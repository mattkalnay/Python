from django.shortcuts import render, redirect
import random
from time import gmtime, strftime


def index(request):
    
    try: 
        request.session['gold']
    except KeyError: 
        request.session['gold'] = 0
    try:
        request.session['act'] 
    except KeyError:
        request.session['act'] = []
    return render(request, 'game/index.html')


def farm(request):

    if request.method =="POST":
        adder = random.randint(10,20)
        request.session['gold'] += adder
        
        request.session['act'].append('Earned ' + str(adder) + ' gold from the farm! (' + strftime("%Y/%m/%d %I:%M %p", gmtime()) + ')') 

        return redirect('/')

def cave(request):
    if request.method =="POST":
        adder = random.randint(5,10)
        request.session['gold'] += adder
        request.session['act'].append('Earned ' + str(adder) + ' gold from the cave! (' + strftime("%Y/%m/%d %I:%M %p", gmtime()) + ')')
        return redirect('/')

def house(request):

    if request.method =="POST":
        adder = random.randint(2,5)
        request.session['gold'] += adder
        request.session['act'].append('Earned ' + str(adder) + ' gold from the house! (' + strftime("%Y/%m/%d %I:%M %p", gmtime()) + ')') 

        return redirect('/')

def casino(request):

    if request.method =="POST":
        adder = random.randint(-50,50)
        request.session['gold'] += adder 
        if adder >= 0: 
            request.session['act'].append('Earned ' + str(adder) + ' gold from the casino! (' + strftime("%Y/%m/%d %I:%M %p", gmtime()) + ')') 
        else:
            request.session['act'].append('Entered a casino and lost' + str(adder) + 'golds... Ouch.. (' + strftime("%Y/%m/%d %I:%M %p", gmtime()) + ')')

        return redirect('/')