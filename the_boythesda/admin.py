from django.contrib import admin

# Register your models here.
from the_boythesda.models import Game, Publisher, Genre, SysReq

#admin.site.register.html(Game)
admin.site.register(Publisher)
admin.site.register(Genre)
#admin.site.register.html(SysReq)


@admin.register(Game)
class AdminGame(admin.ModelAdmin):
    list_display = ('title', 'summary')
    ordering = ['title', 'releaseDate']


@admin.register(SysReq)
class AdminSysReq(admin.ModelAdmin):
    list_display = ('HDD', 'CPU', 'GPU', 'DDR')
