from django.db import models
from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from transliterate import translit
from django.urls import reverse
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponseRedirect
from decimal import Decimal
from django.conf import  settings

import logging
logging.basicConfig(filename="sample.log", level=logging.INFO)

COLORS = [('#000000', 'Black'),
          ('#FF0000', 'Red'),
          ('#0000FF', 'Blue'),
          ('#808080', 'Gray'),
          ('#FFFFFF', 'White'),
          ('#FFC0CB', 'Pink'),
          ('#FFFF00', 'Yellow')]

def image_folder(instance, filename):
    if hasattr(instance, 'slug'):
        filename = instance.slug + '.' + filename.split('.')[1]
        return "{0}/{1}".format(instance.slug, filename)
    else:
        filename = instance.product.slug + '.' + filename.split('.')[1]
        return "{0}/{1}".format(instance.product.slug, filename)

def tmb_image_folder(instance, filename):
    if hasattr(instance, 'slug'):
        filename = 'tmb_' + instance.slug + '.' + filename.split('.')[1]
        return "{0}/{1}".format(instance.slug, filename)
    else:
        filename = 'tmb_' + instance.product.slug + '.' + filename.split('.')[1]
        return "{0}/{1}".format(instance.product.slug, filename)

class Product(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    available = models.BooleanField()
    price = height = models.DecimalField(max_digits=9, decimal_places=2)
    color = models.CharField(choices=COLORS, null=False, max_length=7)
    height = models.IntegerField()
    width = models.IntegerField()
    depth = models.IntegerField()
    subjects = models.ManyToManyField('Subject')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'product_slug': self.slug})




class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    parent_category = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)
    description = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'category_slug': self.slug})




class Subject(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    description = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.title

class ProductIMG(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    img = models.ImageField(upload_to=image_folder)
    image_thumb = models.ImageField(blank=True, upload_to=tmb_image_folder)

    def __str__(self):
        return '%s %s' % (self.product.title, self.title)


def pre_save_product_img(sender, instance, *args, **kwargs):
    size = {'height': 256, 'width': 256}
    extension = str(instance.img.path).rsplit('.', 1)[1]  # получаем расширение загруженного файла
    if extension in ['jpg', 'jpeg', 'png', 'JPG']:  # если расширение входит в разрешенный список
        im = Image.open(instance.img)  # открываем изображение
        im.thumbnail((size['width'], size['height']))
        image_file = BytesIO()
        im.save(image_file, im.format)
        instance.image_thumb.save(instance.img.name, InMemoryUploadedFile(image_file, None, '', instance.img.file.content_type, im.size, instance.img.file.charset,), save=False)







def pre_save_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(translit(instance.title, reversed=True))
        instance.slug = slug



pre_save.connect(pre_save_slug, sender=Category)
pre_save.connect(pre_save_slug, sender=Subject)
pre_save.connect(pre_save_slug, sender=Product)
pre_save.connect(pre_save_product_img, sender=ProductIMG)


class CartItem(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return 'cart item for %s' % (self.id)

class Cart(models.Model):
    items = models.ManyToManyField('CartItem')
    cart_total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    def __str__(self):
        return 'cart id %s' % (self.id)

    def add_to_cart(self, product_slug):
        cart = self
        product = Product.objects.get(slug=product_slug)
        new_item = CartItem.objects.get_or_create(product=product, item_total=product.price)
        if new_item not in cart.items.all():
            cart.items.add(new_item[0])
            cart.save()

        new_cart_total = 0.00
        for item in cart.items.all():
            new_cart_total += float(item.item_total)
        cart.cart_total = new_cart_total
        cart.save()
        return HttpResponseRedirect('cart')



    def remove_from_cart(self, product_slug):
        cart = self
        product = Product.objects.get(slug=product_slug)
        for item in cart.items.all():
            if item.product == product:
                cart.items.remove(item)
                cart.save()

        new_cart_total = 0.00
        for item in cart.items.all():
            new_cart_total += float(item.item_total)
        cart.cart_total = new_cart_total
        cart.save()
        return HttpResponseRedirect('cart')

    def change_qty(self, qty, item_id):
        cart = self
        cart_item = CartItem.objects.get(id=int(item_id))
        cart_item.qty = int(qty)
        cart_item.item_total = int(qty) * Decimal(cart_item.product.price)
        cart_item.save()
        new_cart_total = 0.00
        for item in cart.items.all():
            new_cart_total += float(item.item_total)
        cart.cart_total = new_cart_total
        cart.save()

ORDER_STATUS_CHOISES = (
    ('Заказ обрабатывается', 'Заказ обрабатывается'),
    ('Выполняется','Выполняется'),
    ('Выполняется','Выполняется')
)




class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ForeignKey(Cart, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=266, blank=True, null=True)
    buying_type = models.CharField(max_length=266, choices=(('Самовывоз', 'Самовывоз'),('Доставка', 'Доставка')), default='self')
    date = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOISES, default=ORDER_STATUS_CHOISES[0][0])

    def __str__(self):
        return 'Заказ номер %s' % (self.id)