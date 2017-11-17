from django.shortcuts import render, redirect


import os

import webbrowser

def home(request):
    os.system("node server.js")
    return redirect('http://localhost:8080/Apps/HelloWorld.html')
    # return render(request, "home.html", {})