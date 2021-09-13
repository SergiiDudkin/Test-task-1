from django.contrib import admin
from colleagues.models import Profile

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'position', 'salary', 'unused_vacation_days', 'photo')

admin.site.register(Profile, ProfileAdmin)
