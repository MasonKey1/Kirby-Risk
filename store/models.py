from django.conf import settings                                                                                                    # use a custom user model referenced in settings.py
from django.db import models
from django.urls import reverse

# Create your models here.
class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)                                                    # only return the objects with is_active=True


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)                                                                          # db_index=True => improve performance as it is frequently queried
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])                                                                     # reverse => redirect to the url with parameters

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)                                        # category.product.all() instead of category.product_set.all()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='product_creator')              # user.product_creator.all() instead of user.product_set.all()
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, default='admin')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', )
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()                                                                                                      # overwite the default objects function
    products = ProductManager()                                                                                                     # all() function will also go to ProductManager()

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])                                                                    # reverse => redirect to the url with parameters

    def __str__(self):
        return self.title
