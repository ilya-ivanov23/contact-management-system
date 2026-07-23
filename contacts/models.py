from django.db import models
from django.core.validators import RegexValidator

class ContactStatusChoices(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'Contact Status Choices'

    def __str__(self):
        return self.name

class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', 
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=100)
    
    status = models.ForeignKey(ContactStatusChoices, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
