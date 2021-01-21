import datetime


import self as self
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect

from home.models import Customer, User, Product, Order, OrderItem, DeliveryInfo,  FriendshipRequest,Post
from .forms import RegistrationForm, CustomerForm, AddressForm
from django.contrib.auth import authenticate, login
from django.contrib import messages


# Create your views here.


def register(request):
    if request.method == 'POST':
        # eğer post yaratılmış kişi içini doldurmuş ve save demişse yani post metodu request edilmişse, is_valid true dönüyorsa onu db ye kaydeder bilgileri
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # if form data is valid then save it into the database
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            name = request.POST['first_name']
            surname = request.POST['last_name']
            email = request.POST['email']

            values = {
                'name': name,
                'surname': surname,
                'email': email,
                'user': user
            }
            error_message = None
            customer = Customer(name=name, surname=surname, email=email, user=user)
            customer.save()
            messages.success(request, 'Your account is successfully created!')
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Error")


    else:
        # eğer post request edilmemişse yani form yaratılmamışsa boş bir form yaratılır burada da. Hem save edilmesi hem de yaratılması için aynı metod kullanılıyor yani
        form = RegistrationForm()

    # context dictionary is created in here and it will contain the name form that contains the value for this form that we've created above here
    # and once we create that this we can pass this in as the third argument in the below return statement
    # so we can actually access the form within our template and this template is register.html within our users dictionary
    context = {'form': form}
    return render(request, 'user/signup.html', context)



def Profile(request):
    #data = cartData(request)
    #cartItems = data['cartItems']
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer,)
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
        else:
            messages.error(request, 'Please correct the error below.')

    context = {'form': form}
    return render(request, 'user/profile.html', context)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            #   messages.info(request, 'Your password has been changed successfully!')
            return redirect('home')

        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'user/change_password.html', {'form': form})

@login_required(login_url='/login')
def show_profile(request, user_id):
    if request.user.id == user_id:
        return render(request, 'user/profile.html')
    user = User.objects.get(id=user_id)

    return render(request, 'user/profile.html', {'user': user})



def addresses(request):
    customer = request.user.id
    address = DeliveryInfo.objects.filter(belongs_to__id=customer).first()
    form = AddressForm(instance=address)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address, )
        if form.is_valid():
            form.save()
            messages.success(request, 'Changes are successfully updated!')
        else:
            messages.error(request, 'Please correct the error below.')

    context = {'form': form}
    return render(request, 'user/addresses.html', context)


def add_friend(request, user_id):
    if user_id not in FriendshipRequest.objects.filter(user_id=request.user.id).values_list('friend_id',
                                                                                            flat=True).distinct() and \
            FriendshipRequest.objects.filter(user_id=user_id).values_list('friend_id', flat=True).distinct():
        FriendshipRequest.objects.create(user_id=request.user.id, friend_id=user_id)

    return redirect('/user/profile/' + str(user_id))


def accept_friend(request, user_id):
    friendship = FriendshipRequest.objects.get(user_id=user_id, friend_id=request.user.id,confirmed=2)

    friendship.confirmed = 3
    friendship.save()

    return redirect('/friends/')

def favorite_list(request):
    new = Post.objects.filter(likes=request.user)
    return render(request, 'user/favorites.html', {'new': new})