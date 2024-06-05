from rest_framework import serializers
from django.utils import timezone


# Import Models Here
from inventory_app.models import CarInventory


class CarInventorySerializer(serializers.ModelSerializer):

    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    qr_code = serializers.SerializerMethodField()


    class Meta:
        model = CarInventory
        exclude = ['created','updated','QR_CODE']
    
    def get_qr_code(self,object):
        return object.QR_CODE.url
    
    def get_created_at(self,object):
        return object.created.strftime('%Y-%m-%d-%H:%M:%S')

    def get_updated_at(self,object):
        return object.updated.strftime('%Y-%m-%d-%H:%M:%S')

    def updated(self, instance, validated_data):

        instance.name = validated_data.get('name',instance.name)
        instance.model = validated_data.get('model',instance.model)
        instance.company_name = validated_data.get('company_name',instance.company_name)
        instance.year = validated_data.get('year',instance.year)
        instance.price = validated_data.get('price',instance.price)
        instance.mileage = validated_data.get('mileage',instance.mileage)
        instance.description = validated_data.get('description',instance.description)
        instance.is_avaliable = validated_data.get('is_avaliable',instance.is_avaliable)
        instance.image = validated_data.get('image',instance.image)

        instance.updated = timezone.now()
        instance.save()
        return instance
