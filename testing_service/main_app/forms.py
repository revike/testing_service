from django import forms

from main_app.models import ResultTable


class ResultCreateForm(forms.ModelForm):
    """Form for create result"""

    class Meta:
        model = ResultTable
        fields = '__all__'
