from django.contrib import admin
from .models import CustomUser, Role, BusinessElement, AccessRule

# I tried to hash passwords manually using bcrypt,
# but then I couldn’t log into the Django admin.
# Turns out Django expects passwords to be hashed its own way.

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'role')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(BusinessElement)
class BusinessElementAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(AccessRule)
class AccessRuleAdmin(admin.ModelAdmin):
    list_display = (
        'role', 'element',
        'read_my_permission', 'read_all_permission',
        'create_my_permission', 'create_all_permission',
        'update_my_permission', 'update_all_permission',
        'delete_my_permission', 'delete_all_permission',
    )
    list_filter = ('role', 'element')
    search_fields = ('role__name', 'element__name')
