from django.db import models

# Create your models here.

class completed(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text
        
class found_automatic(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text

class last_checked_number(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text

class multi_user(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text

class not_a_valid_number(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text

class semi_found(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text

class error(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text

class running_status(models.Model):
    is_running = models.BooleanField(default=False)

    def __str__(self):
        return str(self.is_running)