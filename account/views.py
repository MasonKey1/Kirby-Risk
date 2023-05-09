from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from orders.views import user_orders

from .forms import RegistrationForm, UserEditForm
from .models import UserBase
from .tokens import account_activation_token


@login_required
def dashboard(request):
    orders = user_orders(request)
    return render(request,
                  'account/user/dashboard.html',
                  {'section': 'profile', 'orders': orders})


@login_required
def edit_details(request):
    """
    If request.method == 'POST' => save the form
    Else render the Edit form
    """
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
        else:
            print(user_form.errors.as_data())                                           # here you print errors to terminal
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request,
                  'account/user/edit_details.html', {'user_form': user_form})


@login_required
def delete_user(request):
    """
    The user will still be stored in database.
    Only the status of the user is changed to inactive.
    """
    user = UserBase.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')


def account_register(request):
    if request.user.is_authenticated:
        return redirect('account:dashboard')
    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)                                                  # create a new user object based on the form data but without saving it to the database immediately.
            user.email = registerForm.cleaned_data['email']                                         # assigns the email from the cleaned form data to the respective fields of the user object
            user.set_password(registerForm.cleaned_data['password'])                                # assigns the password from the cleaned form data to the respective fields of the user object
            user.is_active = False                                                                  # the account needs to be activated before the user can log in
            user.save()                                                                             # saves the user object to the database
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('account/registration/account_activation_email.html', {      # renders an email message template
                'user': user,
                'domain': current_site.domain,                                                      # yourdomain.com
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),                                 # encodes the user's primary key into a URL-safe base64 representation to be used as a unique identifier or token in Django applications, typically for tasks like generating activation URLs or creating unique password reset tokens.
                'token': account_activation_token.make_token(user),                                 # generates a token using the account_activation_token associated with the user object, which is often utilized for user account activation in Django applications
            })
            user.email_user(subject=subject, message=message)                                       # send email
            return HttpResponse('registered succesfully and activation sent')
    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form': registerForm})


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))                                              # decode the URL-safe base64 encoded user ID and ensuring the result is a string
        user = UserBase.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True                                                                       # activate the account
        user.save()                                                                                 # saved the changes in the database
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')
