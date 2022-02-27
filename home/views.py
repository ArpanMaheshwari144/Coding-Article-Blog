from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User 
from blog.models import Post

# HTML Pages
def home(request):
    return render(request, 'home/home.html')

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content=request.POST['content']
        print(name, email, phone, content)

        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<5:
            messages.error(request, "INVALID DETAILS")
        else:
            contact=Contact(name=name, phone=phone, email=email, content=content)
            contact.save()
            messages.success(request, "YOUR FORM HAS BEEN SUCCESSFULLY SENT")
    return render(request, 'home/contact.html')

def search(request):
    query=request.GET['query']
    if len(query)>78 or len(query) < 1:
        allPosts=Post.objects.none()
    else:
        allPostsTitle=Post.objects.filter(title__icontains=query)
        allPostsContent=Post.objects.filter(content__icontains=query)
        allPostsAuthor=Post.objects.filter(author__icontains=query)
        allPostsSlug=Post.objects.filter(slug__icontains=query)
        allPosts=allPostsTitle.union(allPostsContent, allPostsAuthor, allPostsSlug)

    if allPosts.count()==0:
        messages.warning(request, "NO SEARCH RESULTS FOUND. PLEASE REFINE YOUR QUERY.")
    params={'allPosts':allPosts, 'query':query}
    return render(request, 'home/search.html', params)

# Authentication APIs
def handleSignup(request):
    if request.method=='POST':
        # Get the post parameters
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        password=request.POST['password']
        retypepassword=request.POST['retypepassword']

        # Check for errorneous inputs
        # username should be under 15 characters
        if len(username) > 25:
            messages.error(request, "USERNAME MUST BE UNDER 25 CHARACTERS")
            return redirect('home')

        # username should be alphanumeric
        if not username.isalnum():
            messages.error(request, "USERNAME SHOULD ONLY CONTAINS LETTERS AND NUMBERS")
            return redirect('home')

        if fname == lname:
            messages.error(request, "FIRST NAME AND LAST NAME SHOULD BE DIFFERENT")
            return redirect('home')

        # passwords should match
        if password != retypepassword:
            messages.error(request, "PASSWORDS DID NOT MATCH")
            return redirect('home')

        # Create User
        myuser=User.objects.create_user(username, email, password)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request, "Your iCODER ACCOUNT HAS BEEN SUCCESFULLY CREATED..")
        return redirect('home')
    else:
        return HttpResponse('404 - Not Allowed')

def handleLogin(request):
    if request.method=='POST':
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "SUCCESSFULLY LOGGED IN") 
            return redirect('home')
        else:
            messages.error(request, "INVALID CREDENTIALS, PLEASE TRY AGAIN..")
            return redirect('home')
     

    return HttpResponse('404 - Not Allowed')

def handleLogout(request):
    logout(request)
    messages.success(request, "SUCCESSSFULLY LOGGED OUT")
    return redirect('home')