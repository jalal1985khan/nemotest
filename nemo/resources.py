#from import_export import resources
from .models import *
 
class CompanyResource(resources.ModelResource):
    class Meta:
        model = Company