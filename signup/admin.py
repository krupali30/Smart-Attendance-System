from django.contrib import admin
from .models import Register
from .models import Profile
from .models import Profile_Out

# Register your models here.
admin.site.register(Register)
admin.site.register(Profile)
admin.site.register(Profile_Out)