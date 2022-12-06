import random
from itertools import chain

from main_app.models import ResultTable, Question, ResponseTable


def get_context_for_questions(request, context, group_test):
    """Get context for questions"""
    result = ResultTable.objects.filter(group_test=group_test,
                                        user=request.user)
    question_result = []
    if result:
        questions_result = result.first().questions.all()
        question_result = [i for i in questions_result]

    question = Question.objects.filter(group_test=group_test).exclude(
        question__in=question_result).first()

    type_input = 'checkbox'
    true = random.randint(2, 4)
    if question.type == 'o':
        type_input = 'radio'
        true = 1

    responses_true = ResponseTable.objects.filter(
        question__group_test=group_test, question=question,
        correct=True).order_by('?')[:true]
    false = 4 - responses_true.count()
    responses_false = ResponseTable.objects.filter(
        question__group_test=group_test, question=question,
        correct=False).order_by('?')[:false]
    responses_list = list(chain(responses_false, responses_true))
    responses = sorted(responses_list, key=lambda resp: random.random())

    responses_dict = {}
    for i in responses:
        responses_dict[i.response] = i.correct
    request.session['responses'] = responses_dict

    context['question'] = question
    context['type_input'] = type_input
    context['responses'] = responses

    return context


def get_correct(request, responses):
    """Get correct answer"""
    response = request.session['responses']

    response_table = ResponseTable.objects.filter(response__in=responses)
    response_user = {}
    for i in response_table:
        response_user[i.response] = i.correct

    for k, v in response_user.items():
        answer = response.pop(k)
        if not answer:
            return False

    for k, v in response.items():
        if v:
            return False
    request.session['responses'] = None
    return True


def get_data_for_result(result_for_quest, request, data, question_count):
    """Get data for result"""
    data_for_result = {}
    try:
        completed = result_for_quest.first().completed
        result = result_for_quest.first().result
        count_correct = result_for_quest.first().count_correct
        count_not_correct = result_for_quest.first().count_not_correct
        correct = get_correct(request, data)
        if correct:
            count_correct += 1
        else:
            count_not_correct += 1
    except AttributeError:
        completed = False
        result = 0
        count_correct = 0
        count_not_correct = 0
        correct = get_correct(request, data)
        if correct:
            count_correct = 1
        else:
            count_not_correct = 1

    result_count = count_correct + count_not_correct
    if result_count == question_count:
        completed = True
        result = count_correct / question_count * 100

    data_for_result['count_correct'] = count_correct
    data_for_result['count_not_correct'] = count_not_correct
    data_for_result['completed'] = completed
    data_for_result['result'] = result
    return data_for_result


def update_result_for_quest(result_for_quest, request, response,
                            data_for_quest):
    """Update result for question"""
    if not result_for_quest:
        result_for_quest = ResultTable.objects.create(
            user=request.user,
            group_test=response.first().question.group_test,
            count_correct=data_for_quest['count_correct'],
            count_not_correct=data_for_quest['count_not_correct'],
            completed=data_for_quest['completed'],
            result=f'{data_for_quest["result"]:.0f}',
        )
        result_for_quest.questions.add(response.first().question)
    else:
        result_for_quest.first().questions.add(response.first().question)
        result_for_quest.update(
            count_correct=data_for_quest['count_correct'],
            count_not_correct=data_for_quest['count_not_correct'],
            completed=data_for_quest['completed'],
            result=f'{data_for_quest["result"]:.2f}',
        )
    return result_for_quest
