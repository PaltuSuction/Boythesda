from django.db import models

# Create your models here.
from django.utils.safestring import mark_safe


class Game(models.Model):
    title = models.CharField(max_length=200, help_text='Название игры', verbose_name='Название игры')
    summary = models.TextField(default='Нет описания', help_text='Описание игры', verbose_name='Описание игры')
    releaseDate = models.DateField(null=True, blank=True)
    price = models.FloatField(max_length=9999.00, default=0.0, verbose_name='Цена', help_text='Цена игры', null=True, blank=True)
    Image = models.ImageField(upload_to='gamePages/', null = True, blank=True,)
    scoreCritics = models.IntegerField(help_text='Средняя оценка критиков', null = True, blank= True)
    scoreUsers = models.IntegerField(help_text='Средняя оценка пользователей', null = True, blank = True)

    publisher = models.ForeignKey('Publisher', help_text='Издатель', on_delete=models.SET_DEFAULT, default= 'Издатель отсутствует или был удален')
    sysReq = models.ForeignKey('SysReq', verbose_name='Системные требования (Рекомендуемые)', on_delete=models.CASCADE)
    genre = models.ManyToManyField('Genre', verbose_name='Жанр(ы)')

    class Meta:
        verbose_name = 'Игра'
        db_table = 'GAME'

    def __str__(self):
        return self.title

    def summary_short(self):
        summary_list = self.summary.split(' ')
        i = len(summary_list)
        if i > 30: i = 30
        elif i == 0: return "Описания нет."
        short_sum = ' '.join(summary_list[0:i])
        return short_sum + '...'




class Publisher(models.Model):
    name = models.CharField(max_length=200, help_text='Издатель', verbose_name='Издатель', unique=True)
    summary = models.TextField(help_text='Описание издателя', null= True, blank=True, default='Нет описания')
    foundation_date = models.DateField(verbose_name='Год основания', blank=True, null = True)

    class Meta:
        db_table = 'PUBLISHER'

    def __str__(self):
        return self.name



class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name='Жанр', default='Жанр не указан', unique=True)

    class Meta:
        db_table = 'GENRE'

    def __str__(self):
        return self.name

class SysReq(models.Model):
    configuration_name = models.CharField(max_length=200, null = True, blank= True)
    HDD = models.CharField(max_length=300, help_text='Место на жестком диске', verbose_name='Место на жестком диске')
    CPU = models.CharField(max_length=300, help_text='Процессор', verbose_name='Рекоментуемый процессор')
    GPU = models.CharField(max_length=300, help_text='Видеокарта', verbose_name='Рекоментуемая видеокарта')
    DDR = models.SmallIntegerField(help_text='Объем оперативной памяти (Гб)', verbose_name='Объем оперативной памяти (Гб)')

    class Meta:
        db_table = 'SYSREQ'

    def __str__(self):
        if self.configuration_name == None:
            return 'Конфигурация #{}' .format(self.id)
        else: return self.configuration_name





