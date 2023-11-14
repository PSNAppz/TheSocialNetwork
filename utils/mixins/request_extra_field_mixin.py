""" A mixin that allow the client side to request extra field
    for a given serializer 
"""


class RequestExtraFieldMixin:

    def get_field_names(self, declared_fields, info):

        view = self.context.get('view')
        request = self.context.get('request')

        fields = super().get_field_names(declared_fields, info)

        if view is None or request is None:
            return fields

        if view.action not in ('list', 'retrive'):
            return fields

        requested_fields = request.GET.get('fields')

        if requested_fields:
            requested_fields = tuple(requested_fields.split(','))
            return fields + requested_fields

        return fields
