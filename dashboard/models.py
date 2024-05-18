from django.db import models
from django.core.files.storage import default_storage
from django.core.files import File
from django.db import models

from random import choices
import string
from io import BytesIO

import qrcode
from PIL import Image



class CodeGenerate(models.Model):
    code = models.CharField(max_length=255, blank=True)
    
    @staticmethod
    def generate_code():
        return ''.join(choices(string.ascii_letters + string.digits, k=20)) 
    
    def save(self, *args, **kwargs):
        if not self.id:
            while True:
                code = self.generate_code()
                if not self.__class__.objects.filter(code=code).count():
                    self.code = code
                    break
        super(CodeGenerate,self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Category(CodeGenerate):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(CodeGenerate):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)


    def __str__(self):
        return self.name
    

    def save(self, *args, **kwargs):
        if self.id:
            image_path = self.qr_code.path
            if default_storage.exists(image_path):
                default_storage.delete(image_path)
        qr_data = f'''
        Category: {self.category.name}
        Product Name: {self.name}
        Quantity: {self.quantity}
        Price: {self.price}
        Description: {self.description}
        Created: {self.created_at}
        '''
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        file_name = f'{self.name}_{self.created_at.strftime("%d-%m-%Y")}.png'
        self.qr_code.save(file_name, File(buffer), save=False)
        super(Product,self).save(*args, **kwargs)

    def delete(self):
        image_path = self.qr_code.path
        if default_storage.exists(image_path):
            default_storage.delete(image_path)
        super(Product, self).delete()


class ProductImage(CodeGenerate):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images')


    def __str__(self):
        return self.product.name


    def delete(self):
        image_path = self.image.path
        if default_storage.exists(image_path):
            default_storage.delete(image_path)
        super(ProductImage, self).delete()


class Enter(CodeGenerate):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'
    
    @property
    def total(self):
        return self.price * self.quantity
    
    def save(self, *args, **kwargs):
        if self.pk:
            obj = Enter.objects.get(id=self.id)
            self.product.quantity -= obj.quantity
            self.price -= obj.price
        self.product.quantity += int(self.quantity)
        self.price += int(self.price)
        self.product.save()
        super(Enter, self).save(*args, **kwargs)



class Outlay(CodeGenerate):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    returned = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    def __str__(self):
        return f'{self.product.name} - {self.quantity} - {self.returned} - {self.date.strftime("%d.%m.%Y %H-%M-%S")}'


    def save(self, *args, **kwargs):
        if not self.pk:
            self.price = self.product.price
        else:
            obj = Outlay.objects.get(id=self.id)
            self.product.quantity += obj.quantity
        self.product.quantity -= int(self.quantity)
        self.product.save()
        super(Outlay, self).save(*args, **kwargs)

class Returned(CodeGenerate):
    out = models.ForeignKey(Outlay, on_delete=models.CASCADE, related_name='returned_set')


    def __str__(self):
        return f'{self.out.product.name} - {self.out.quantity}'
    
    def save(self, *args, **kwargs):
        self.out.returned = True
        self.out.product.quantity += int(self.out.quantity)
        self.out.product.save()
        self.out.save()
        super(Returned, self).save(*args, **kwargs)
    
