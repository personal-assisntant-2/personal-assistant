'''from django.contrib.auth.decorators import login_required

@login_required 
 @login_required(login_url='auth:login')
'''
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.urls import reverse
from django.template import loader
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User


from .forms import AbonentForm
from .models import Abonent, Phone, Email, Note, Tag

from datetime import date, timedelta

class AbonentDetailView(DetailView):
    """built-in view
        to view one contact from model Abonent
        data from Phone, Email, Note are added to the standard context
    """
    model = Abonent
    #template_name = 'addressbook/detail.html'
    context_object_name = 'abonent'
    
    def get_context_data(self,**kwargs):
        
        context = super().get_context_data(**kwargs)
        
        context['phones'] = Phone.objects.filter(abonent_id = context['abonent'].id)
        context['emails'] = Email.objects.filter(abonent_id = context['abonent'].id)
        context['notes'] = Note.objects.filter(abonent_id = context['abonent'].id)
        return context
    

def change_user():
    ''' искусственная функция для внутренного пользования
    пока нет аутентификации здесь переключается с анонимного пользователя
    на ulkabo
    '''
    from django.contrib.auth import login, logout, authenticate
    user = User.objects.get(pk=1)
    print(user.username)
    #user = authenticate(request, username=user.username, password=user.password) 
    login(request, user)

def find_contact(request):
    pass

def add_contact(request):
    ''' form for adding a contact
     there are all fields from all models.
     name
     birthday
     address
     phone - 3
     email - 3
     the note
     tag - 2
     records are manually created in all tables.
     validation not registered yet
    '''
    # список тегов нужен для автозаполнения(подсказки) в поле тегов
    tags = Tag.objects.all()
    content = {'tags': [tag.tag for tag in tags]}
    if request.method == 'POST':
        # считываем данные с реквеста и сразу записываем в словарь
        # иначе теряются телефоны, и почты, остается только один, из последного поля
        data = dict(request.POST)
        # если нет имени, форма возвращается пустая
        if not data['name'][0]:
            return redirect(reverse('addressbook:add-contact'))

        # создается запись в Аbonent
        abonent = Abonent.objects.create(
            owner_id= request.user.id,
            name = data['name'][0],
            birthday = data['birthday'][0],
            address = data['address'][0])
        # создаются записи в Phone
        for el in data['phone']:
            print('phone', el)
            if el:
                ph= Phone.objects.create(
                    abonent_id = abonent.id,
                    phone = int(el)
                )
        # создаются записи в Email 
        for el in data['email']:
            print('email', el)
            if el:
                em = Email.objects.create(
                    abonent_id = abonent.id,
                    email = el
                ) 
        #если заметки есть, то добавляем заметку в таблицу  Note
        if data['note'] :
            note = Note.objects.create(
                abonent_id = abonent.id,
                note = data['note'][0]
                )
            #создаем список тегов из формы, чтобы потом к ним привязать заметку
            tags_list = []
            for el in data['tag']:
                #поле тега может быть пустым, тогда пропускаем его
                if el:
                    # если тега нет в таблице  Tag  , то создаем там запись
                    if el not in content['tags']:
                        tags_list.append(Tag.objects.create(tag = el))
                    else:
                        # если такой тег есть в таблице, то находим его и запоминаем
                        # чтобы потом с ним связать заметку
                        tag = Tag.objects.get(tag = el)
                        tags_list.append(tag)
            # связываем все теги с заметкой
            for tag in tags_list:
                tag.note.add(note)  
        
        return redirect(reverse('addressbook:add-contact'))
    return render(request, 'addressbook/add_contact.html', content)
    
def edit_contact():
    pass
    #return render(request, 'addressbook/edit_contact.html', content)

def birthdays(request):
    '''The first page  after authentication.
    There will be list of friends, 
    who has birthday in the near future
    ordered
    '''
    period = 50
    # даты будут сравниваться как кортежи (месяц, день)
    date_begin = date.today()
    date_end = date_begin + timedelta(days = period)
    date_begin = (date_begin.month, date_begin.day)
    date_end = (date_end.month, date_end.day)

    abonents = Abonent.objects.filter(owner = request.user, 
                birthday__isnull = False )
    abonents_list = []
    #  из полученного полного запроса переписываются в список только подходящие
    for abonent in abonents:
        if date_begin<(abonent.birthday.month, abonent.birthday.day)<date_end:
            abonents_list.append({'pk': abonent.id,
                                    'name': abonent.name,
                                'birthday' : abonent.birthday,
                                'short_bd': (abonent.birthday.month, abonent.birthday.day),
                                'str_bd': abonent.birthday.strftime('%A %d %B %Y')})
    #сортировка по (месяц, день)
    abonents_list.sort(key=lambda el: el['short_bd'])
    content = {
        'abonents': abonents_list,
    }
    return render(request, 'addressbook/birthdays.html', content)

def home(request):
    ''' The first page of Addressbook
    List of all contacts of user
    '''
    all_abonent = Abonent.objects.filter(owner = request.user)
    content = {
        'abonents': all_abonent,
    }
    return render(request, 'addressbook/home.html', content)