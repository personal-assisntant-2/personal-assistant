from django import forms
from django.core.exceptions import ValidationError


def file_size(value): # add this to some file where you can import it from
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MiB.')


class UploadFileForm(forms.Form):
    file = forms.FileField(
        validators=[file_size],
        label='Upload file'
    )


CATEGORY_CHOICES = (
    ('audio', 'Audios'),
    ('archive', 'Archives'),
    ('doc', '"Documents'),
    ('img', 'Images'),
    ('video', 'Video'),
    ('others', 'Others')
)


class CategoryForm(forms.Form):
    category_field = forms.ChoiceField(
        choices=CATEGORY_CHOICES
    )

