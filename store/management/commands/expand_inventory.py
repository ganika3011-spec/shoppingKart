from django.core.management.base import BaseCommand
from category.models import Category
from store.models import Product, Variation

class Command(BaseCommand):
    help = 'Expands the product inventory with new categories and products'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting inventory expansion...")

        # 1. Create Categories
        categories_dict = {
            'Gadgets': {'slug': 'gadgets', 'description': 'Latest premium electronics and gadgets.'},
            'Accessories': {'slug': 'accessories', 'description': 'Fashionable accessories for your daily life.'},
            'Fitness': {'slug': 'fitness', 'description': 'Gear to keep you active and healthy.'},
            'Clothing': {'slug': 'clothing', 'description': 'Stylish and comfortable apparel for every occasion.'},
        }

        cats = {}
        for name, data in categories_dict.items():
            cat, created = Category.objects.get_or_create(
                category_name=name,
                defaults={'slug': data['slug'], 'description': data['description']}
            )
            cats[name] = cat
            status = "created" if created else "already exists"
            self.stdout.write(self.style.SUCCESS(f"Category '{name}' {status}."))

        # 2. Define Products
        products_data = [
            {
                'product_name': 'AuraX Noise Cancelling Headphones',
                'slug': 'aurax-headphones',
                'description': 'Experience pure sound with AuraX. Advanced active noise cancellation and 40-hour battery life.',
                'price': 299,
                'image': 'photos/products/headphones.png',
                'stock': 50,
                'category': cats['Gadgets'],
                'variations': [
                    {'category': 'color', 'value': 'Black'},
                    {'category': 'color', 'value': 'Silver'},
                ]
            },
            {
                'product_name': 'Zenith Pro Smart Fitness Watch',
                'slug': 'zenith-pro-watch',
                'description': 'Your health at a glance. Track heart rate, sleep, and workouts with the Zenith Pro.',
                'price': 199,
                'image': 'photos/products/smartwatch.png',
                'stock': 100,
                'category': cats['Gadgets'],
                'variations': [
                    {'category': 'color', 'value': 'Space Gray'},
                    {'category': 'color', 'value': 'Rose Gold'},
                    {'category': 'size', 'value': '40mm'},
                    {'category': 'size', 'value': '44mm'},
                ]
            },
            {
                'product_name': 'Terra Minimalist Canvas Backpack',
                'slug': 'terra-backpack',
                'description': 'Durable, stylish, and sustainable. The Terra backpack is perfect for urban explorers.',
                'price': 79,
                'image': 'photos/products/backpack.png',
                'stock': 30,
                'category': cats['Accessories'],
                'variations': [
                    {'category': 'color', 'value': 'Olive'},
                    {'category': 'color', 'value': 'Sand'},
                    {'category': 'color', 'value': 'Navy'},
                    {'category': 'size', 'value': 'Small'},
                    {'category': 'size', 'value': 'Large'},
                ]
            },
            {
                'product_name': 'CloudSoft Organic Hoodie',
                'slug': 'cloudsoft-hoodie',
                'description': 'The softest hoodie you will ever own. Made from 100% certified organic cotton.',
                'price': 89,
                'image': 'photos/products/hoodie.png',
                'stock': 75,
                'category': cats['Clothing'],
                'variations': [
                    {'category': 'color', 'value': 'Cream'},
                    {'category': 'color', 'value': 'Charcoal'},
                    {'category': 'color', 'value': 'Baby Blue'},
                    {'category': 'size', 'value': 'S'},
                    {'category': 'size', 'value': 'M'},
                    {'category': 'size', 'value': 'L'},
                    {'category': 'size', 'value': 'XL'},
                ]
            },
            {
                'product_name': 'SwiftRun Performance Shorts',
                'slug': 'swiftrun-shorts',
                'description': 'Lightweight and breathable. SwiftRun shorts are designed for high-intensity training.',
                'price': 45,
                'image': 'photos/products/shorts.png',
                'stock': 150,
                'category': cats['Fitness'],
                'variations': [
                    {'category': 'color', 'value': 'Black'},
                    {'category': 'color', 'value': 'Neon'},
                    {'category': 'size', 'value': 'S'},
                    {'category': 'size', 'value': 'M'},
                    {'category': 'size', 'value': 'L'},
                    {'category': 'size', 'value': 'XL'},
                ]
            }
        ]

        # 3. Create Products and Variations
        for p_data in products_data:
            product, created = Product.objects.get_or_create(
                product_name=p_data['product_name'],
                defaults={
                    'slug': p_data['slug'],
                    'description': p_data['description'],
                    'price': p_data['price'],
                    'image': p_data['image'],
                    'stock': p_data['stock'],
                    'category': p_data['category'],
                    'is_available': True,
                }
            )
            status = "created" if created else "already exists"
            self.stdout.write(f"Product '{p_data['product_name']}' {status}.")

            # Add variations
            for var_data in p_data['variations']:
                Variation.objects.get_or_create(
                    product=product,
                    variation_category=var_data['category'],
                    variation_value=var_data['value'],
                    defaults={'is_active': True}
                )
            self.stdout.write(f"Variations for '{p_data['product_name']}' updated.")

        self.stdout.write(self.style.SUCCESS("Success: Inventory expansion complete!"))
