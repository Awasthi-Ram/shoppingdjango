from django.db import models

# Create your models here.

class Product(models.Model):
    product_id = models.AutoField  #interfield hai jo ki auto metically increment hoti hai (primary firld is automaticalli is in the model by default no need to add)
    product_name = models.CharField('Name', max_length=50)
    category = models.CharField(max_length=50,default="")
    subcategory = models.CharField(max_length=50,default="")
    price = models.DecimalField("Price", decimal_places=2, max_digits=5000000)
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/images",default="")
    
    def __str__(self):
       return self.product_name

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)  #interfield hai jo ki auto metically increment hoti hai (primary firld is automaticalli is in the model by default no need to add)
    name = models.CharField('Name', max_length=50)
    email = models.EmailField(max_length=50,default="")
    desc = models.TextField(max_length=500)
    
    
    def __str__(self):
       return self.name
    

class orders(models.Model):
    order_id = models.AutoField(primary_key=True)  #interfield hai jo ki auto metically increment hoti hai (primary firld is automaticalli is in the model by default no need to add)
    iteams_json = models.CharField( max_length=50000)
    name = models.CharField( max_length=90)
    email = models.EmailField(max_length=50)
    address = models.TextField(max_length=500)
    city = models.CharField( max_length=90)
    state = models.CharField( max_length=90)
    zip_code = models.CharField( max_length=90)
    
    
    def __str__(self):
       return self.name