from django.db import models
    


class Credit(models.Model):

    TYPE_DNI_CHOICES  = [
        ('cc', 'Cedula'),
        ('id', 'Identificacion'),
    ]

    full_name = models.CharField(max_length=100)
    type_dni = models.CharField(max_length=100, choices=TYPE_DNI_CHOICES )
    dni = models.CharField(max_length=100)
    credit_value = models.FloatField()
    interests = models.FloatField()
    months = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'credit'

    def __str__(self):
        return self.full_name