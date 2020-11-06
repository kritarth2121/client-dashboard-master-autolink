from django.contrib import admin

# Register your models here.
from .models import Feed,Profile,Work,Project,Note,MyModelAdmin
admin.site.register(Feed)
admin.site.register(Profile)
admin.site.register(Work,MyModelAdmin)
admin.site.register(Project,MyModelAdmin)
admin.site.register(Note)

