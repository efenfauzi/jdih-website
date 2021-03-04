from django.db import models
from django.contrib.auth.models import (
	BaseUserManager, AbstractBaseUser, Group, PermissionsMixin,
	Permission
)
from django.utils.html import format_html

class PermissionList(Permission):

	def trans_name(self):
		if "can delete" in self.name.lower():
			new_name = self.name.lower().split("can delete")[-1]
			return "Hapus %s" %new_name
		if "can add" in self.name.lower():
			new_name = self.name.lower().split("can add")[-1]
			return "Tambah %s" %new_name
		if "can view" in self.name.lower():
			new_name = self.name.lower().split("can view")[-1]
			return "Tampil %s" %new_name
		if "can change" in self.name.lower():
			new_name = self.name.lower().split("can change")[-1]
			return "Edit %s" %new_name
	trans_name.short_description = 'List Rule Permission'

	def __str__(self):
		return '%s' % (self.name)

	def codename_info(self):
		return self.codename
	codename_info.short_description = 'Fungsi Module'

	class Meta:
		proxy = True
		verbose_name = "Permission List"
		verbose_name_plural = "Permission List"


class GroupPermission(Group):

	class Meta:
		db_table = 'jdih_admin_permissions'
		verbose_name_plural = 'Group Permissions'
		verbose_name = 'Group Permissions'

	def list_admin(self):
		html = ''
		users = UserJDIHCostum.objects.filter(groups__name=self.group_ptr)
		for x in users:
			html += f"<li>{x.username} | {x.email}</li>"
		return format_html(html)


class AdminUserManager(BaseUserManager):
	def create_user(self, email, username, name, password=None):
		"""
		Creates and saves a User with the given email, date of
		birth and password.
		"""
		if not email:
		    raise ValueError('Users must have an email address')

		user = self.model(
		    email=self.normalize_email(email),
		    username=username,
		    name=name,

		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, name, password=None):
		"""
		Creates and saves a superuser with the given email, date of
		birth and password.
		"""
		user = self.create_user(
		    email,
		    password=password,
		    username=username,
		    name=name,
		)
		user.is_admin = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class UserJDIHCostum(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(
		verbose_name='email address',
		max_length=255,
		unique=True,
		help_text="Alamat email pengguna"
	)
	username = models.CharField(
				max_length=20, unique=True, 
				help_text="Nama Pengguna adalah username yang harus unik tidak diperbolehkan duplikat",
				verbose_name="Nama Pengguna")
	name = models.CharField(max_length=50, help_text="Nama Lengkap Pengguna", verbose_name="Nama Lengkap")
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False, help_text="Status sebagai admin yang dapat menginput data system", verbose_name="Status admin")
	is_superuser = models.BooleanField(default=False)
	user_permissions = models.ManyToManyField(PermissionList, blank=True)

	objects = AdminUserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email', 'name']

	def __str__(self):
		return self.username

	# def has_perm(self, perm, obj=None):
	# 	"Does the user have a specific permission?"
	# 	# Simplest possible answer: Yes, always
	# 	return True

	# def has_module_perms(self, app_label):
	# 	"Does the user have permissions to view the app `app_label`?"
	# 	# Simplest possible answer: Yes, always
	# 	return True

	@property
	def is_staff(self):
		"Is the user a member of staff?"
		# Simplest possible answer: All admins are staff
		return self.is_admin

	class Meta:
		db_table = 'jdih_admin'
		verbose_name_plural = 'Admin List'
		verbose_name = 'Admin List'


	def hak_akses(self):
		# print(dir(self.groups))
		html = ''
		as_group_admin = self.groups.filter(user=self.id)
		if as_group_admin.count() >= 1:
			for x in as_group_admin:
				html += f"<li>{x}</li>"
			return format_html(html)
		else:
			if self.is_superuser is True:
				return format_html("""<span class="badge" style="background: red">Superadmin</span>""")
			return "belum memiliki permissions admin"
