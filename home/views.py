from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from .models import *
from .forms import QuestionForm
# Create your views here.

def home(request):
    context={}
    return render(request, 'home/home-container.html', context)

def whatsinside(request):
    context={}
    return render(request, 'home/whatsInside.html', context)
def givegift(request):
    context={}
    return render(request, 'home/givegift.html', context)

def orderslist(request):
    context={}
    return render(request, 'home/payment.html', context)

def questionnaire(request):
    category=Question.objects.get(question_category='category_options')
    form = QuestionForm(instance=category)

    context = {}
    return render(request, 'home/questions.html', context)

def contact(request):
    context = {}
    return render(request, 'home/contact.html', context)
def giftcart(request):
    context = {}
    return render(request, 'home/giftcart-display.html', context)

def checkout(request):
    context = {}
    return render(request, 'home/checkout.html', context)

def orderdetails(request):
    context = {}
    return render(request, 'home/order-details.html', context)
def cart(request):
    #data = cartData(request)
    #cartItems = data['cartItems']
    #order = data['order']
    #items = data['items']
    context={}
    #context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'home/cart.html', context)

def friendslist(request):
    context = {}
    return render(request, 'home/friends.html', context)

def blog(request):
    context = {}
    return render(request, 'home/blog.html', context)

def favorites(request):
    context = {}
    return render(request, 'home/favorites.html', context)
def messages(request):
    context = {}
    return render(request, 'home/messages.html', context)

def postdetails(request):
    context = {}
    return render(request, 'home/post-details.html', context)