from django.db import models


class Make(models.Model):
    name = models.CharField(max_length=50, unique=True)
    logo = models.ImageField(upload_to='make_logo/', blank=True)
    
    
    class Meta:
        verbose_name_plural = "Car Maker"
        
    def __str__(self):
        return self.name
    
    
class Model(models.Model):
    make = models.ForeignKey(Make, on_delete=models.CASCADE, related_name="make")
    name = models.CharField(max_length=100)
    
    
    class Meta:
        verbose_name_plural = "Car Models"
    
    def __str__(self):
        return self.name
    
    
class Car(models.Model):
    TRANSMISSION_CHOICES = [
        ("manual", "Manual"),
        ("automatic", "Automatic"),
    ]

    FUEL_CHOICES = [
        ("petrol", "Petrol"),
        ("diesel", "Diesel"),
        ("electric", "Electric"),
        ("hybrid", "Hybrid") 
    ]
    
    STATUS_CHOICES = [
        ("upcoming", "Upcoming"),
        ("active", "Active"),
    ]
    
    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name="model")
    year = models.IntegerField(default=2000)
    vin = models.CharField(max_length=17, unique=True)
    kilometers = models.PositiveIntegerField()
    engine_size = models.CharField(max_length=20)
    transmission = models.CharField(choices=TRANSMISSION_CHOICES, max_length=50)
    fuel_type = models.CharField(choices=FUEL_CHOICES, max_length=50)
    color = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, default="upcoming", max_length=50)
    starting_price = models.DecimalField(max_digits=12, decimal_places=2)
    current_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    auction_start_date = models.DateTimeField(auto_now_add=False)
    auction_end_date = models.DateTimeField(auto_now_add=False)
    
    class Meta:
        verbose_name_plural = "Cars"

    def __str__(self):
        return self.model.name
    
    
class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="car_image")
    image = models.ImageField(upload_to="car_images/", blank=True)