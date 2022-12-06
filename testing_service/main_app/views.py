from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import generic

from main_app.forms import ResultCreateForm
from main_app.models import GroupTest, ResultTable, ResponseTable, Question
from main_app.utils import get_context_for_questions, get_data_for_result, \
    update_result_for_quest


class TestingListView(generic.ListView):
    """List tests"""
    template_name = 'main_app/list_test.html'
    model = GroupTest

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список тестов'
        return context

    def get_queryset(self):
        results = ResultTable.objects.filter(user=self.request.user,
                                             completed=True)
        res_list = [i.group_test_id for i in results]
        queryset = self.model.objects.exclude(id__in=res_list)
        return queryset

    @method_decorator(user_passes_test(lambda u: not u.is_anonymous))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class TestingDetailView(generic.DetailView, generic.CreateView):
    """Detail test"""
    template_name = 'main_app/detail_test.html'
    model = GroupTest
    form_class = ResultCreateForm
    success_url = reverse_lazy('main:list_test')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        try:
            get_context_for_questions(self.request, context, self.object)
        except AttributeError:
            pass
        return context

    def post(self, request, *args, **kwargs):
        data = self.request.POST.getlist('response')
        if data:
            response = ResponseTable.objects.filter(
                question__group_test=kwargs['pk'], response__in=data)
            question_count = Question.objects.filter(
                group_test__id=kwargs['pk']).count()

            result_for_quest = ResultTable.objects.filter(
                user=self.request.user,
                group_test=response.first().question.group_test,
            )

            data_for_quest = get_data_for_result(result_for_quest,
                                                 self.request, data,
                                                 question_count)

            result_for_question = update_result_for_quest(result_for_quest,
                                                          self.request,
                                                          response,
                                                          data_for_quest)
            if data_for_quest['completed']:
                try:
                    pk = result_for_question.id
                except AttributeError:
                    pk = result_for_question.first().id
                return HttpResponseRedirect(
                    reverse('main:result', kwargs={'pk': pk}))

        return HttpResponseRedirect(reverse('main:detail_test', kwargs=kwargs))

    def get(self, request, *args, **kwargs):
        result = ResultTable.objects.filter(user=request.user,
                                            group_test=self.get_object(),
                                            completed=True)
        if result:
            return HttpResponseRedirect(reverse(
                'main:result', kwargs={'pk': result.first().pk}))
        return super().get(request, *args, **kwargs)

    @method_decorator(user_passes_test(lambda u: not u.is_anonymous))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ResultView(generic.DetailView):
    """Result"""
    template_name = 'main_app/result.html'
    model = ResultTable
