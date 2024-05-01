# from django.shortcuts import redirect, render
# from django.shortcuts import get_object_or_404
# from django.http import JsonResponse

# from app.forms import AnswerForm
# from app.models import Answer, Question, Test, UserResponse


# def index(request):
#     # Your index view logic here
#     return render(request, 'index.html')


# def question_detail(request, question_id):
#     question = get_object_or_404(Question, id=question_id)
#     form = AnswerForm()
#     return render(request, 'question_detail.html', {'question': question, 'form': form})


# def submit_user_response(request, test_id, question_id, answer_id):
#     if request.method == 'POST':
#         # Get the submitted answer from the form
#         form = AnswerForm(request.POST)
#         if form.is_valid():
#             answer_text = form.cleaned_data['answer']
#             # Get the corresponding test, question, and answer objects
#             test = Test.objects.get(pk=test_id)
#             question = Question.objects.get(pk=question_id)
#             answer = Answer.objects.get(pk=answer_id)
#             # Create a UserResponse object with the submitted data
#             user_response = UserResponse.objects.create(test=test, question=question, answer=answer)
#             # Optionally, you can do additional processing or redirect the user
#             return redirect('index')  # Redirect to the homepage after submitting the response
#         else:
#             # Handle form errors
#             return JsonResponse({'error': 'Form validation failed'}, status=400)
#     else:
#         # Handle non-POST requests
#         return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from .forms import AnswerForm
from .models import Answer, Question, Test, UserResponse

def index(request):
    first_question = Question.objects.first()
    test_id = 1
    return render(request, 'index.html', {'first_question': first_question, 'test_id': test_id})

def question_detail(request, test_id, question_id):
    question = get_object_or_404(Question, test_id=test_id, id=question_id)
    form = AnswerForm()
    return render(request, 'question_detail.html', {'question': question, 'form': form})


def submit_user_response(request, test_id, question_id):
    if request.method == 'POST':
        answer_text = request.POST.get('answer', '')  # Get the answer text from the form
        if answer_text:  # Check if the answer text is not empty
            try:
                test = Test.objects.get(pk=test_id)
                question = Question.objects.get(pk=question_id)
                
                user_response = UserResponse.objects.create(question=question, answer_text=answer_text)
                # Get the next question if it exists
                next_question = Question.objects.filter(test=test, id__gt=question_id).order_by('id').first()
                if next_question:
                    # Redirect to the next question
                    return redirect('question_detail', test_id=test_id, question_id=next_question.id)
                else:
                    # No more questions, redirect to the index page
                    return redirect('index')
            except (Test.DoesNotExist, Question.DoesNotExist) as e:
                return JsonResponse({'error': str(e)}, status=404)  # Handle missing test or question
        else:
            return JsonResponse({'error': 'Answer text is required'}, status=400)  # Handle empty answer text
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)  # Handle non-POST requests
