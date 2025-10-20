from django.contrib import admin

# Register your models here.

from .models import Answer, Invitation, Notification, Question, Questionaire, Response, ResponseAnswer, User, Profile, Post, Comment, Like, Follow
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Follow)
admin.site.register(Notification)
admin.site.register(Invitation)
admin.site.register(Questionaire)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Response)
admin.site.register(ResponseAnswer)