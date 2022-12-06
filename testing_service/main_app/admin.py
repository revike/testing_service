from django.contrib import admin
from django.forms import all_valid
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from main_app.models import GroupTest, ResponseTable, Question, \
    ResultTable


@admin.register(ResultTable)
class ResultTableAdmin(admin.ModelAdmin):
    """Admin panel appearance settings"""
    list_display = (
        'id', 'user', 'group_test', 'result', 'completed')
    list_display_links = (
        'id', 'user', 'group_test', 'result', 'completed')
    fields = (
        'id', 'user', 'group_test', 'result', 'completed', 'created',
        'updated', 'count_correct', 'count_not_correct')
    readonly_fields = (
        'id', 'user', 'group_test', 'result', 'completed',
        'created', 'updated',)
    list_filter = ('user__username', 'completed')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class ResponseInline(NestedStackedInline):
    model = ResponseTable
    extra = 0
    fk_name = 'question'


class QuestionInline(NestedStackedInline):
    model = Question
    extra = 1
    fk_name = 'group_test'
    inlines = [ResponseInline]


@admin.register(GroupTest)
class GroupTestAdmin(NestedModelAdmin):
    model = GroupTest
    inlines = [QuestionInline]
    list_display = ('id', 'name', 'description')
    list_display_links = ('id', 'name', 'description')
    fields = ('id', 'name', 'description', 'created', 'updated',)
    readonly_fields = ('id', 'created', 'updated')
    search_fields = ('name', 'description')

    @staticmethod
    def validate_form_admin(form, msg):
        form._errors["__all__"] = form.error_class([msg])
        return form

    def all_valid_with_nesting(self, formsets):
        if not all_valid(formsets):
            return False
        for formset in formsets:
            if not formset.is_bound:
                pass

            for form in formset:

                if hasattr(form, 'nested_formsets'):
                    if not self.all_valid_with_nesting(form.nested_formsets):
                        return False
                    if self.all_valid_with_nesting(form.nested_formsets):
                        correct = 0
                        not_correct = 0
                        for nested_formsets in form.nested_formsets:
                            for nested_formset in nested_formsets.cleaned_data:
                                correct_status = nested_formset.get('correct',
                                                                    None)
                                if correct_status:
                                    correct += 1
                                elif correct_status is False:
                                    not_correct += 1
                        if not correct and not not_correct:
                            continue
                        if not correct or not not_correct:
                            msg = u"Необходимо хотя бы один правильный и " \
                                  u"один неправильный ответ "
                            self.validate_form_admin(form, msg)
                            return False

                    if (not hasattr(
                            form, 'cleaned_data')
                        or not form.cleaned_data) and \
                            self.formset_has_nested_data(form.nested_formsets):
                        msg = u"Вопрос должен быть создан при создании " \
                              u"вложенных ответов "
                        self.validate_form_admin(form, msg)
                        return False
        return True
