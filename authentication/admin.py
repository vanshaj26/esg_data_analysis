from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from authentication import models

# Register your models here.


class UserAdmin(BaseUserAdmin):
    ordering = ['created_on','f_name']
    list_display = [
        'email',
        'f_name',
        'l_name',
        'tenant',
        'user_type'
        
    ]

    list_filter = ('tenant',)
    search_fields = ('f_name', 'l_name', 'email')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('personal Info'),
            {
                'fields': (
                    'f_name',
                    'l_name',
                    'tenant',
                    'user_type'
                )
            }
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_superuser',
                    'is_staff',
                    'is_active',
                    'f_login'
                )
            }
        ),
        (
            _('Important Dates'),
            {
                'fields': (
                    'created_on',
                    'last_login',
                    'updated_on'
                )
            }
        ),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ( 'email',
                        'f_name',
                        'l_name',
                        'password1',
                        'password2',
                        'user_type',
                        'tenant',
                        'f_login')
        }),
    )

admin.site.register(models.User, UserAdmin)
