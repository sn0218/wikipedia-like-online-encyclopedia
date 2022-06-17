from audioop import reverse
from django.shortcuts import render
from markdown2 import Markdown
from . import util
from django.shortcuts import redirect
from django import forms
from django.contrib import messages
import random


# initialize markdowner 
markdowner = Markdown()

# New Page Form 
class NewPageForm(forms.Form):
    title = forms.CharField(
        required=True, 
        label="Title",
        max_length=64,
        widget=forms.TextInput(
            attrs={'placeholder': 'Page Title'
            }
        ))

    content = forms.CharField(
        required=True,
        label="Content",
        widget=forms.Textarea(
        attrs={
            'style': 'height: 30em; width: 50em',
            'placeholder': 'Enter Markdown content'}
        ))

# Edit page form
class EditPageForm(forms.Form):
    content = forms.CharField(
        required=True,
        label="Content",
        widget=forms.Textarea(
        attrs={
            'style': 'height: 30em; width: 50em',
            'placeholder': 'Enter Markdown content'}
        ))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    # get the content of md file 
    entry = util.get_entry(title)

    # check if the entry exist
    if entry is None:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })
    
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        # convert the md file into HTML
        "entry": markdowner.convert(entry)
    })


def search(request):
    # check if method is GET
    if request.method == "GET":
        # save the parameter associated to the key q in query variable
        query = request.GET.get('q', '')  
        
        # get the entries
        entries = util.list_entries()
        # print(entries)

        # check if query matches the entry
        if query in entries:
            # redirect to the view of the entry
            return redirect('entry', title=query)
        
        else:
            # return case-insensitive partial match results
            results = list(filter(lambda x: query.lower() in x.lower(), entries))

            return render(request, "encyclopedia/search.html", {
                "query": query,
                "entries": results
            })

     
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def create(request):
    if request.method == "POST":
        # create form instance to save the submitted data 
        form = NewPageForm(request.POST)

        # check whether the form's valid
        if form.is_valid():

            # isolate the title and content from the cleaned version of form data
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            # get the entries
            entries = util.list_entries()

            # check if the entry already exists with the provided title
            if title in entries:
                messages.error(request, 'The entry already exists.')

                return render(request, "encyclopedia/create.html", {
                "form": form
                })

            else:
                # save entry to disk
                util.save_entry(title, content)

                # return sucessful message
                messages.success(request, 'Encyclopedia page created successfully.')
                
                # redirect user to the new entry's page
                return redirect('entry', title=title)
            
        else:
            # if the form is invalid, re-render the page with existing information
            return render(request, "encyclopedia/create.html", {
                "form": form
            })


    return render(request, "encyclopedia/create.html", {
        "form": NewPageForm()
    })


def edit(request, title):
    if request.method == "POST":
        # create form instance to save the submitted data 
        form = EditPageForm(request.POST)

        # check whether the form's valid
        if form.is_valid():

            # isolate content from the cleaned version of form data
            content = form.cleaned_data["content"]

            # save entry to disk
            util.save_entry(title, content)

            # return sucessful message
            messages.success(request, 'Encyclopedia page updated successfully.')
                
            # redirect user to the entry's page
            return redirect('entry', title=title)
            
        else:
            # if the form is invalid, re-render the page with existing information
            messages.error(request, 'The form is invalid. Please resumbit.')
            # return the pre-populated form by edit form instance
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "form": EditPageForm(initial = {
                    "content": entry
                })
            })

    else:
    # get the content of md file 
        entry = util.get_entry(title)

        # check if the entry exist
        if entry is None:
            return render(request, "encyclopedia/error.html", {
                "title": title
            })
        
        # return the pre-populated form by edit form instance
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "form": EditPageForm(initial = {
                "content": entry
            })
        })


def randpage(request):
    # choose a title randomly
    title = random.choice(util.list_entries())

    # redirect to the randoly chosen page
    return redirect('entry', title=title)

    
    







       
            


    

