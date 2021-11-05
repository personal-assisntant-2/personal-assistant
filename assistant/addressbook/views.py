from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.urls import reverse
from django.template import loader
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User


from .forms import AbonentForm
from .models import Abonent, Phone, Email, Note, Tag



def add_contact(request):
    from django.contrib.auth import login, logout, authenticate
    #user = User.objects.get(pk=1)
    #print(user.username)
    #user = authenticate(request, username=user.username, password=user.password) 
    #login(request, user)
    tags = Tag.objects.all()
    if request.method == 'POST':
        data = dict(request.POST)
        print('type data', type(data['name']))
        abonent = Abonent.objects.create(
            owner_id= request.user.id,
            name = data['name'][0],
            birthday = data['birthday'][0],
            address = data['address'][0])
        
        for el in data['phone']:
            print('phone', el)
            if el:
                ph= Phone.objects.create(
                    abonent_id = abonent.id,
                    phone = int(el)
                )
                print('---saved phone---', ph)
        for el in data['email']:
            print('email', el)
            if el:
                em = Email.objects.create(
                    abonent_id = abonent.id,
                    email = el
                )
                print('---saved email', em)   
        if data['note'] :
            tags_list = []
            for el in data['tag']:
                if el:
                    tags_list.append(Tag.objects.create(
                        tag = el
                    ))
            note = Note.objects.create(
                abonent_id = abonent.id,
                note = data['note'][0]
                )
            for tag in tags_list:
                tag.note.add(note)  
        
        return redirect(reverse('addressbook:add-contact'))
    content = {'tags': [tag.tag for tag in tags]}
    print('------tagss', content['tags'])
    return render(request, 'addressbook/add-contact.html', content)
    


def home(request):
    all_abonent = Abonent.objects.all()
    template = loader.get_template("addressbook/home.html")
    context = {
        'result': all_abonent
    }
    return HttpResponse(template.render(context, request))