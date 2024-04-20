from django.db import models

# Create your models here.
from accounts.models import CustomUser
from django.core.validators import MinValueValidator 


class Department(models.Model):
    name = models.CharField(max_length = 100, null = False, blank = False)

    def __str__(self):
        return self.name
    
    
class Photo(models.Model):
    department = models.ForeignKey(Department, on_delete = models.SET_NULL, null = True, blank=True)
    image = models.ImageField(null = False, blank = False)
    description = models.TextField()

    def __str__(self):
        return self.description
    
    
class Product(models.Model):
    CONDITION_CHOICES = [
        ('pre_owned', 'Pre-owned'),
        ('new_with_box', 'New with Box'),
        ('new_without_box', 'New without Box'),
        ('new_with_defects', 'New with Defects'),
    ]

    title = models.CharField(max_length=255, null=False, blank=False)
    brand = models.CharField(max_length=255, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='products')
    price = models.FloatField(default=0.0, validators =[MinValueValidator(0.0)])
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='Pre-owned')
    description = models.TextField()
    product_id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='products')
    # image = models.ImageField(upload_to='product_images/', default='https://png.pngtree.com/png-clipart/20190918/ourmid/pngtree-load-the-3273350-png-image_1733730.jpg')


    def __str__(self):
        return self.title
    

def product_directory_path(instance, filename):
    print("########################################",instance)
    # Access the title of the related Product instance
    product_title_cleaned = instance.title.replace(" ", "_")
    return f'products/{product_title_cleaned}/{filename}'


class Productimage(models.Model):

    imageID = models.AutoField(primary_key=True)
    product =  models.ForeignKey(Product, on_delete=models.CASCADE)
    
    imageURL = models.ImageField(upload_to='product_images/', default='https://png.pngtree.com/png-clipart/20190918/ourmid/pngtree-load-the-3273350-png-image_1733730.jpg')

    ## thumbnail = models.BooleanField(default= False)

    ##imageURL = models.ImageField(upload_to=product_directory_path)

    def __str__(self):
        return f"Image {self.imageID} of Product {self.product_id}"
    
    
class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)  # Optional: Link to user model
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.email} on {self.product.title}"  # Adjust based on your User model fields

