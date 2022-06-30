from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils.translation import ugettext_lazy as _


class MyUserManager(BaseUserManager):
    def create_user(self,full_name,phonenumber,email,password=None,admin=False,active=False):
        if not full_name:
            raise ValueError(_("Please Enter Full Name !."))
        if not phonenumber:
            raise ValueError(_("Please Enter Mobile Number !."))
        if not email:
            raise ValueError(_("Please Enter Email !."))
        if not password:
            raise ValueError(_("Please Enter Password !."))
        user=self.model(email=self.normalize_email(email),
                        full_name=full_name,
                        phonenumber=phonenumber,
                        admin=admin,
                        active=active,
                        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,full_name,phonenumber,email,password=None,admin=True,active=True):
        user=self.create_user(full_name,phonenumber,email,password,admin,active)
        user.save(using=self._db)
        return user
    
   




class User(AbstractBaseUser,PermissionsMixin):
    full_name=models.CharField(max_length=255,verbose_name="Full Name")
    email=models.EmailField(unique=True,max_length=255,verbose_name="Email")
    phonenumber=models.CharField(max_length=255,verbose_name="Mobile Number",unique=True)
    admin=models.BooleanField(default=False)
    active=models.BooleanField(default=False)
    date_joined=models.DateTimeField(auto_now_add=True)
  

    USERNAME_FIELD='phonenumber'
    REQUIRED_FIELDS=['full_name','email']
    objects=MyUserManager()

    def __str__(self):
        return str(self.phonenumber)
    
    def is_active(self):
        return self.active

    def is_staff(self):
        return self.admin
    
    def is_admin(self):
        return self.admin

    def is_superuser(self):
        return self.admin
    
    def has_perm(self,perm,obj=None):
        return True
        
    def has_perms(self,perm,obj=None):
        return True

    def has_module_perms(self,app_label):
        return True




class Playlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=250)
    imdb=models.CharField(max_length=250)
    img=models.CharField(max_length=1000)
    




