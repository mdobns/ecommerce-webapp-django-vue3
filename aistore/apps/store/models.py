from io import BytesIO
from django.core.files import File
from django.db import models
from PIL import Image

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    ordering = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('ordering',)

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    price = models.FloatField()

    num_available = models.IntegerField(default=1)

    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    dateadded = models.DateTimeField(auto_now_add=True)

    

    class Meta:
        ordering = ('-dateadded',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Save the original image first
        super().save(*args, **kwargs)

        if self.image:
            # Regenerate thumbnail if missing or image has changed
            if not self.thumbnail or self.image_has_changed():
                self.thumbnail = self.make_thumbnail(self.image)
                super().save(update_fields=['thumbnail'])

    def image_has_changed(self):
        if not self.pk:
            return True
        old = Product.objects.get(pk=self.pk)
        return old.image != self.image

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img = img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)
        return thumbnail

class productImage(models.Model):
    product = models.ForeignKey("Product", related_name='images', on_delete=models.CASCADE)
    
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        # Save the original image first
        super().save(*args, **kwargs)

        if self.image:
            # Regenerate thumbnail if missing or image has changed
            if not self.thumbnail or self.image_has_changed():
                self.thumbnail = self.make_thumbnail(self.image)
                super().save(update_fields=['thumbnail'])

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img = img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)
        return thumbnail
