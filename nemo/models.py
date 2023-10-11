from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.conf import settings


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    user_image = models.ImageField(upload_to='userprofile', null=True, default='default.jpg')
    

    def __str__(self):
        return self.first_name
    


class Candidate(models.Model):
    STATUS =(
        ("ACTIVE" ,"ACTIVE"),
        ("IN-ACTIVE" ,"IN-ACTIVE")
    )
    GROUPS =(
        ("OFFICER","OFFICER"),
        ("RATING","RATING"),
        ("IV CREW","IV CREW")
    )
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200 , null=True)
    rank = models.CharField(max_length=200 , null=True)
    availibity = models.CharField(max_length=200 , null=True)
    nationality = models.CharField(max_length=200 , null=True)
    marital_status = models.CharField(max_length=200 , null=True)
    date_birth = models.CharField(max_length=200 , null=True)
    count_birth = models.CharField(max_length=200 , null=True)
    birth_month= models.CharField(max_length=200 , null=True, blank=True)
    birth_place = models.CharField(max_length=200 , null=True)
    worked_with_us = models.CharField(max_length=200 , null=True)
    vessel_type = models.CharField(max_length=200 , null=True)
    experience = models.CharField(max_length=200 , null=True)
    zone = models.CharField(max_length=200 , null=True)
    grade = models.CharField(max_length=200 , null=True)
    boiler_suit_size = models.CharField(max_length=200 , null=True)
    safety_shoe_size = models.CharField(max_length=200 , null=True)
    height = models.CharField(max_length=200 , null=True)
    weight = models.CharField(max_length=200 , null=True)
    license_country = models.CharField(max_length=200 , null=True)
    INDoS_Number = models.CharField(max_length=200 , null=True)
    profile = models.ImageField(null=True, blank=True ,upload_to='profile')
    resume = models.FileField(null=True, blank=True, upload_to='resume')
    status = models.CharField(max_length=200, choices=STATUS )
    candidate_groups = models.CharField(max_length=200, choices=GROUPS)
    vendor = models.CharField(max_length=200 , null=False)

    permanent_address=models.CharField(max_length=200 , null=True)
    permanent_city=models.CharField(max_length=200 , null=True)
    permanent_state=models.CharField(max_length=200 , null=True)
    permanent_pincode=models.CharField(max_length=200 , null=True)

    temp_address=models.CharField(max_length=200 , null=True)
    temp_city=models.CharField(max_length=200 , null=True)
    temp_state=models.CharField(max_length=200 , null=True)
    temp_pincode=models.CharField(max_length=200 , null=True)

    mobile1 = models.CharField(max_length=200 , null=True)
    mobile2 = models.CharField(max_length=200 , null=True)
    landline = models.CharField(max_length=200 , null=True)
    email1 = models.CharField(max_length=200 , null=True) 
    email2 = models.CharField(max_length=200 , null=True)
    #added_by_user = models.CharField(max_length=200 , null=True, default=request.user )
    added_by_user = models.CharField(max_length=200 , null=True)
    date_created = models.DateTimeField(auto_now_add=True , null=True)

    def __str__(self):
        return self.first_name


class Company(models.Model):
    CATEGORY =(
        ("Owner" ,"Owner"),
        ("Managers" ,"Managers")
    )
    company_name= models.CharField(max_length=200, null=True, unique=True)
    contact_person= models.CharField(max_length=200, null=True)
    address= models.CharField(max_length=200, null=True)
    phone= models.CharField(max_length=200, null=True)
    email= models.CharField(max_length=200, null=True)
    management= models.CharField(max_length=200, choices=CATEGORY)
    date_created = models.DateTimeField(auto_now_add=True , null=True)

    def __str__(self):
        return self.company_name
    

class Vessel(models.Model):
    vessel_name = models.CharField(max_length=200, null=True, unique=True)
    date_created = models.DateTimeField(auto_now_add=True , null=True)
    
    def __str__(self):
        return self.vessel_name
    

class Experience(models.Model):
    experience = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True , null=True)
    
    def __str__(self):
        return self.experience

class Rank(models.Model):
    RANK=(
        ("Officer","Officer" ),
        ("Rating","Rating" ),
        ("IV Crew","IV Crew" )
    )
    #user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    rank_name= models.CharField(max_length=200, null=True)       
    rank_order= models.CharField(max_length=200, null=True)
    rank_category = models.CharField(max_length=200, choices=RANK)
    date_created = models.DateTimeField(auto_now_add=True , null=True)   

    def __str__(self):
        return self.rank_name
    
class Grade(models.Model):
    grade_name =models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True , null=True)

    def __str__(self):
        return self.grade_name
    
class Port(models.Model):
    port_name= models.CharField(max_length=200, null=True, unique=True)
    date_created = models.DateTimeField(auto_now_add=True , null=True)

    def __str__(self):
        return self.port_name
    

class PortAgent(models.Model):
    port_agent = models.CharField(max_length=200 ,null=True)
    port_contact_person = models.CharField(max_length=200 , null=True)
    port_agent_address= models.CharField(max_length=200, null=True)
    port_agent_phone =models.CharField(max_length=200, null=True)
    port_agent_email = models.CharField(max_length=200, null=True)
    port_agent_city = models.CharField(max_length=200, null=True)
    port_agent_state = models.CharField(max_length=200, null=True)
    port_agent_country = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True , null=True)

    def __str__(self):
        return self.port_agent    
    
class Hospital(models.Model):
    hospital_name = models.CharField(max_length=200, null=True)
    doctor_name = models.CharField(max_length=200, null=True)
    hospital_address = models.CharField(max_length=200, null=True)
    hospital_city = models.CharField(max_length=200, null=True)
    hospital_state = models.CharField(max_length=200, null=True)
    hospital_phone = models.CharField(max_length=200, null=True)
    hospital_email = models.CharField(max_length=200, null=True)
    hospital_image = models.ImageField(null=True ,blank=True)
    date_created = models.DateTimeField(auto_now_add=True , null=True)

    def __str__(self):
        return self.hospital_name 

class DocumentType(models.Model):
    EXPIRY_DATE =(
        ('Yes','Yes'),
        ('No','No')
    )
    document_type = models.CharField(max_length=200, null=True)
    hide_expiry_date = models.CharField(max_length=200, choices=EXPIRY_DATE)
    date_created = models.DateTimeField(auto_now_add=True , null=True)

    def __str__(self):
        return self.document_type 
    

class Vendors(models.Model):
    vendor_name = models.CharField(max_length=200, null=True)
    vendor_address = models.CharField(max_length=200, null=True)  
    date_created = models.DateTimeField(auto_now_add=True , null=True) 

    def __str__(self):
        return self.vendor_name 



class VslType(models.Model):
    vsl_name = models.CharField(max_length=200, null=True)
    vsl_type = models.CharField(max_length=200, null=True)  
    vsl_company = models.CharField(max_length=200, null=True)
    IMO_Number  = models.CharField(max_length=200, null=True)
    vsl_flag = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True , null=True)


    def __str__(self):
        return self.vsl_name   



class OfficeDocument(models.Model):
    document_name = models.CharField( max_length=200, null=True)
    document_file = models.FileField( null=True, upload_to='officedoc')
    date_created = models.DateTimeField(auto_now_add=True , null=True) 

    def __str__(self):
        return self.document_name      
 
class CountryName(models.Model):
    country_name = models.CharField( max_length=200, null=True, unique=True)
    country_code = models.CharField( max_length=200, null=True)
    country_phone_code = models.CharField( max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True , null=True)

    def __str__(self):
        return self.country_name 

class CrewPlanner(models.Model):     
    IMMEDIATE=(
        ("Yes","Yes"),
        ("No","No")
    )
        
    #crew_rank = models.CharField( max_length=200, null=True)
    crew_rank = models.ForeignKey(Rank, on_delete=models.CASCADE)
    crew_company_name = models.ForeignKey(Company, on_delete=models.CASCADE)
    crew_vessel = models.ForeignKey(VslType, on_delete=models.CASCADE)
    crew_vsl_name = models.ForeignKey(Vessel, on_delete=models.CASCADE)
    crew_trading = models.CharField( max_length=200, null=True)
    crew_wages = models.CharField( max_length=200, null=True)
    crew_doj = models.CharField( max_length=200, null=True)
    crew_immediate = models.CharField( max_length=200, null=True, choices=IMMEDIATE)
    crew_other_info = models.CharField( max_length=200, null=True)
    crew_status = models.CharField( max_length=200, null=True)
    crew_created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)
    crew_updated_by = models.CharField( max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True , null=True)
    
    def __str__(self):
        return self.crew_trading


# files handling modles
class ExcelFiles(models.Model):
    file = models.FileField(upload_to='import_files')


class Notifications(models.Model):
    notify_details = models.TextField()
    ready_by_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    added_by_user = models.CharField(max_length=200,  null=True)
    status = models.BooleanField(null=True)
    alert = models.CharField(max_length=200,  null=True)
    type = models.CharField(max_length=200,  null=True)
    date_created = models.DateTimeField(auto_now_add=True , null=True)

    def __str__(self):
        return self.notify_details 
    
class ReadNotification(models.Model):
    notify = models.ForeignKey(Notifications, on_delete=models.CASCADE)
    readuser = models.ForeignKey(User, on_delete=models.CASCADE)    
    status = models.BooleanField(default=False)


class Medical(models.Model):
    DONE=(
        ("OFFICE","OFFICE"),
        ("AGENT","AGENT"),
        ("SELF","SELF")
    )
    STATUS=(
        ("FIT","FIT"),
        ("UNFIT","UNFIT")
    )
    hospital_name= models.ForeignKey(Hospital,models.CASCADE)
    place = models.CharField(max_length=200, null=True)
    date= models.CharField(max_length=200, null=True)
    expiry_date= models.CharField(max_length=200, null=True)
    done_by = models.CharField(max_length=200, null=True,choices=DONE)
    status = models.CharField(max_length=200, null=True,choices=STATUS)
    amount= models.CharField(max_length=200, null=True)
    upload= models.FileField(null=True, blank=True, upload_to='medicals')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)  
    
    def __str__(self):
     return self.hospital_name.hospital_name 


class Travel(models.Model):
        MODES =(
        ("BUS","BUS"),
        ("TRAIN","TRAIN"),
        ("AIR","AIR"),
        ("CAB","CAB")
    )
        STATUS =(
        ("BOOKED","BOOKED"),
        ("CANCELLED","CANCELLED"),
        ("TRAVELLING","TRAVELLING"),
        ("TRAVELLED","TRAVELLED")
    )
        travel_date = models.CharField(max_length=200, null=True)
        travel_from = models.CharField(max_length=200, null=True)
        travel_to = models.CharField(max_length=200, null=True)
        travel_mode = models.CharField(max_length=200, null=True, choices= MODES)
        travel_status = models.CharField(max_length=200, null=True, choices=STATUS)
        ticket_no = models.CharField(max_length=200, null=True)
        agent_name = models.CharField(max_length=200, null=True)
        port_agent= models.ForeignKey(PortAgent, models.CASCADE)
        travel_amount = models.CharField(max_length=200, null=True)
        candidate = models.ForeignKey(Candidate, models.CASCADE)

        def __str__(self):
            return self.ticket_no
        
class BankDetails(models.Model):
    TYPE=(
        ('INDIAN','INDIAN'),
        ('NRI','NRI')
    )
    account_type= models.CharField(max_length=200,null=True, choices=TYPE)        
    bank_name = models.CharField(max_length=200,null=True)
    account_no = models.CharField(max_length=200,null=True)
    bank_address= models.CharField(max_length=200,null=True)
    ifsc_code= models.CharField(max_length=200,null=True)
    swift_code= models.CharField(max_length=200,null=True)
    benificiary= models.CharField(max_length=200,null=True)
    benificiary_address = models.CharField(max_length=200,null=True)
    pancard_number= models.CharField(max_length=200,null=True)
    statement= models.FileField(max_length=200,blank=True,upload_to="bankdetails")
    pancard = models.FileField(max_length=200,blank=True,upload_to="bankdetails")
    candidate = models.ForeignKey(Candidate,models.CASCADE)

    def __str__(self):
     return self.account_no
    
class candidateDocument(models.Model):
    document = models.CharField(max_length=200,null=True)
    document_number= models.CharField(max_length=200,null=True)
    issue_date= models.CharField(max_length=200,null=True)
    issue_place= models.CharField(max_length=200,null=True)
    document_files= models.FileField(max_length=200, null=True,upload_to="document", blank=True)
    candidate = models.ForeignKey(Candidate,models.CASCADE)

    def __str__(self):
        return self.document
    
class candidateNkd(models.Model):
    RELATIONS =(
        ('FATHER','FATHER'),
        ('MOTHER','MOTHER'),
        ('BROTHER','BROTHER'),
        ('SISTER','SISTER'),
        ('SON','SON'),
        ('DAUGHTER','DAUGHTER'),
        ('HUSBAND','HUSBAND'),
        ('WIFE','WIFE'),
        ('MOTHER-IN-LAW','MOTHER-IN-LAW'),
        ('FATHER-IN-LAW','FATHER-IN-LAW'),
        ('UNCLE','UNCLE'),
        ('AUNT','AUNT'),
        ('NEPHEW','NEPHEW'),
        ('NIECE','NIECE'),
    )
    PROIRITY=(
        ('HIGH','HIGH'),
        ('MEDIUM','MEDIUM'),
        ('LOW','LOW')
    )
    kin_name = models.CharField(max_length=200, blank=True, null=True)
    kin_relation = models.CharField(max_length=200, null=True, choices=RELATIONS)
    kin_contact_number = models.CharField(max_length=200, blank=True, null=True)
    kin_contact_address = models.CharField(max_length=200, blank=True, null=True)
    kin_priority = models.CharField(max_length=200, blank=True, null=True, choices=PROIRITY)
    candidate = models.ForeignKey(Candidate,models.CASCADE,null=True)
    

    def __str__(self):
        return self.kin_name
    

class contract(models.Model):
    CURRENCY=(
        ('AED','AED'),
        ('BMD','BMD'),
        ('EUR','EUR'),
        ('GBP','GBP'),
        ('INR','INR'),
        ('MYR','MYR'),
        ('SGD','SGD'),
        ('USD','USD')
    )
    WAGES_TYPE=(
        ('NETT','NETT'),
        ('GROSS','GROSS'),
        ('PER DAY','PER DAY'),
        ('PER MONTH','PER MONTH')
    )
    rank = models.ForeignKey(Rank,models.CASCADE,null=True)
    company = models.ForeignKey(Company,models.CASCADE,null=True)
    vsl_name = models.CharField(max_length=200, blank=True, null=True)
    vessel_type = models.ForeignKey(Vessel,models.CASCADE,null=True)
    sign_on_port = models.ForeignKey(Port, models.CASCADE, related_name='sign_on_port')
    sign_on = models.CharField(max_length=200, blank=True, null=True)
    wage_start = models.CharField(max_length=200, blank=True, null=True)
    eoc = models.CharField(max_length=200, blank=True, null=True)
    wages = models.CharField(max_length=200, blank=True, null=True)
    currency = models.CharField(max_length=200, blank=True, null=True, choices=CURRENCY)
    wages_types = models.CharField(max_length=200, blank=True, null=True, choices=WAGES_TYPE)
    sign_off = models.CharField(max_length=200, blank=True, null=True)
    sign_off_port = models.ForeignKey(Port,models.CASCADE,null=True,related_name="sign_off_port")
    reason_for_sign_off = models.CharField(max_length=200, blank=True, null=True)
    documents = models.FileField(max_length=200, null=True,upload_to="contract", blank=True)
    aoa = models.FileField(max_length=200, null=True,upload_to="contract", blank=True)
    aoa_number = models.CharField(max_length=200, blank=True, null=True)
    emigrate_number = models.CharField(max_length=200, blank=True, null=True)
    candidate = models.ForeignKey(Candidate,models.CASCADE,null=True)

    def __str__(self):
        return self.aoa_number


class discussion(models.Model):
    #status = models.CharField(max_length=200, blank=True, null=True)
    proposed = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    joined = models.BooleanField(default=False)
    reject = models.BooleanField(default=False)
    company = models.ForeignKey(Company,models.CASCADE,null=True)
    date = models.CharField(max_length=200, blank=True, null=True)
    reason = models.CharField(max_length=200, blank=True, null=True)
    reminder_check = models.BooleanField(default=False)
    comment_check = models.BooleanField(default=False)
    reference_check =  models.BooleanField(default=False)
    special_comment = models.CharField(max_length=200, blank=True, null=True)
    reminder_date = models.CharField(max_length=200, blank=True, null=True)
    refernce_comment = models.CharField(max_length=200, blank=True, null=True)
    candidate = models.ForeignKey(Candidate,models.CASCADE,null=True)



    


    
    
        
        
      

