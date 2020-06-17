from rest_framework import serializers

from product.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        # fields={
        #     'name','description','price','discount_price',
        # }
        fields= '__all__'
