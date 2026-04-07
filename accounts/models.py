from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
import logging

logger = logging.getLogger(__name__)


class MyAccountManager(BaseUserManager):
    """Custom manager for Account model."""
    
    def create_user(self, first_name, last_name, username, email, password=None):
        """Create and save a regular user."""
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name.strip(),
            last_name=last_name.strip(),
        )
        user.set_password(password)
        user.save(using=self._db)
        logger.info(f"User created: {username}")
        return user

    def create_superuser(self, first_name, last_name, username, email, password):
        """Create and save a superuser with admin privileges."""
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        logger.info(f"Superuser created: {username}")
        return user


class Account(AbstractBaseUser):
    """Custom user model for the application."""
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True, db_index=True)
    email = models.EmailField(max_length=100, unique=True, db_index=True)
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message='Phone number must be between 9 and 15 digits.'
            )
        ]
    )

    # Status fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)  # Email confirmation required
    is_superadmin = models.BooleanField(default=False)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
        ordering = ['-date_joined']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['username']),
        ]

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        """Return user's full name."""
        return f"{self.first_name} {self.last_name}".strip()

    def has_perm(self, perm, obj=None):
        """Check if user has a specific permission."""
        return self.is_admin or self.is_superadmin

    def has_module_perms(self, app_label):
        """Check if user has permissions for an app."""
        return self.is_admin or self.is_superadmin


class UserProfile(models.Model):
    """Extended user profile for additional user information."""
    
    user = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    address_line_1 = models.CharField(max_length=100, blank=True)
    address_line_2 = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(blank=True, upload_to='userprofile/')
    city = models.CharField(max_length=30, blank=True)
    state = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=50, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"Profile of {self.user.full_name}"

    @property
    def full_address(self):
        """Return formatted full address."""
        parts = [
            self.address_line_1,
            self.address_line_2,
            self.city,
            self.state,
            self.country,
            self.postal_code,
        ]
        return ', '.join(filter(None, parts))
