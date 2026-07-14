from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100,unique=True)
    email = models.EmailField()
    def __str__(self):
        return self.name

class login(models.Model):
    email = models.CharField(100)
    password = models.CharField(100)
    status = models.IntegerField()
    def __str__(self):
        return self.email

class veh_listing(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    number_plate = models.CharField(max_length=20)
    brand = models.CharField(max_length=50)
    year = models.IntegerField()

    veh_type= [
        ('car', 'Car'),
        ('bike', 'Bike'),
        ('auto', 'Auto'),
        ('heavy vehicle', 'Heavy Vehicle'),
        ('other', 'Other'),
    ]

    type = models.CharField(
        max_length=20,
        choices=veh_type,
        default='car'
    )

    # identification

    # reg_number = models.CharField(max_length=20)
    # reg_no = models.CharField(max_length=20, unique=True)
    
    rc = models.ImageField(
        upload_to='rc_images/',
        null=True,
        blank=True
    )

    # pricing

    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
   

    # location
    location = models.CharField(max_length=100)
    pickup_location = models.CharField(max_length=100)

    # availability
    is_available = models.BooleanField(default=True)

    is_verified = models.BooleanField(default=False)

    # Specs
    fuel_type = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
    ]

    TRANSMISSION_TYPES = [
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
    ]

    fuel = models.CharField(
        max_length=10,
        choices=fuel_type
    )

    trans = models.CharField(
        max_length=10,
        choices=TRANSMISSION_TYPES
    )

    mileage = models.IntegerField(
    
    null=True,
    blank=True
)
        
    

    # images of the vehicle
    image1 = models.FileField(upload_to='vehicle_images/', null=True, blank=True)
    image2 = models.FileField(upload_to='vehicle_images/', null=True, blank=True)
    image3 = models.FileField(upload_to='vehicle_images/', null=True, blank=True)
    image4 = models.FileField(upload_to='vehicle_images/', null=True, blank=True)

    # #verification
    img1 = models.FileField(upload_to='verification_images/', null=True, blank=True)
    img2 = models.FileField(upload_to='verification_images/', null=True, blank=True)

        # description
    description = models.TextField()

class Booking(models.Model):

    vehicle = models.ForeignKey(
        veh_listing,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=15)

    pickup_date = models.DateField()
    return_date = models.DateField()

    total_price = models.IntegerField()

    Aadhar_number = models.CharField(max_length=20)
    license_number = models.CharField(max_length=20)
    advance_payment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    razorpay_payment_id = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    license_image = models.FileField(
        upload_to='license_images/',
        null=True,
        blank=True
    )

    aadhar_image = models.FileField(
        upload_to='aadhar_images/',
        null=True,
        blank=True
    )

    booking_status = models.CharField(
        max_length=30,
        default='Pending'
    )

class Review(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    
    rating = models.IntegerField()
    comment = models.TextField()

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    reply = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


    

    

# Create your models here.
