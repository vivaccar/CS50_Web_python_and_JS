from django.shortcuts import render
import markdown
import random

from . import util

def md_to_html(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html_content = md_to_html(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "Page not found"
        })
    else:
        return render(request, "encyclopedia/entries.html", {
            "title": title,
            "content": html_content
        })
    
def search(request):
    if request.method == "POST":
        search_content = request.POST['q']
        html_content = md_to_html(search_content.lower())
        if html_content is not None:
            return render(request, "encyclopedia/entries.html", {
            "title": search_content,
            "content": html_content
        })
        else:
            all_entries = util.list_entries()
            result = []
            for entry in all_entries:
                if search_content.lower() in entry.lower():
                    result.append(entry)
            return render(request, "encyclopedia/search.html", {
                "result": result
            })
        
def new_page(request):
    if request.method == "GET":
        return render (request, "encyclopedia/new_page.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        if title.lower() in util.list_entries():
            return render(request, "encyclopedia/error.html", {
                "message": "This title already exists."
            })
        else:
            util.save_entry(title, content)
            html_content = md_to_html(title)
            return render(request, "encyclopedia/entries.html", {
                "title": title,
                "content": html_content
            })
        
def edit(request):
    if request.method == 'POST':
        title = request.POST['E_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })

def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_content = md_to_html(title)
        return render(request, "encyclopedia/entries.html", {
            "title": title,
            "content": html_content
        })
    
def random_page(request):
    if request.method == "GET":
        entries = util.list_entries()
        title = random.choice(entries)
        return entry(request, title)