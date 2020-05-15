from django.shortcuts import render, HttpResponse, redirect, HttpResponsePermanentRedirect
from .models import SigningUser, ContactUser, Profile
from django.contrib import messages
from createpost.models import userpost, BlogComment
from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


def loggin(request):
    if request.method == 'POST':
        number = request.POST['username']
        pass1 = request.POST['passw']
        curr_user = authenticate(username=number, password=pass1)
        if curr_user is not None:
            login_auth(request, curr_user)
            messages.success(request, "Logged in Successfully.")
            return redirect('homepage')
        else:
            return HttpResponse("Invalid username or password")
    return render(request, 'home/login.html')

def signin(request):
    if request.method == 'POST':

        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        number = request.POST['number']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        gender = request.POST['gender']

        if pass1 == pass2:
            try:
                user = User.objects.get(username=username)
                return HttpResponse("User already exist with the username you enetered.")
            except User.DoesNotExist:
                new_user = User.objects.create_superuser(username, number, pass1)
                new_user.first_name = fname
                new_user.last_name = lname

                # Updating signin model as well
                new_signin = SigningUser(fname=fname, lname=lname, username=username, number_email=number, gender=gender)


                # updating to Profile as well
                name = fname + ' ' + lname
                new_profile = Profile(fullname=name, username=username)

                new_user.save()
                new_signin.save()
                new_profile.save()

                return redirect('login')
                # return redirect('homepage')

        else:
            return HttpResponse("Invalid password")
    return render(request, 'home/signup.html')

def ourfamily(request):
    return render(request, 'home/ourfamily.html')

def singlePage(request,title=None):
    post = userpost.objects.filter(title=title).first()
    comments = BlogComment.objects.filter(post=post)
    size = len(comments)


    get_profile =  userpost.objects.filter(title=title).first().author
    pro = Profile.objects.get(username=get_profile)
    context = {
        'post':post,
        'comment':comments,
        'size': [size],
        'user':request.user,
        'pro':pro,
    }
    return render(request, 'home/single-standard.html', context)

def postComment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')

        user = request.user
        postSno = request.POST.get('postSno')
        post = userpost.objects.get(sno=postSno)
        # parent =
        url_title = post.title
        final_url = url_title.replace(' ', "_")

        blogcomment = BlogComment(comment=comment, user=user, post=post)
        blogcomment.save()
        messages.success(request, "Comment has been successfully posted in the comment section below.")
    return redirect(f"single-standard/{url_title}")

def contactusers(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        matter = request.POST['matter']

        contactuser = ContactUser(name=name, email=email, subject=subject, matter=matter)
        contactuser.save()
        messages.success(request, "Thankyou for contacting us. Our team will reach out to you soon.")
        return redirect('homepage')
    return render(request, 'home/contact.html')

def about(request):
    return render(request, 'home/about.html')

def homepage(request):
    context = {
        'userkeposts': [userpost.objects.all()],
        'user': request.user
    }
    return render(request, 'home/homepage.html',context)

def pageNotFound(request,slug):
    return render(request, 'home/PNF.html')

def logout(request):
    if request.method == "GET":
        messages.success(request, "Sucessfully logged out.")
        logout_auth(request)
        request.session.flush()
        return redirect('homepage')
    return render(request, 'home/homepage.html')

def profile(request):

    if request.method == 'POST':

        current_user = request.user.username

        if Profile.objects.filter(username=current_user).exists():
            from_profile_model = Profile.objects.get(username=current_user)
            old_photo = from_profile_model.photo
        else:
            old_photo = ''

        new_username = request.POST['username']
        name = request.POST['fullname']
        bio = request.POST['bio']
        dob = request.POST['dob']
        gender = request.POST['gender']
        marrystatus = request.POST['marrystatus']
        address = request.POST['address']
        occupation = request.POST['occupation']
        number = request.POST['number']
        email = request.POST['email']
        languagesknown = request.POST['languagesknown']

        if len(request.FILES) != 0:
            new_photo = request.FILES['profilephoto']
        else:
            new_photo = old_photo


# USER
        a = 0
        if User.objects.filter(username=new_username).exists():
            a = 1
            user = User.objects.get(username=new_username)
            if ' ' in name:
                fname, lname = name.split(' ')
            else:
                fname = name
                lname = ' '
            user.username = new_username
            user.first_name = fname
            user.last_name = lname
            user.email = email

        else:
             # It will update user if username is unique
            user = User.objects.get(username=current_user)
            if ' ' in name:
                fname, lname = name.split(' ')
            else:
                fname = name
                lname = ' '
            user.username = new_username
            user.first_name = fname
            user.last_name = lname
            user.email = email

# SIGNUP
        if SigningUser.objects.filter(username=new_username).exists():
            signin_info = SigningUser.objects.get(username=new_username)
            signin_info.fname = fname
            signin_info.lname = lname
            signin_info.username = new_username
            signin_info.email = email
            signin_info.gender = gender

        else:
            signin_info = SigningUser.objects.get(username=current_user)
            signin_info.fname = fname
            signin_info.lname = lname
            signin_info.username = new_username
            signin_info.email = email
            signin_info.gender = gender

# PFOFILE
        if Profile.objects.filter(username=new_username).exists():
            new_profile = Profile.objects.get(username=new_username)
            new_profile.username = new_username
            new_profile.photo = new_photo
            new_profile.fullname = name
            new_profile.bio = bio
            new_profile.dob = dob
            new_profile.gender = gender
            new_profile.marrystatus = marrystatus
            new_profile.address = address
            new_profile.occupation = occupation
            new_profile.number = number
            new_profile.email = email
            new_profile.languages = languagesknown

        else:
            new_profile = Profile.objects.get(username=current_user)
            new_profile.username = new_username
            new_profile.photo = new_photo
            new_profile.fullname = name
            new_profile.bio = bio
            new_profile.dob = dob
            new_profile.gender = gender
            new_profile.marrystatus = marrystatus
            new_profile.address = address
            new_profile.occupation = occupation
            new_profile.number = number
            new_profile.email = email
            new_profile.languages = languagesknown


        user_obj = userpost.objects.filter(author=current_user)
        for item in user_obj:
            new_post_author = userpost.objects.get(title=item)
            new_post_author.author = new_username
            new_post_author.save()

        user.save()
        signin_info.save()
        new_profile.save()
        if a  == 0:
            messages.success(request, "Your profile was updated successfully.")
        else:
            messages.warning(request, "Username was not updated because it alredy exists.")
        return redirect('profile')


    updated_username = request.user.username
    updated_profile = Profile.objects.get(username=updated_username)
    context = {
        'from_profile' : updated_profile
    }
    print(updated_profile.gender)

    return render(request,'home/profile.html', context)
