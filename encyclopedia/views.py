from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.urls import reverse
from random import choice

from markdown2 import Markdown

from . import util

#searchResults = []

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    entry = forms.CharField(widget=forms.Textarea, label="Entry")

class NewEditForm(forms.Form):
    title = forms.CharField(label="Title", disabled=True)
    entry = forms.CharField(widget=forms.Textarea, label="Entry")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def detail(request, title):
    markdowner = Markdown()
    return render(request, "encyclopedia/detail.html", {
        "entry": markdowner.convert(util.get_entry(title)) ,
        "title": title
        })

def random(request):
    markdowner = Markdown()
    choices = choice(util.list_entries())
    return render(request, "encyclopedia/detail.html", {        
        "entry": markdowner.convert(util.get_entry(choices)),
        "title": choices
    })

def add(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            entry = form.cleaned_data["entry"]
            if util.get_entry(title) == None:
                util.save_entry(title,entry)
                markdowner = Markdown()
                return render(request,"encyclopedia/detail.html", {
                    "entry": markdowner.convert(util.get_entry(title)),
                    "title": title
                })
            else:
                return render(request,"encyclopedia/add.html", {
                    "myMessage": "The title <strong>'" + title + "'</strong> already exists. Please use a different Title.",
                    "form": form
                })
            #return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "encylopedia/add.html", {
                "form": form
            })

    return render(request, "encyclopedia/add.html", {
        "form": NewEntryForm(),
        "title": "Add Wiki"
    })

def editentry(request,id):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            entry = form.cleaned_data["entry"]
            util.save_entry(title,entry)
            markdowner = Markdown()
            return render(request,"encyclopedia/detail.html", {
                "entry": markdowner.convert(util.get_entry(title)),
                "title": title
            })
        else:
            return render(request, "encylopedia/edit.html", {
                "form": form
            })
    else:
        context = {}
        initial_values = { 
            "title" : id, 
            "entry" : util.get_entry(id)
        }
        editform = NewEntryForm(request.POST or None, initial=initial_values)    
        context['form']= editform.as_table
        context['title'] = id
        return render(request, "encyclopedia/edit.html", context)

def search(request):
    title = request.POST.get('q')
    markdowner = Markdown()
    searchResults = util.list_entries()
    searchStrings = []
    for result in searchResults:
        if result.upper() == title.upper():
            return render(request, "encyclopedia/detail.html", {
                "entry": markdowner.convert(util.get_entry(result)),
                "title": title
            })
        elif title.upper() in result.upper():
            searchStrings.append(result)
        else:
            continue
    
    return render(request, "encyclopedia/search.html", {
        "entries": searchStrings,
        "title": title
    })
    