from django.shortcuts import render,HttpResponseRedirect
from .forms import SignUpForm , LoginForm , PostModelForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Post 
from django.contrib.auth.models import Group
# Create your views here.



def home(request):
    post = Post.objects.all()
    return render(request,'home.html',{'post':post})




def about(request):
    return render(request,'about.html')




def contact(request):
    return render(request,'contact.html')



def dashboard(request):
    if request.user.is_authenticated:
        post = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request,'dashboard.html',{'post':post,'full_name':full_name,'groups':gps})
    else:
        return HttpResponseRedirect('/login/')



def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = LoginForm(request=request , data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upassword = fm.cleaned_data['password']
                user = authenticate(username=uname , password=upassword)
                if user is not None:
                    login(request,user)
                    messages.success(request,"Logged in Successfully !!")
                    return HttpResponseRedirect('/dashboard/')
        else:
            fm= LoginForm()
        return render(request,'login.html',{'form':fm})
    else:
        return HttpResponseRedirect('/dashboard/')





# SIGNUP FORM KE LIYE HAME DJANGO PREDEFINED FORM PROVIDE KARTA HE JISE HAM LOG USERCREATION FORM KAHTE HE
def user_signup(request):
    if request.method == 'POST':
        fm = SignUpForm(request.POST)
        if fm.is_valid():
            user = fm.save()  
            messages.success(request,'Your are Sign-in Successfully Your account has been created')
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:  
       fm = SignUpForm()
    return render(request,'signup.html',{'form':fm})





def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')




# Add Post View function
def add_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = PostModelForm(request.POST)
            if fm.is_valid():
                title = fm.cleaned_data['title']
                desc = fm.cleaned_data['desc']
                post = Post(title=title, desc=desc)
                post.save()
                fm = PostModelForm()
        else:
            fm = PostModelForm()
        return render(request,'addpost.html',{'form':fm})       
    else:
        return HttpResponseRedirect('/login/')


#update post view function
def update_post(request,id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = Post.objects.get(pk=id)
            fm = PostModelForm(request.POST , instance=pi)
            if fm.is_valid():
                fm.save()
        else:
           pi = Post.objects.get(pk=id)
           fm = PostModelForm(instance=pi) 
        return render(request,'updatepost.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')



#delete post view function
def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')