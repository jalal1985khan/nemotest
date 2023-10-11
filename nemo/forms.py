from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User , Group
from django.forms import forms ,ModelForm
from django.db.models import fields
from nemo.models import *
from django import forms


class CreateUserForm(UserCreationForm):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for visible in self.visible_fields():
    #         visible.field.widget.attrs['class'] = 'form-control'
    #         visible.field.widget.attrs['placeholder'] = visible.field.label

    class Meta:
        model = User
        fields = ['username','email','password1','password2','is_active','is_staff','is_superuser']
        # widgets = {
        #     'username': forms.TextInput(attrs={'class': 'form-control'}),
        #     'email': forms.TextInput(attrs={'class': 'form-control'}),
        #     'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
        #     'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        #     'is_active': forms.CheckboxInput(attrs={'class': 'minimal'}),

        # }
        
        #fields = '__all__'

class CreateProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label

    class Meta:
        model = Profile
        fields = '__all__'
        exclude =['user']          

class CreateCandidateForm(forms.ModelForm):
    #groups = forms.CharField(error_messages={'required':"Group Required"})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            # visible.field.widget.attrs['placeholder'] = visible.field.label
            
    class Meta:
        model = Candidate
        fields = '__all__'
        exclude =['added_by_user']  


class CreateCompanyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            #visible.field.widget.attrs['placeholder'] = visible.field.label
            
    class Meta:
        model = Company
        fields = '__all__'

class CreateVesselForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label
    
    class Meta:
        model = Vessel
        fields = '__all__'

class CreateExperienceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label    
    class Meta:
        model = Experience
        fields = '__all__'
        
class CreateRankForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label     
    
    class Meta:
        model = Rank
        fields ='__all__'

class CreateGradeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label 
    
    class Meta:
        model = Grade
        fields = '__all__'

        
class CreatePortForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label 
    
    class Meta:
        model = Port
        fields = '__all__'
            
class CreatePortAgentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label     
    
    class Meta:
        model = PortAgent
        fields = '__all__'
            
class CreateHospitalForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label     
    
    class Meta:
        model = Hospital
        fields = '__all__'

class CreateDocumentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label
    
    class Meta:
        model = DocumentType
        fields = '__all__'
        

class CreateVendorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label
    
    class Meta:
        model = Vendors
        fields = '__all__'


class CreateVslForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label
    
    class Meta:
        model = VslType
        fields = '__all__' 

 

class CreateOfficeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label

    class Meta:
        model = OfficeDocument
        fields = '__all__'
                 
class CreateCountryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label

    class Meta:
        model = CountryName
        fields = '__all__'

class CreateCrewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label

    class Meta:
        model = CrewPlanner
        fields = '__all__'
        exclude=['crew_created_by','crew_updated_by']



class CreateNotificationForm(forms.ModelForm):
    
    class Meta:
        model = Notifications
        fields = ('ready_by_user','status')

class CreateMedicalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label
    
    class Meta:
        model = Medical
        fields = '__all__'
        exclude=['candidate']   

class CreateTravelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label
    
    class Meta:
        model = Travel
        fields = '__all__'
        exclude=['candidate']  


class CreateBankDetailsForm(forms.ModelForm):

    class Meta:
        model= BankDetails
        fields='__all__'
        exclude= ['candidate']                      
        
class CreateCandidateDocumentForm(forms.ModelForm):

    class Meta:
        model= candidateDocument
        fields='__all__'
        exclude= ['candidate'] 
       
class CreateCandidateNkdForm(forms.ModelForm):

    class Meta:
        model= candidateNkd
        fields='__all__'
        exclude= ['candidate']

class CreateContractForm(forms.ModelForm):

    class Meta:
        model= contract
        fields='__all__'
        exclude= ['candidate']                
        #exclude= ['candidate','rank','company','vessel_type','sign_on_port','sign_off_port']                


class CreateDiscussionForm(forms.ModelForm):

    class Meta:
        model= discussion
        fields='__all__'
        exclude= ['candidate']                
        #exclude= ['candidate','rank','company','vessel_type','sign_on_port','sign_off_port']                        