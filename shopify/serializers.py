from rest_framework import serializers
from .models import Shopify

class ShopifySerializer(serializers.ModelSerializer):
    class  Meta:
        model=Shopify
        fields=['token','storename','gstin','branch','category','transaction1','addnote1','storecode','addnote2']
    