""" 
This mixin can be used to make a signal serializer 
to return differnet fields based on the type of view 
the serializer is called on

right now it only supports list and retrive views

list: retruns all the field declared in fields
retrive: returns all the field declared in fields and detail_field

usage:

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'price',
        )
        detail_fields = (
            'images',
            'rating',
            'descrption',
        )

"""


class DetailFieldMixin:

    def get_field_names(self, declared_fields, info):

        view = self.context.get('view')
        detail_fields = getattr(self.Meta, 'detail_fields', tuple())

        # field include in the detail_field is taken out from declared_fields
        # before passing to super, this is so that an arrest isn't thrown when
        # a declared field is included in detail_fields instead of fields,
        declared_fields = set(declared_fields) - set(detail_fields)

        fields = super().get_field_names(declared_fields, info)

        if view and view.action == 'retrieve':
            return fields + detail_fields
        return fields
