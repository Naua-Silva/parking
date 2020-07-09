from django.db import models

class Reserve(models.Model):
	plate = models.CharField(max_length=8)
	entryTime = models.DateTimeField(auto_now_add=True)
	departureTime = models.DateTimeField(blank=True, null=True)
	time = models.TimeField(blank=True, null=True)
	In = models.BooleanField(default=True)
	paid = models.BooleanField(default=False)

	def __str__(self):
		return str(self.plate)