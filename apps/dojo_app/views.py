from django.shortcuts import render, redirect
from .models import User, Post
# Create your views here.
from django.contrib import messages
from django.db.models import Count

def index(request):
    if 'id' in request.session:
        return redirect('/success')
    return render(request, 'dojo_app/index.html')


def process(request):
    if request.method != 'POST':
        return redirect('/')
    else:
        valid = User.objects.validate(request.POST)
        if valid[0] == True:
            request.session['id'] = valid[1].id
            return redirect('/success')
        else:
            for msg in valid[1]:
                messages.add_message(request, messages.INFO, msg)
            return redirect('/')

def success(request):
    if 'id' not in request.session:
        return redirect('/')
    try:
        context= {
            'user' : User.objects.get(id=request.session['id']),
            'secrets' : Post.objects.annotate(numlike=Count('like')).order_by('-created_at')[:5],
            'msgs' : Post.objects.all()
        }
    except User.DoesNotExist:
        messages.add_message(request, messages.INFO, 'user not found')
        return redirect('/')
    return render(request,'dojo_app/secrets.html', context)

def login(request):
    if request.method != "POST":
        return redirect('/')
    else:
        user = User.objects.authenticate(request.POST)
        print user
        if user[0] == True:
            request.session['id'] = user[1].id
            return redirect('/success')
        else:
            messages.add_message(request, messages.INFO, user[1])
            return redirect('/')

def logout(request):
    if 'id' in request.session:
        request.session.pop('id')
    return redirect('/')

def process2(request):
    if request.method != 'POST':
        return redirect('/success')
    post = Post.objects.verify(request.POST, request.session['id'])
    print post
    return redirect('/success')

def like(request, post_id):
    like_valid = Post.objects.like_post(request.session['id'], post_id)
    print 'like_valid'
    return redirect('/success')

def like2(request, post_id):
    like_valid = Post.objects.like_post(request.session['id'], post_id)
    print 'like_valid'
    return redirect('/popular')

def delete(request, id):
    try:
        target = Post.objects.get(id=id)
    except Post.DoesNotExist:
        messages.info(request, 'Post was not found')
        return redirect('/success')
    target.delete()
    return redirect('/success')

def delete2(request, id):
    try:
        target = Post.objects.get(id=id)
    except Post.DoesNotExist:
        messages.info(request, 'Post was not found')
        return redirect('/success')
    target.delete()
    return redirect('/popular')

def popular(request):

    user = User.objects.get(id=request.session['id'])
    secrets =  Post.objects.annotate(numlike=Count('like')).order_by('-numlike')
    liked =  Post.objects.filter(like=user)

    return render(request, 'dojo_app/popular.html',{'secrets':secrets, 'user':user})

# Create your views here.
