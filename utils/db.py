from django.db import models
from django.db.models import Func


class Month(Func):
    """
    Method to extract month
    """
    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = models.IntegerField()

class Year(Func):
    """
    Method to extract year
    """
    function = 'EXTRACT'
    template = '%(function)s(YEAR from %(expressions)s)'
    output_field = models.IntegerField()
