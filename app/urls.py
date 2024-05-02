from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('question/<int:test_id>/<int:question_id>/', views.question_detail, name='question_detail'),
    path('submit_response/<int:test_id>/<int:question_id>/', views.submit_user_response, name='submit_response'),
    path('submit_results/', views.submit_results, name='submit_results'),
    path('delete_user_responses/', views.delete_user_responses, name='delete_user_responses'),
]
