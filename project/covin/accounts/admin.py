from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from .models import Beneficiary


from .forms import UserAdminCreationForm, UserAdminChangeForm

User = get_user_model()



class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'admin')
    list_filter = ('admin', 'staff', 'active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
       # ('Full name', {'fields': ()}),
        ('Permissions', {'fields': ('admin', 'staff', 'active', 'groups', 'user_permissions')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

#-----------------Group stuff-------------#
#from django.contrib.contenttypes.models import ContentType
#new_group, created = Group.objects.get_or_create(name='new_group')
#ct = ContentType.objects.get_for_model(User)
#permission = Permission.objects.create(content_type=ct)

admin.site.register(User, UserAdmin)

# Remove Group Model from admin. We're not using it.
#admin.site.unregister(Group)






admin.site.register(Beneficiary)