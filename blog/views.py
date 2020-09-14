from django.shortcuts import render
from .models import BlogPost
from django.http import HttpResponse

# Create your views here.
def index(request):
    myposts = BlogPost.objects.all()
    myposts = reversed(myposts)
    return render(request,'blog/index.html',{'myposts':myposts})
##########################################################
def latestProducts(request,):
    return render(request,'blog/Latestproducts.html')
##############################################################################################
def blogPosts(request,id):
    post = BlogPost.objects.filter(post_id = id)[0]
    print(post)
    return render(request,'blog/blogPosts.html',{'post':post})
