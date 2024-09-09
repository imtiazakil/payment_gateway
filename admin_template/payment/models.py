from django.db import models

# Create your models here.
class Payment(models.Model):
    STATUS_CHOICES = (
        (0, 'Unpaid'),
        (1, 'Paid'),
    )
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tran_id = models.CharField(max_length=100, unique=True)
    response_data = models.JSONField()  # Save the API response as JSON
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)  # 0 = unpaid, 1 = paid

    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"