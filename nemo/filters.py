import django_filters
from django_filters import CharFilter
from nemo.models import *
from django import forms


class CandidateFilter(django_filters.FilterSet):

    id = django_filters.NumberFilter(
        field_name='id',
        lookup_expr='icontains',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    first_name = django_filters.CharFilter(
        field_name='first_name',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    rank = django_filters.CharFilter(
        field_name='rank',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    availibity = django_filters.CharFilter(
        field_name='availibity',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    availibityto = django_filters.CharFilter(
        field_name='availibity',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    experience = django_filters.CharFilter(
        field_name='experience',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    grade = django_filters.CharFilter(
        field_name='license',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    status = django_filters.CharFilter(
        field_name='status',
        lookup_expr='icontains',
        widget=forms.TimeInput(attrs={'class': 'form-control'})
    )
    license_country = django_filters.CharFilter(
        field_name='license_country',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    vessel_type = django_filters.CharFilter(
        field_name='vessel_type',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    zone = django_filters.CharFilter(
        field_name='zone',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    # document = django_filters.CharFilter(
    #     field_name='document_type',
    #     lookup_expr='icontains',
    #     widget=forms.TextInput(attrs={'class': 'form-control'})
    # )
     
    class Meta:
        model = Candidate
        fields = ['id','first_name','availibity','availibityto','rank', 'vessel_type','experience','grade','license_country','status','zone']


   
   
