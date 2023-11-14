""" exclude fields based on client queries """


class RequestExcludeFieldMixin:

    def get_field_names(self, declared_fields, info):
        view = self.context.get('view')
        request = self.context.get('request')

        fields = super().get_field_names(declared_fields, info)

        if view is None or request is None:
            return fields

        if view.action not in ('list', 'retrive'):
            return fields

        excludes = request.GET.get('excludes')

        if excludes:
            excludes = excludes.split(',')
            return set(fields) - set(excludes)

        return fields
