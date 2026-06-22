from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Recruteur, Etudiant

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'type_utilisateur', 'is_staff', 'is_active')
    list_filter = ('type_utilisateur', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'type_utilisateur')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'type_utilisateur', 'password1', 'password2')}),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(Recruteur)
admin.site.register(Etudiant)
