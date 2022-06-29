import bcrypt
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect, render
from app_one.models import Comment, Message, User
from django.contrib import messages
import re

def index(request):
    return render(request,"home.html")


def register(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/register")
        else:
            password = request.POST["password"]
            salt = bcrypt.gensalt()
            hash = bcrypt.hashpw(password.encode(), salt)
            user = User()
            user.first_name = request.POST["first_name"]
            user.last_name = request.POST["last_name"]
            user.email = request.POST["email"]
            user.password = request.POST["password"]
            user.password = hash.decode()
            user.save()
            if user.id==1:
                user.is_admin = True
                user.save()
            messages.success(request, "User has been sucessfully registered")
        return redirect("/signin")
    else:
        return render(request,"register.html")

def signin(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        errors = User.objects.login_basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/signin")
        else:
            try:
                user = User.objects.get(email=email)
                if bcrypt.checkpw(password.encode(), user.password.encode()):
                    request.session["loggedInUser"] = user.id
                    request.session["userLevel"] = user.is_admin
                    if user.is_admin == True:
                        return redirect("dashboard/admin")
                    if user.is_admin == False:
                        return redirect("dashboard/users")
                else:
                    messages.error(request, "Incorrect Password")
            except User.DoesNotExist:
                messages.error(
                    request, "You do not have an account ,Please Register first !")
    return render(request,"signin.html")


def dashboard(request):
    if "loggedInUser" in request.session:
        user = User.objects.get(id=request.session["loggedInUser"])
        if user.is_admin:
            context = {
               "users": User.objects.all()
            }
            return render(request, "dashboard.html", context)
        else:
            return HttpResponse("PROTECTED PAGE !")
    else:
        return HttpResponse("PROTECTED PAGE !")

def userDshboard(request):
    if "loggedInUser" in request.session:
            user = User.objects.get(id=request.session["loggedInUser"])
            context = {
                "user": user,
               "users": User.objects.all()
            }
    return render(request, "userDashboard.html", context)
        
    
def editUser(request,userId):
        context = {
               "user": User.objects.get(id=userId)
            }
        return render(request,"editUser.html",context)

def addUser(request):
    user = User.objects.get(id=request.session["loggedInUser"])
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/users/new")
        else:
            password = request.POST["password"]
            salt = bcrypt.gensalt()
            hash = bcrypt.hashpw(password.encode(), salt)
            user = User()
            user.first_name = request.POST["first_name"]
            user.last_name = request.POST["last_name"]
            user.email = request.POST["email"]
            user.password = request.POST["password"]
            user.password = hash.decode()
            user.is_admin = False
            user.save()
            messages.success(request, "User has been added sucessfully")
            return redirect("/users/new")
    return render(request,"addUser.html")


def removeUser(request,userId):
    User.objects.get(id=userId).delete()
    print("removed...")
    return redirect("/dashboard/admin")

#when normal user click on profile in nav , view the info & allow alter
def userEdit(request,userId):
    user = User.objects.get(id=userId)
    if request.method == "POST":
        errors = User.objects.update_basic_validator(request.POST,user)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f"/users/edit/{ userId }")
        else:
            user.email = request.POST["email"]
            user.first_name = request.POST["first_name"]
            user.last_name = request.POST["last_name"]
            user.save()
            messages.success(request,"Information updated")

            return redirect(f"/users/edit/{ userId }")
    context = {
               "user": user
            }
    return render(request, "editUser.html", context)

def Adminedit(request,userId):
    user = User.objects.get(id=userId)
    if request.method == "POST":
        errors = User.objects.update_basic_validator(request.POST,user)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f"/users/Adminedit/{ userId }")
        else:
            user.email = request.POST["email"]
            user.first_name = request.POST["first_name"]
            user.last_name = request.POST["last_name"]
            user.is_admin = request.POST["level"]
            user.save()
            messages.success(request,"Information updated")

            return redirect(f"/users/Adminedit/{ userId }")
    context = {
               "user": user
            }
    return render(request, "AdmineditUser.html", context)


def userEditPassword(request,userId):
    user = User.objects.get(id=userId)
    if request.method == "POST":
        if len(request.POST["password"]) < 8 :
            messages.error(request,"Password should be at least 8 characters")
            
        elif not re.match(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$', request.POST['password']):
            messages.error(request,"password should be strong")

        elif request.POST["confirmPW"] != request.POST["password"]:

                messages.error(request,"The passwords don't match")
            
        else:
                password = request.POST["password"]
                salt = bcrypt.gensalt()
                hash = bcrypt.hashpw(password.encode(), salt)
                user.password = request.POST["password"]
                user.password = hash.decode()
                user.save()
                messages.success(request,"Password updated")

                return redirect(f"/users/edit/{ userId }")
    context = {
               "user": user
            }
    return render(request, "editUser.html", context)
        
def adminEditPassword(request,userId):
    user = User.objects.get(id=userId)
    if request.method == "POST":
        if len(request.POST["password"]) < 8 :
            messages.error(request,"Password should be at least 8 characters")
            
        elif not re.match(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$', request.POST['password']):
            messages.error(request,"password should be strong")

        elif request.POST["confirmPW"] != request.POST["password"]:

                messages.error(request,"The passwords don't match")
            
        else:
                password = request.POST["password"]
                salt = bcrypt.gensalt()
                hash = bcrypt.hashpw(password.encode(), salt)
                user.password = request.POST["password"]
                user.password = hash.decode()
                user.save()
                messages.success(request,"Password updated")

                return redirect(f"/users/Adminedit/{ userId }")
    context = {
               "user": user
            }
    return render(request, "AdmineditUser.html", context)



def userEditDesc(request,userId):
    user = User.objects.get(id=userId)
    if request.method == "POST":
        if not request.POST["desc"]:
            return redirect(f"/users/edit/{ userId }")
        else:
            user.desc = request.POST["desc"]
            user.save()
            messages.success(request,"Description updated")

        return redirect(f"/users/edit/{ userId }")
    context = {
               "user": user
            }
    return render(request, "editUser.html", context)

#==================================================
def show_user(request,id):
    context={
        'user':User.objects.get(id=id),
    }
    return render(request,"userShow.html",context)

def post_message(request,id):
    if request.method == "POST":
        message=request.POST["message"]

        Message.objects.create(message=message,
        user_id=request.session["loggedInUser"],
        for_user_id=id)

    return redirect(f'/users/show/{id}')

def post_comment(request,id):
    user=request.POST["user"]
    if request.method == "POST":
        comment=request.POST["comment"]
        Comment.objects.create(comment=comment,
        user_id=request.session["loggedInUser"],
        message_id =id)

    return redirect(f'/users/show/{user}')
   
#==============================================
def logoff(request):
    request.session.flush()
    return redirect("/")