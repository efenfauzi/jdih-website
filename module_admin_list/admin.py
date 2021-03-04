from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin

from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from module_admin_list.models import UserJDIHCostum, GroupPermission, PermissionList

from django.contrib.auth.models import Permission

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserJDIHCostum
        fields = ('email', 'username')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label=("Password"),
                    help_text=("Demi keamanan passwords disimpan dalam bentuk hashing. "
                    "Anda dapat mengubah password dengan mengklik link "
                    "berikut <a href=\"../password/\">ubah password</a>."))

    # user_permissions = forms.ModelMultipleChoiceField(
    #                 Permission.objects.filter(content_type__app_label__startswith='module'), 
    #                 widget=admin.widgets.FilteredSelectMultiple(('permissions'), False))



    class Meta:
        model = UserJDIHCostum
        fields = ('username', 'name', 'email', 'password')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'name', 'email', 'is_admin', 'hak_akses')
    list_filter = ('is_admin',)
    fieldsets = (
                (None, {'fields': ('email', 'password')}),
                ('Personal info', {'fields': ('username',)}),
            )
    fieldsets_perm = (('Permissions', {'fields': ('is_admin','groups')}),)
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'name', 'email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups',)

    def get_fieldsets(self, request, obj=None):
        if obj:
            if obj.is_superuser:
                fieldsets = self.fieldsets
            else:
                fieldsets = self.fieldsets + self.fieldsets_perm
        else:
            fieldsets = self.add_fieldsets
        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if obj.is_superuser:
                return ('is_superuser','username')
        return self.readonly_fields

# Now register the new UserAdmin...
admin.site.register(UserJDIHCostum, UserAdmin)

# unregister the Group model from admin.
# admin.site.unregister(Group)
# class GroupInline(admin.StackedInline):
#     model = GroupPermission

# class GroupAdmin(BaseGroupAdmin):
#     pass

# admin.site.register(GroupPermission, GroupAdmin)
admin.site.unregister(Group)


class GroupInlineForm(forms.ModelForm):
    class Meta:
        model = GroupPermission
        fields = ('name', 'permissions')

    permissions = forms.ModelMultipleChoiceField(
        PermissionList.objects.filter(content_type__app_label__startswith='module').exclude(content_type__model='urlmodelresolve').exclude(codename='add_permissionlist').exclude(codename='delete_permissionlist'), 
        widget=admin.widgets.FilteredSelectMultiple(('permissions'), False))


class GroupAdmin(admin.ModelAdmin):
    form = GroupInlineForm
    search_fields = ('name',)
    ordering = ('name',)
    list_display = ('name', 'list_admin')

admin.site.register(GroupPermission, GroupAdmin)

class PermissionsListAdmin(admin.ModelAdmin):
    list_display = ('name', 'codename_info',)
    search_fields = ('name',)
    readonly_fields = ('codename_info','content_type')
    fieldsets = (
        (None, {'fields': ('name', 'codename_info', 'content_type')}),
    )
    
    def get_queryset(self, request):
        return PermissionList.objects.filter(content_type__app_label__startswith='module').exclude(content_type__model='urlmodelresolve').exclude(codename='add_permissionlist').exclude(codename='delete_permissionlist')

admin.site.register(PermissionList, PermissionsListAdmin)