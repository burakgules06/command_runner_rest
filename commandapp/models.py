from django.db import models

STATUS_CHOICES = [
    (0, 'Başarılı'),
    (1, 'Başarısız'),
    (2, 'Devam Ediyor')
]
class Command(models.Model): #Command
    # command execution/start date
    # command fnish/executed date
    command = models.CharField(max_length=100)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)  #0basarısız 1basarili 2devamediyor
    output_file = models.FileField()  #output_file
    command_start_date = models.DateTimeField(auto_now_add=True)
    command_end_date = models.DateTimeField(auto_now_add=True)
