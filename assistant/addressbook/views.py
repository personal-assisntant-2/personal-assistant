from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.template import loader
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


from .forms import AbonentForm, FindContactsForm
from .models import Abonent, Phone, Email, Note, Tag
from .queries import read_abonents


class AbonentDetailView(DetailView):
    model = Abonent
    print('----')
    #template_name = 'addressbook/detail.html'
    context_object_name = 'abonent'

    def get_context_data(self, **kwargs):
        #print('----', get_template_names(self))
        context = super().get_context_data(**kwargs)
        # print(vars(context['abonent']))
        context['phones'] = Phone.objects.filter(
            abonent_id=context['abonent'].id)
        context['emails'] = Email.objects.filter(
            abonent_id=context['abonent'].id)
        context['notes'] = Note.objects.filter(
            abonent_id=context['abonent'].id)
        print('-----', dir(context['phones']))
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


def add_contact(request):
    ''' форма добавления контакта
    есть все поля из всех моделей.
    имя
    день рождения
    адрес
    телефон - 3
    email - 3
    заметка 
    tag  - 2
    вручную создаются записи в всех таблицах.
    валидация еще не прописана 
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
            owner_id=request.user.id,
            name=data['name'][0],
            birthday=data['birthday'][0],
            address=data['address'][0])
        # создаются записи в Phone
        for el in data['phone']:
            print('phone', el)
            if el:
                ph = Phone.objects.create(
                    abonent_id=abonent.id,
                    phone=int(el)
                )
        # создаются записи в Email
        for el in data['email']:
            print('email', el)
            if el:
                em = Email.objects.create(
                    abonent_id=abonent.id,
                    email=el
                )
        # если заметки есть, то добавляем заметку в таблицу  Note
        if data['note']:
            note = Note.objects.create(
                abonent_id=abonent.id,
                note=data['note'][0]
            )
            # создаем список тегов из формы, чтобы потом к ним привязать заметку
            tags_list = []
            for el in data['tag']:
                # поле тега может быть пустым, тогда пропускаем его
                if el:
                    # если тега нет в таблице  Tag  , то создаем там запись
                    if el not in content['tags']:
                        tags_list.append(Tag.objects.create(tag=el))
                    else:
                        # если такой тег есть в таблице, то находим его и запоминаем
                        # чтобы потом с ним связать заметку
                        tag = Tag.objects.get(tag=el)
                        tags_list.append(tag)
            # связываем все теги с заметкой
            for tag in tags_list:
                tag.note.add(note)

        return redirect(reverse('addressbook:add-contact'))
    print('---')
    return render(request, 'addressbook/add-contact.html', content)


def edit_contact():
    pass


def home(request):
    #url = ' /deta i l / % ( p k ) d/ '
    all_abonent = Abonent.objects.all()
    #template = loader.get_template("addressbook/home.html")
    content = {
        'abonents': all_abonent
    }
    for ab in all_abonent:
        # print(ab)
        x = ab.phones
        print('-', x)
        print('--', x.values())
        print('---', dir(x))
    # return HttpResponse(template.render(context, request))
    print('-------', reverse('addressbook:home'))
    return render(request, 'addressbook/home.html', content)


@login_required()
def find_contacts(request):
    """предоставляет форму ввода, в которую можно ввести следующие поисковые атрибуты:
    - паттерн (поиск совпадения по всем текстовым полям (имя, адрес, телефон, email, note)),
    - даты (при поиске учитывает даты рождения и даты создания заметок). Варианты поиска:
        - совпадение с конкретной датой
        - до какой-то даты (включая ее)
        - после какой-то даты (включая ее)
        - между какими-то датами (включая эти даты)
    - тэги (при поиске просматирваются поля "tag" привязанные к note)
    Если при поиске введено несколько поисковых атрибутов, то модель 
    поиска "<атрибут 1> and <атрибут 2> and <атрибут 3>"
    Результат поиска в виде списка соовествующих записей в кратком представлении 
    (каждая запись - ссылка, при нажатии на которую осуществляется переход на страницу 
    записи с детальной информацией)
    """
    if request.method == 'POST':
        form = FindContactsForm(request.POST)
        if form.is_valid():
            res = form.cleaned_data
            user = request.user
            print('user: ', user)
            abonents = read_abonents(user,
                                     pattern=res['pattern'], tags=res['tags'], date_start=res['date_start'], date_stop=res['date_stop'])
            print(abonents)

            content = {'form': form, 'abonents': abonents}
            return render(request, "addressbook/find-contacts.html", content)
    else:
        form = FindContactsForm()

    return render(request, "addressbook/find-contacts.html", {'form': form})
