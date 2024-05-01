from django.contrib import admin
from .models import Test, Question, Answer, UserResponse

admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(UserResponse)