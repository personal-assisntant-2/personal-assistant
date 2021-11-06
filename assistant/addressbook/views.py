import email
from django.http import HttpResponse
from random import randint, choice
from faker import Faker
from django.contrib.auth.models import User
from addressbook.models import Abonent, Phone, Email, Note, Tag

fake = Faker()


def create_face_user(num: int, password: str = '111',
                     abonents_min: int = 10,
                     abonents_max: int = 100,
                     phone_max: int = 3,
                     email_max: int = 2,
                     note_max: int = 1,
                     tags_max: int = 3):

    for _ in range(num):
        first_name = fake.first_name()
        last_name = fake.last_name()
        user = User.objects.create_user(username=first_name + ' ' + last_name,
                                        email=fake.ascii_email(),
                                        password=password)
        user.save()

        for _ in range(randint(abonents_min, abonents_max)):
            abonent = Abonent(name=fake.name(),
                              birthday=fake.date_between(
                                  start_date='-80y', end_date='-10y'),
                              address=fake.address(),
                              owner=user)
            abonent.save()
            for _ in range(randint(0, phone_max)):
                phone = Phone(phone=fake.phone_number(),
                              abonent=abonent)
                phone.save()

            for _ in range(randint(0, email_max)):
                email = Email(email=fake.ascii_email(),
                              abonent=abonent)
                email.save()

            for _ in range(randint(0, note_max)):
                note = Note(note=fake.sentence(
                    nb_words=10, variable_nb_words=True),
                    date=fake.date_between(start_date='-5y', end_date='today'),
                    abonent=abonent)
                note.save()
                for _ in range(randint(0, tags_max)):
                    tag = choice(Tag.objects.all())
                    tag.note.add(note)
                # Create your views here.


def fake_user(request):
    create_face_user(5)
    return HttpResponse('фейкове пользователи созданы')
