from django.db import models

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.IntegerField()  # e.g., 10 for 10%
    active = models.BooleanField(default=True)
    available_quantity = models.PositiveIntegerField(default=1)  # Number of uses left
    used_quantity = models.PositiveIntegerField(default=0)  # Number of times used

    def is_valid(self):
        return self.active and self.available_quantity > 0
 
    def use(self):
        if self.is_valid():
            self.used_quantity += 1
            if self.used_quantity >= self.available_quantity:
                self.active = False
            self.save()
            return True
        return False

        
    def __str__(self):
        return self.code
