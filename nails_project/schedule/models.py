from django.db import models

# Create your models here.


class Schedule(models.Model):
    date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    available = models.BooleanField(default=False)

    def __str__(self):
        if self.start_time and self.end_time:
            return f"{self.date.strftime('%d/%m')} {self.start_time.strftime('%H:%M')}-{self.end_time.strftime('%H:%M')}"
        else:
            return f"{self.date.strftime('%d/%m')} Not available!"
