from random import choices
from django import forms
from django.forms.widgets import CheckboxSelectMultiple, SelectDateWidget


from .models import Abonent, Phone, Email, Note, Tag


class AbonentForm(forms.ModelForm):
    name = forms.CharField(label='Имя')
    birthday = forms.DateField(
        label='день рождения', widget=forms.widgets.SelectDateWidget())
    #email = forms.EmailField(label='электронная очта', widget=forms.widgets.EmailInput())

    class Meta:
        model = Abonent
        fields = ('name', 'birthday')  # , 'email')


class FindContactsForm(forms.Form):
    #tags_dict = {elem.tag: elem for elem in Tag.objects.all()}
    tags_test = (('A', 'a'), ('B', 'b'), ('C', 'c'))
    pattern = forms.CharField(label='паттерн', required=False)
    tags = forms.MultipleChoiceField(
        choices=tags_test, widget=CheckboxSelectMultiple, label='выберите тэги', required=False)
    date = forms.DateField(label='дата', widget=SelectDateWidget(
        years=[a for a in range(1920, 2021)]), required=False)
