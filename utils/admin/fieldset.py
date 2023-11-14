""" A small util to simplify the use of fieldsets in admin """


def FieldSets(**kwargs):
    sections = []

    for key, val in kwargs.items():
        key = None if key.lower() == 'none' else key.replace('_', ' ')
        sections.append((
            key,
            {
                'fields': val,
            },
        ))

    return sections
