from django.shortcuts import render, redirect
from django.http import Http404
from votes.models import Vote
from ravenrpc import Ravencoin

rvn = Ravencoin('user', 'password')

def index(request):
    return render(request, 'index.html')

def browse(request):
    return render(request, 'browse.html', {'votes': Vote.objects.all()[::-1]})

def create(request):
    return render(request, 'create.html')

def questions(request):
    return render(request, 'questions.html') 

def me(request):
    return render(request, 'me.html')

def poll(request, asset_name):
    try:
        vote = Vote.objects.get(asset_name=asset_name)
    except:
        raise Http404("Poll not found")
    return render(request, 'poll.html', {'vote': vote, 
                                         'asset_data': rvn.getassetdata(asset_name)['result']})

def get_poll(request):
    if request.GET.get('asset', None):
        return redirect('/poll/' + request.GET.get('asset', None).upper() + '/')
    return render(request, 'find.html')
