from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item
from .forms import CreateNewList
# Create your views here.


def index(response, id):
    ls = ToDoList.objects.get(id=id)
    
    if response.method == "POST":
        if response.POST.get('save'):
            for i in ls.item_set.all():
                if response.POST.get("c" + str(i.id)) == 'checker':
                    i.checked = True
                else:
                    i.checked = False
                i.save()
        elif response.POST.get('newItem'):
            txt = response.POST.get('new')
            if len(txt) > 2:
                ls.item_set.create(text=txt, checked=False)
            else:
                print(f"INVALID INPUT")
            
    
    return render(response, 'main/viewlist.html', {"ls":ls})

def home(response):
    return render(response, "main/home.html", {})

def create(response):
    if response.method == "POST":
        form = CreateNewList(response.POST)
        if form.is_valid():
            n = form.cleaned_data['name']
            t = ToDoList(name=n)
            t.save()
        return HttpResponseRedirect("/%i" %t.id)
    else:
        form = CreateNewList()
    return render(response, "main/create.html", {"form":form})