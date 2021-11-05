from django import forms



from .models import Abonent, Phone, Email, Note, Tag

class AbonentForm(forms.ModelForm):
    name = forms.CharField(label = 'Имя')
    birthday = forms.DateField(label = 'день рождения', widget=forms.widgets.SelectDateWidget())
    #email = forms.EmailField(label='электронная очта', widget=forms.widgets.EmailInput())
    

    class Meta:
        model = Abonent
        fields = ('name', 'birthday')#, 'email')