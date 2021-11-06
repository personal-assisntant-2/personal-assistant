"""The module is designed to create fake users and fill their address books with fake entries."""

from faker import Faker
from django.contrib.auth.models import User

fake = Faker()


def create_face_user(num: int, password: str = '111'):

    for _ in range(num):
        first_name = fake.first_name()
        last_name = fake.last_name()
        user = User.objects.create_user(username=first_name + ' ' + last_name,
                                        email=fake.ascii_email(),
                                        password=password)
