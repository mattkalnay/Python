from django.shortcuts import render, redirect
from .models import Show
from django.contrib import messages


def add(request):
    return render(request, 'restful_tv/add.html')

def update(request, id):
    errors = Show.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/shows/{id}/edit')
    else:
        update_show = Show.objects.get(id=id)
        update_show.title = request.POST['title']
        update_show.network = request.POST['network']
        update_show.release = request.POST['release']
        update_show.desc = request.POST['desc']
        update_show.save()
        print(update_show)
        return redirect(f'/shows/{id}')

def show(request):
    context = {
        "details" : Show.objects.all()
    }
    return render(request, 'restful_tv/show.html', context)

def edit(request, id):
    context = {
        "information" : Show.objects.get(id=id),
    }

    return render(request, 'restful_tv/edit.html', context)

def display(request, id):
    context = {
        "information" : Show.objects.get(id=id),
    }
    return render(request, 'restful_tv/display.html', context)

def delete(request, id):
    d = Show.objects.get(id=id)
    d.delete()
    return redirect('/shows')

def fresh(request):
    errors = Show.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
                messages.error(request, value)
        return redirect('/shows/new')
    else: 
        new_show = Show.objects.create(title=request.POST['title'], network = request.POST['network'], release=request.POST['release'], desc = request.POST['desc'])
        print(new_show)
        return redirect('/shows')

def root(request):
    return redirect('/shows')
