from digilocker import models

# models.last_checked_number.objects.create("789456").save()

last = models.last_checked_number.objects.last().text

print(last)