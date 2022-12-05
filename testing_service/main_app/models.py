from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from auth_app.models import User


class GroupTest(models.Model):
    """Table Group test"""
    objects = None
    name = models.CharField(max_length=128,
                            verbose_name='название теста')
    description = models.TextField(verbose_name='описание')
    created = models.DateTimeField(auto_now_add=True, verbose_name='создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='изменен')

    class Meta:
        db_table = "group_test"
        verbose_name = "Тест"
        verbose_name_plural = "Наборы тестов"

    def __str__(self):
        return self.name


class Question(models.Model):
    """Table of questions"""
    objects = None
    TYPE_QUESTION = (
        ('o', 'один правильный ответ'),
        ('m', 'несколько правильных ответов'),
    )
    group_test = models.ForeignKey(GroupTest, on_delete=models.CASCADE,
                                   verbose_name='тест')
    question = models.TextField(verbose_name='вопрос')
    type = models.CharField(max_length=1, choices=TYPE_QUESTION,
                            verbose_name='тип вопроса')
    created = models.DateTimeField(auto_now_add=True, verbose_name='создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='изменен')

    class Meta:
        db_table = "question"
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.question


class ResponseTable(models.Model):
    """Response table"""
    objects = None
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 verbose_name='вопрос')
    response = models.CharField(max_length=128, verbose_name='ответ')
    created = models.DateTimeField(auto_now_add=True, verbose_name='создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='изменен')
    correct = models.BooleanField(default=False, verbose_name='верный ответ')

    class Meta:
        db_table = "response"
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return self.response


class ResultTable(models.Model):
    """Table Result"""
    objects = None
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='пользователь')
    group_test = models.ForeignKey(GroupTest, on_delete=models.CASCADE,
                                   verbose_name='тест')
    count_correct = models.PositiveSmallIntegerField(
        verbose_name='правильные ответы')
    count_not_correct = models.PositiveSmallIntegerField(
        verbose_name='неправильные ответы')
    result = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, verbose_name='результат',
        validators=[MinValueValidator(Decimal('0.00'))])
    best_result = models.DecimalField(
        max_digits=5, decimal_places=2, default=0,
        verbose_name='лучший результат',
        validators=[MinValueValidator(Decimal('0.00'))])
    created = models.DateTimeField(auto_now_add=True, verbose_name='создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='изменен')

    class Meta:
        db_table = "result"
        verbose_name = "Результат"
        verbose_name_plural = "Результаты"

    def __str__(self):
        return self.group_test.name
