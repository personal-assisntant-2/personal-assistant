from .models import UploadedFiles


def create_uploaded_file(name: str, extension: str, file: bytes, user, size: int) -> UploadedFiles:
    uploaded_file = UploadedFiles.objects.create(
            name=name,
            extension=extension,
            file=file,
            user=user,
            size=size
        )


def normalize(text):
    """
    if the text contains Cyrillic letters, then the function replaces them with the Latin.
    :return: updated text.
    """
    CYRILLIC = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    LATIN = ['a', 'b', 'v', 'g', 'd', 'e', 'ye', 'zh', 'z', 'i', 'y', 'k', 'l', 'm', 'n', 'o',
             'p', 'r', 's', 't', 'u', 'f', 'kh', 'ts', 'ch', 'sh', 'shch', '', 'y', '', 'e', 'yu', 'ya']

    TRANSLIT_DICT = dict()
    for c, l in zip(CYRILLIC, LATIN):
        TRANSLIT_DICT[ord(c)] = l
        TRANSLIT_DICT[ord(c.upper())] = l.upper()
    translated_text = text.translate(TRANSLIT_DICT)

    return translated_text
