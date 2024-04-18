# Inside your app's signals.py file
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ProductTable

@receiver(post_save, sender=ProductTable)
def create_default_products(sender, instance, created, **kwargs):
    if created:
        default_products = ['Branding', 'Design', 'SMM', 'Website', 'CRM', 'Google Adds', 'Meta Adds', 'Video Editing', 'Marketing']  # Define your default product names here
        for product_name in default_products:
            ProductTable.objects.get_or_create(Product_Name=product_name)
