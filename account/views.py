from django.shortcuts import redirect, render
from .forms import SignINForm,SignUpForm
from django.contrib.auth import authenticate,login
# from django.contrib.auth.models import User
from account.models import User
from django.contrib.sites.shortcuts import get_current_site

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.contrib.auth import logout


# Create your views here.

def logout_user(request):
    logout(request)
    return redirect("/")
 
def index(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username,password)
        user = authenticate(request,username = username, password = password )
        print("jjja",user)
        if user is not None:
        
            login(request,user)
            return redirect("homepage:homepage")
        else:
            
            pass
    return render(request,'signin.html')


def signup(request):
   
    if request.method =='POST':
       
            email = request.POST.get('email')
            password = request.POST.get("password")
            user = authenticate(request,username = email, password = password )
            if user is not None:
                print("user exists")
                return redirect("account:sign_in")
            else:
                user = User.objects.create(email = email)
                user.set_password(password)
                user.is_active =  False
                user.save()
                current_site = get_current_site(request)
                email_subject = 'Activate Your Account'
                message = render_to_string('activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                })
                to_email = email
                email = EmailMessage(email_subject, message, to=[to_email])
                email.send()
                return render(request,'send_email_user.html')
                # userr = authenticate(request,username = email, password = password )
                # if userr is not None:
                #     login(request,userr)
                #     return redirect("homepage:dashboard")

    return render(request,'signup.html')


def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request,user)
        current_site = get_current_site(request)
        email_subject = 'Successfull Registration'
        message = render_to_string('successfull_regestration.html', {
        'user': user,
        'domain': current_site.domain
        })
        to_email = user.email
        email = EmailMessage(email_subject, message, to=[to_email])
        email.send()

        return render(request,'your_account_activated.html')
        
    else:
        return render(request,'invalid_link.html')


def password_reset(request):
    msg = ''
    if request.method == "POST":
        email = request.POST.get('email')
        qs = User.objects.filter(email=email)
        site = get_current_site(request)

        if len(qs) > 0:
                user = qs[0]
                user.is_active = False  # User needs to be inactive for the reset password duration
                user.reset_password = True
                user.save()
                

                email_subject = 'Reset Password'
                message = render_to_string('reset_password_email.html', {
                    'user': user,
                    'protocol': 'http',
                    'domain': site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = user.email
                email = EmailMessage(email_subject, message, to=[to_email])
                email.send()

                return HttpResponse('Reset Password Email Sent Successfully')

    
    return render(request,'forgot_password.html')



def reset(request,uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        request.session['user_id'] =  user.id
        return render(request,'password_reset.html')        
    else:
        return HttpResponse('Activation link is invalid!')


def change_user(request):
    user_id =  request.session.get("user_id")
    if request.method == "POST":
        passs =  request.POST.get("password")
        print(passs)
        user_obj =  User.objects.get(id = user_id)
        user_obj.set_password(passs)
        user_obj.save()
        
        del request.session['user_id']
        return redirect("account:sign_in")

            



