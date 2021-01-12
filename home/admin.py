from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Category)
admin.site.register(DeliveryInfo)
admin.site.register(Answer)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_on')
    list_filter = ('created_on',)
    search_fields = ['name']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'email')
    list_filter = ('name', 'surname')
    search_fields = ('name', 'surname', 'email')

@admin.register(PaymentInfo)
class BankAdmin(admin.ModelAdmin):
    list_display = ('card_number', 'balance')

@admin.register(Post)
class postAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'content', 'title', 'created_at','postpic')
    list_filter = ['created_at']
    search_fields = ('created_by', 'content')


class FriendsListAdmin(admin.ModelAdmin):

    list_display = ['__str__']

    class Meta:
        model = Friendship

admin.site.register(Friendship, FriendsListAdmin)

@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('questionnaire_name', 'questions_count',)
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text']

@admin.register(QuestionnaireResults)
class QuestionnaireResultsAdmin(admin.ModelAdmin):
    list_display = ('user','completed')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('commenter', 'comment_content', 'blogpost', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('commenter', 'comment_content')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)