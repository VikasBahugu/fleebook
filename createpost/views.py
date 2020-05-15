from django.shortcuts import render, HttpResponse, redirect
from . models import userpost
from django.contrib import messages
from PIL import Image

# Create your views here.
def createPost(request):
    if request.method == 'POST':
        title = request.POST['title']
        category = request.POST['category']
        author = request.user
        message = request.POST['message']
        photo = request.FILES['photo']

        user_post = userpost(title=title, category=category, message=message, photo=photo, author=author)
        user_post.save()
        messages.success(request, "New post created, it will appear in the homepage.")
        return redirect('homepage')
    return render(request, 'home/createPost.html')


