from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

CERTIFICATE = (
    ('Insurance', 'Insurance'),
    ('Fitness', 'Fitness'),
    ('Pollution', 'Pollution')
    )


class TruckDetails(models.Model):
	truck_name= models.CharField(max_length=15, unique=True)
	truck_number = models.CharField(max_length=12)
	truck_owner= models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return '{}'.format(self.truck_name)


class Certificate(models.Model):
	certificate_name  = models.CharField(max_length=20, choices=CERTIFICATE)
	expire_date=models.DateField()
	truck_name=models.ForeignKey(TruckDetails,on_delete=models.CASCADE)

	def __str__(self):
		return '{}'.format(self.certificate_name)



class Notifications(models.Model):
	"""docstring for notifications"""
	certificate_name=models.ForeignKey(Certificate,on_delete=models.CASCADE)
	notice1=models.BooleanField(default=False)
	notice2=models.BooleanField(default=False)
	notice3=models.BooleanField(default=False)
	read1=models.BooleanField(default=False)
	read2=models.BooleanField(default=False)
	read3=models.BooleanField(default=False)
	time1 = models.DateTimeField(default=timezone.now)
	time2 = models.DateTimeField(default=timezone.now)
	time3 = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return '{}'.format(self.certificate_name)