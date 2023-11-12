from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
	def create_user(self, email, password=None, **extra_fields):
		if not email:
			raise ValueError('An email is required.')
		if not password:
			raise ValueError('A password is required.')
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save()
		return user
	
    # using django email config for drf to see if it will work
	def create_superuser(self, email, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		
		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True')
		
		# if not email:
		# 	raise ValueError('An email is required.')
		# if not password:
		# 	raise ValueError('A password is required.')
		# user = self.create_user(email, password, **extra_fields)
		# user.save()
		return self.create_superuser(email, password, **extra_fields)


class CustomUser(AbstractUser):
	email = models.EmailField(max_length=50, unique=True)
	username = None
	

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
	objects = CustomUserManager()
	
	# changing the related_name to avoid clashes with reverse
    # for user groups and user_permissions
	groups =models.ManyToManyField('auth.Group', related_name='auth_groups', blank=True)
	user_permissions = models.ManyToManyField('auth.Permission', related_name='auth_user_permissions', blank=True)


	def __str__(self):
		return self.email


# from django.db import models
# from django.contrib.auth.base_user import BaseUserManager
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# class AppUserManager(BaseUserManager):
# 	def create_user(self, username, email, password=None):
# 		if not email:
# 			raise ValueError('An email is required.')
# 		if not password:
# 			raise ValueError('A password is required.')
# 		email = self.normalize_email(email)
# 		user = self.model(username=email).rstrip[0]
# 		user = self.model(email=email)
# 		user.set_password(password)
# 		user.save()
# 		return user
# 	def create_superuser(self, email, password=None):
# 		if not email:
# 			raise ValueError('An email is required.')
# 		if not password:
# 			raise ValueError('A password is required.')
# 		user = self.create_user(email, password)
# 		user.is_superuser = True
# 		user.is_active = True
# 		user.save()
# 		return user


# class AppUser(AbstractBaseUser, PermissionsMixin):
# 	user_id = models.AutoField(primary_key=True)
# 	email = models.EmailField(max_length=50, unique=True)
# 	username = models.CharField(max_length=50)
# 	USERNAME_FIELD = 'email'
# 	REQUIRED_FIELDS = ['username']
# 	objects = AppUserManager()
	
#     # renamed related fields
# 	groups =models.ManyToManyField('auth.Group', related_name='auth_groups', blank=True)
# 	user_permissions = models.ManyToManyField('auth.Permission', related_name='auth_user_permissions', blank=True)



# 	def __str__(self):
# 		return self.username
