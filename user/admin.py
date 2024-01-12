from django.contrib import admin
from .models import *

# Register your models here.
class contactusAdmin(admin.ModelAdmin):
    list_display =('id','Name','Mobile','Email','Message')
admin.site.register(contactus,contactusAdmin)

class categoryAdmin(admin.ModelAdmin):
    list_display=('id','Name','Cpic')
admin.site.register(category,categoryAdmin)


class maincatAdmin(admin.ModelAdmin):
    list_display = ('id','Name','picture','cdate')
admin.site.register(maincate,maincatAdmin)


class myproductAdmin(admin.ModelAdmin):
    list_display = ('id','mcategory','pprice','dprice','psize','pcolor','pdes','pdel','ppic','pdate','pcategory')
admin.site.register(myproduct,myproductAdmin)



class registerAdmin(admin.ModelAdmin):
    list_display = ('name','email','mobile','ppic','passwd','address')
admin.site.register(register,registerAdmin)


class mcartAdmin(admin.ModelAdmin):
    list_display = ('id','userid','pid','cdate','status')
admin.site.register(mcart,mcartAdmin)


class morderAdmin(admin.ModelAdmin):
    list_display = ('id','userid','pid','remark','odate','status')
admin.site.register(morder,morderAdmin)

