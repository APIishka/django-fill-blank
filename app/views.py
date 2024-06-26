from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from .models import Question, Test, UserResponse
from django.db.models import F

def _format_question_text(text, placeholder):
    # Replace 'coh7$' with input field
    count_placeholders = text.count(placeholder)
    text = text.replace(f'{placeholder*count_placeholders}', f'<input type="text" name="answer" value="" style="width: {16.6*count_placeholders}px; border: none; outline: none; box-shadow: none;" maxlength="{count_placeholders}" >')

    # Replace 'tab$' with spaces
    text = text.replace('tab$', '&nbsp;&nbsp;')

    # Replace '\n' with HTML line breaks
    text = text.replace('\\n', '<br>')

    return text

def index(request):
    first_question = Question.objects.first()
    test_id = 1
    return render(request, 'index.html', {'first_question': first_question, 'test_id': test_id})

def question_detail(request, test_id, question_id):
    test = get_object_or_404(Test, pk=test_id)
    question = get_object_or_404(Question, pk=question_id)
    
    formatted_text = _format_question_text(question.text, question.placeholder)
    
    return render(request, 'question_detail.html', {'test': test, 'question': question, 'formatted_text': formatted_text})

def submit_user_response(request, test_id, question_id):
    if request.method == 'POST':
        answer_text = request.POST.get('answer', '')  # Get the answer text from the form
        if answer_text:
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
                    # No more questions, redirect to the results page
                    return redirect('submit_results')
            except (Test.DoesNotExist, Question.DoesNotExist) as e:
                return JsonResponse({'error': str(e)}, status=404)  # Handle missing test or question
        else:
            return JsonResponse({'error': 'Answer text is required'}, status=400)  # Handle empty answer text
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)  # Handle non-POST requests


def submit_results(request):
    if request.method == 'GET':
        user_responses = UserResponse.objects.all()
        total_questions = Question.objects.count()
        correct_answers = UserResponse.objects.filter(answer_text=F('question__answer__text')).count()
        percentage_correct = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        context = {
            'user_responses': user_responses,
            'percentage_correct': percentage_correct
        }
        return render(request, 'submit_results.html', context)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)
    
def delete_user_responses(request):
    UserResponse.objects.all().delete()
    return JsonResponse({'message': 'User responses deleted successfully'})