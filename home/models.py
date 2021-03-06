from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from taggit.managers import TaggableManager
from django.conf import settings
# Create your models here.




class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, blank=False)
    surname = models.CharField(max_length=200, blank=False)
    email = models.EmailField(max_length=200, blank=False)
    profile_pic = models.ImageField(default="profile2.png", null=True)
    date=models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    def __str__(self):
        return self.name + self.surname


class Category(models.Model):
    name = models.CharField(max_length=255,null=True)
    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    categories = models.ManyToManyField(Category, blank=True)
    #tags = TaggableManager()
    #similars = models.ManyToManyField(Product)
    image = models.ImageField(blank=False)
    favorites = models.ManyToManyField(User, related_name='product_favorites', blank=True)
    description = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    objects = models.Manager()

class Order(models.Model):
    total_items = models.DecimalField(blank=True,null=True,default=0, max_digits=10, decimal_places=2)
    total_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    belong_to = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now, blank=False)
    completed= models.BooleanField(default=False,blank=True)


class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(default=1, blank=False, max_digits=6, decimal_places=2)
    status = models.CharField(blank=False, default='Pending', max_length=64)
    created_at = models.DateTimeField(default=datetime.now, blank=False)


class PaymentInfo(models.Model):
    belongs_to = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    name_on_card = models.CharField(max_length=255, blank=False)
    card_number = models.CharField(max_length=20, blank=False)
    expiration_date = models.DateField(blank=False)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.now, blank=False)
    balance = models.FloatField(max_length=10, default=1000)
    def __str__(self):
        return self.card_number


class DeliveryInfo(models.Model):
    belongs_to = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    country = models.CharField(max_length=64, blank=False)
    city = models.CharField(max_length=64, blank=False)
    details = models.TextField(blank=False)
    postal_code = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.now, blank=False)




class Blog_Category(models.Model):
    title = models.CharField(max_length=255,null=True)
    def __str__(self):
        return self.title

class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False,null=True)
    blog_categories = models.ManyToManyField(Blog_Category, blank=True)
    content = models.TextField(blank=False)
    created_at = models.DateTimeField(default=datetime.now, blank=False)
    likes = models.ManyToManyField(User, related_name='post_likes')
    postpic=models.ImageField(default="bio-image.png", null=True, blank=True)
    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.title} by {self.created_by}'

    @property
    def number_of_comments(self):
        return Comment.objects.filter(blogpost=self).count()

    @property
    def number_of_likes(self):
        return self.likes.all().count()
    def get_absolute_url(self):
        return "/blog/post/%i" % self.id

    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()

class Comment(models.Model):
    blogpost = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    comment_content = models.TextField()
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return str(self.commenter) + ', ' + self.blogpost.title[:40]


class FriendshipRequest(models.Model):
    NOT_CONFIRMED = 1
    PENDING = 2
    CONFIRMED = 3

    STATUS_CHOICES = (
        (NOT_CONFIRMED, 'Not Confirmed'),
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friends")
    confirmed = models.IntegerField(choices=STATUS_CHOICES,
                                    default=PENDING)

    def __str__(self):
        return self.user.username


class Questionnaire(models.Model):
    questionnaire_name = models.CharField(max_length=100,
                                          null=False,
                                          default=None,
                                          blank=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    questions_count = models.IntegerField(default=0)

    def __str__(self):
        return self.questionnaire_name


class Question(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    question_category = models.ManyToManyField(Category,
                                               default=None,
                                               blank=False)

    def __str__(self):
        return self.question_text


class QuestionnaireResults(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False),
    created_at = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.user.username


class Answer(models.Model):
    RATING_CHOICES = ((0, "0"), (1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"))
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.IntegerField(choices=RATING_CHOICES,default=0)
    questionnaire_result = models.ForeignKey(QuestionnaireResults, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return u"%s - %s" % (self.question, self.answer)

class Chat_Messages(models.Model):
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='receiver')
    content = models.TextField(blank=False)
    created_at = models.DateTimeField(default=datetime.now, blank=False)
    unread=models.BooleanField(default=True)