from django.contrib.auth.base_user import BaseUserManager
  
class CustomUserManager(BaseUserManager):
    def create_user(self, customID, password=None, **extra_fields):
        if not customID:
            raise ValueError('The Email field must be set')
        user = self.model(customID=customID, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, customID, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(customID, password, **extra_fields)