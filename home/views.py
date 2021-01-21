import decimal
import json
from statistics import mean
from user.views import *
from django.core.mail import send_mail
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, BadHeaderError
from .models import *
from .forms import  PostForm, CommentForm, AnswerForm, ContactForm,MessagesForm
from django.urls import reverse

# Create your views here.

def home(request):
    context={}
    return render(request, 'home/home-container.html', context)

def whatsinside(request):
    context={}
    return render(request, 'home/whatsInside.html', context)
def givegift(request):
    selected_category = 'SDFGHFD'
    if request.POST:
        selected_category = request.POST.get("category_options", None)


        return redirect('/questions/' + selected_category)

    context = {
        'categories': Category.objects.all(), 'selected': selected_category,
    }
    if request.user.is_authenticated:
        return render(request, 'home/givegift.html', context)
    else:
        return redirect('login')




def orderslist(request, order_id):
    order = Order.objects.get(id=order_id)
    order_items = order.order_items.all()
    context = {
        'order': order,
        'order_items': order_items
    }
    return render(request, 'home/payment.html', context)

@login_required(login_url='/login')
def questionnaire(request, category_name):
    answer_form = AnswerForm()
    category = Category.objects.get(name=category_name)
    questions = Question.objects.filter(question_category=category.id)


    if request.method == 'POST':
        questionnaire_result = QuestionnaireResults(user=request.user,
                                                    questionnaire_id=Question.objects.get(
                                                        id=request.POST.get('question')).questionnaire_id,
                                                    created_at=datetime.now()
                                                   )
        questionnaire_result.save()
        for i in range(0, len(request.POST.getlist('question'))):
            answer = Answer(question_id=request.POST.getlist('question')[i], answer=request.POST.getlist('answer')[i],
                            questionnaire_result=questionnaire_result)
            answer.save()
        return redirect('/cart/')

    context = {'questions': questions, 'answer_form': answer_form}
    return render(request, 'home/questions.html', context)

def checkout(request, order_id):
    order = Order.objects.get(id=order_id)

    if request.method == 'POST':
        order.completed=True
        order.save()
        return redirect('/order-detail/')

    context = {
        'order': order,
        'order_items': order.order_items.all()
    }
    return render(request, 'home/checkout.html', context)


def orderdetails(request):
    orders = request.user.order_set.all()

    context = {
        'orders': orders
    }
    return render(request, 'home/order-details.html', context)



#@login_required(login_url='/login')
def cart(request):
    questionnaire_result = QuestionnaireResults.objects.filter(user=request.user).latest('created_at')
    answers = Answer.objects.filter(questionnaire_result=questionnaire_result).values_list('answer', flat=True)
    value = round(mean(answers))
    if value==5:
        value=6
    elif value==4:
        value=3
    elif value==0:
        value=1

    products = Product.objects.filter(categories__id__in=[value]).distinct()
    context = {
        'products': products
    }

    if request.method == 'POST':
        order = Order(belong_to=request.user, created_at=datetime.now())
        order.save()
        for i in range(0, len(request.POST.getlist('id'))):
            print(request.POST.getlist('quantity')[i])
            if decimal.Decimal(request.POST.getlist('quantity')[i]) != decimal.Decimal(0):
                order_item = OrderItem(created_at=datetime.now(), order_id=order,
                                       product_id_id=request.POST.getlist('id')[i],
                                       quantity=request.POST.getlist('quantity')[i])
                order_item.save()
                order.total_price += order_item.product_id.price * decimal.Decimal(order_item.quantity)
                order.total_items+=decimal.Decimal(order_item.quantity)
        order.save()

        if len(order.order_items.all()) == 0:
            order.delete()
            return redirect('/cart/')

        return redirect('/checkout/' + str(order.id))
    return render(request, 'home/cart.html', context)

def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(username, from_email, message, ['site@admin.gmail.com'])

            except BadHeaderError:
                return HttpResponse('Invalid header found. ')
            return render(request, 'home/contact.html', {'username': username})
    return render(request, 'home/contact.html', {'form': form})

def giftcart(request):
    context = {}
    return render(request, 'home/giftcart-display.html', context)


def blog(request):
    category_count = Blog_Category.objects.all()
    posts = Post.objects.all()
    paginator = Paginator(posts, 4)
    page_number = request.GET.get('page')
    most_recent = Post.objects.order_by('-created_at')[0:3]
    page_request_var = 'page'
    page_obj = paginator.get_page(page_number)
    user=request.user.customer

    context = {
        'posts': page_obj, 'user':user, 'page_request_var': page_request_var,
        'category_count': category_count,'most_recent': most_recent,
    }
    return render(request, 'home/blog.html', context)

def messages(request,id):
    if request.method == 'POST':
        new_msg = Chat_Messages.objects.create(receiver_id=id, sender=request.user, content=request.POST.get('msg'),
                                               created_at=datetime.now())

    messages=Chat_Messages.objects.filter(Q(receiver_id=request.user.id, sender_id=id) | Q(receiver_id=id, sender_id=
    request.user.id)).order_by('created_at')
    friends = FriendshipRequest.objects.filter(Q(user_id=request.user.id) | Q(friend_id=request.user.id))

    context = {
        'friends': friends,
        'messages':messages,'friend_id':id,'friend_name':User.objects.get(id=id).username

    }
    return render(request, 'home/messages.html', context)





def search_post(request):
    category_count = Blog_Category.objects.all()
    most_recent = Post.objects.order_by('-created_at')[0:3]
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        ).distinct()
    context = {
        'posts': queryset,'category_count': category_count,'most_recent': most_recent,
    }
    return render(request, 'home/search_results.html', context)
def show_post(request, pk_blog):
    category_count = Blog_Category.objects.all()
    most_recent = Post.objects.order_by('-created_at')[0:3]
    post = get_object_or_404(Post, id=pk_blog)
    user = post.created_by
    comments = post.comments.all()

    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True

    if request.user.is_authenticated:
        PostView.objects.get_or_create(
            user=request.user,
            post=post)

    comment_form = CommentForm()
    context = {
        'post': post,
        'user': user,
        'comments': comments,
        'likes':is_liked,
        'total_likes': post.number_of_likes,
        'comment_form': comment_form,
        'category_count': category_count,
        'most_recent': most_recent,
    }

    if request.method == "POST":
        comment_form = CommentForm(request.POST,
                                   instance=Comment(blogpost_id=pk_blog, commenter=request.user))
        if comment_form.is_valid():
            comment_form.save()

    return render(request, 'home/post-details.html', context)


def FavoriteView(request, id):
    post = get_object_or_404(Post, id=id)
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        is_liked= True

    return HttpResponseRedirect(reverse('post_details', args=[str(id)]))


def RemoveFavoriteList(request, id):
    post = get_object_or_404(Post, id=id)

    if post.likes.filter(id=request.user.id).exists():
       post.likes.remove(request.user)

    return HttpResponseRedirect(reverse('favorites'))
@login_required(login_url='/login')
def create_post(request):
    category_count = Blog_Category.objects.all()
    most_recent = Post.objects.order_by('-created_at')[0:3]
    post_form = PostForm()

    context = {
        'post_form': post_form,
        'category_count': category_count,
        'most_recent': most_recent
    }
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES, instance=Post(created_by=request.user, created_at=datetime.now()))
        if post_form.is_valid():
            post_form.save()
        post = Post.objects.last()
        return redirect(post.get_absolute_url())

    return render(request, 'home/post-create.html', context)


@login_required(login_url='/login')
def edit_post(request, pk_blog):
    category_count = Blog_Category.objects.all()
    most_recent = Post.objects.order_by('-created_at')[0:3]
    post = get_object_or_404(Post, id=pk_blog)

    if request.user.id == post.created_by:
        return redirect('/blog')
    else:
        post_form = PostForm(instance=post)

    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post_form.save()
        return redirect("/blog")

    context = {
        'post_form': post_form,
        'post': post,
        'category_count': category_count,
        'most_recent': most_recent
    }

    return render(request, 'home/blog-form.html', context)


@login_required(login_url='/login')
def delete_post(request, pk_post):
    if request.user.id != pk_post:
        return redirect('/blog')

    post = Post.objects.get(id=pk_post)
    post.delete()

    return redirect('/blog')


def friendslist(request):
    user=request.user
    context = {
        'friends': FriendshipRequest.objects.filter(Q(user_id=request.user.id) | Q(friend_id=request.user.id)),
        'request': request, 'user':user

    }
    print(context)
    return render(request, 'home/friends.html', context)

def friend_profile(request, id):
    user = get_object_or_404(User, id=id)
    total_friends=FriendshipRequest.objects.filter(Q(friend_id=user.id)).annotate(count=Count('friend'))


    context={'user':user,
             'friends': FriendshipRequest.objects.filter(Q(user_id=user.id) | Q(friend_id=user.id)),
             'total_friends':total_friends}
    return render(request, 'home/friends_profile.html', context)
