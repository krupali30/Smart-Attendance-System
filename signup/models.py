from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Register(models.Model):
    # name=models.CharField(max_length=100)
    # email=models.EmailField()
    # password=models.CharField(max_length=32)
    # c_password=models.CharField(max_length=32)

    username=models.ForeignKey(User, on_delete=models.CASCADE)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    add=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    zip_code=models.IntegerField()
    city=models.CharField(max_length=100)
    email=models.EmailField()
    p_no=models.PositiveBigIntegerField()
    aadhar_no=models.PositiveBigIntegerField()
    profession=models.CharField(max_length=200)
    salary=models.IntegerField()
    join_date=models.DateField()
    pro_pic=models.ImageField(upload_to='dataset')

    def __str__(self):
        return "%s" %(self.first_name)


class Profile(models.Model):
    # username=models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    name=models.CharField(max_length=100)
    date=models.DateField()
    time=models.TimeField()
    attendance=models.BooleanField(blank=False,null=False,default='True')
    abnormal=models.BooleanField(blank=False,null=False,default='False')

    def __str__(self):
        return "%s" %(self.name)

class Profile_Out(models.Model):
    # username=models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    name=models.CharField(max_length=100)
    date=models.DateField()
    time=models.TimeField()
    attendance=models.BooleanField(blank=False,null=False,default='True')
    abnormal=models.BooleanField(blank=False,null=False,default='False')

    def __str__(self):
        return "%s" %(self.name)
