
from django.contrib import admin
from django.contrib.auth import get_user_model

UserModel = get_user_model()


@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_superuser",
        "is_staff",
        "created_at",
    )
    list_filter = (
        "is_staff",
        "is_superuser",
    )
