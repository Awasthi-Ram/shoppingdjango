
from .models import blogpost
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    mypost = blogpost.objects.all()
    return render(request,"blog/index.html",{'mypost':mypost})
    
def BlogPost(request,id):
    post = blogpost.objects.filter(post_id = id)[0]
    #[0] is because it retirn list and we want the data of the frist elemtnt by default there is only one element
    print(post)
    return render(request,"blog/blogpost.html",{'post':post})
    
