from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "first_name", "last_name", "age", "get_email")
    search_fields = ("first_name", "last_name", "user__email")

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = "Email"
