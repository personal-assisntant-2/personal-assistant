
from models import Abonent, Phone, Email, Note, Tag
from django.db.models import Q


def read_abonents(pattern: str = '', tags: list = [], date_min: date = None, date_max: date = None) -> list:
    """Ищет и возвращает список экземпляров записей типа Abonent, соотвествующих параметрам поиска.
    Параметры поиска задаются паттерном 'pattern', списком tags и временным интервалом date_min ... date_max. 
    Если  pattern == '' (пустая строка - состояние по умолчанию), поиск осуществляется только с учетом 
    остальных параметров. Поиск по паттерну проходит по всем текстовым и строковым полям БД: name, 
    address, phone, email, note.
    Поиск по временным отметкам осуществляется по полям Abonent.birthday и Note.date (дата создания заметки)
    Поиск по временным отметкам реализуется по правилам:
    - date_min == None and date_max == None - состояние по умолчанию. Поиск по времени не осуществляется.
    - date_min == None and date_max == date - в результаты поиска включаются записи, временные отметки которых
    соотвествуют условию < date_max
    - date_min == date and date_max == None -  в результаты поиска включаются записи, временные отметки которых
    соотвествуют условию > date_min
    - date_min == date_1 and date_max == date_2 -  в результаты поиска включаются записи, временные отметки которых
    соотвествуют условию BETWEEN date_1 AND date_2 (попадающие в интервал, включая границы)
    - date_min == date_max (тип данных - date) - в выборку попадут записи в которых временные метки равны date_min
    """
    if pattern == '':
        results_patt = Abonent.objects.all()
    else:
        results_patt = Abonent.objects.filter(Q(name__icontains=pattern) |
                                              Q(phone__icontains=pattern) |
                                              Q(email__icontains=pattern) |
                                              Q(address__icontains=pattern) |
                                              Q(note__icontains=pattern))

    return results_patt
