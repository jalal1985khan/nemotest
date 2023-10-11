from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User,Group
from django.contrib import messages
from nemo.forms import *
from django.contrib.auth.decorators import login_required
from nemo.decorators import unauthenticated_user,admin_only
from nemo.models import *
from nemo.filters import *
import pandas as pd
from django.conf import settings
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#from nemo.resources import *
from django.template import loader
from django.db.models import Count
import csv
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist


import logging
logger = logging.getLogger(__name__)
logger = logging.getLogger('django')


#users start here
@login_required(login_url='login')
@admin_only
def registerPage(request):
    form = CreateUserForm()
    user = request.user
    profile = CreateProfileForm()

    if request.method =='POST':      
         form = CreateUserForm(request.POST)
         profile = CreateProfileForm( instance = user )
         if form.is_valid():
              user = form.save()
              username = form.cleaned_data.get('username')
              permission = request.POST['permission']
              first_name = request.POST['first_name']
              last_name = request.POST['last_name']
              phone = request.POST['phone']
              email = request.POST['email']
              group = Group.objects.get(name=permission)
              user.groups.add(group)
              Profile.objects.create(user=user,first_name=first_name,last_name=last_name,phone=phone,email=email)
              messages.success(request,'User created successfully ' + username) 
    customers = User.objects.all()
    groups = Group.objects.all()

    context ={'form':form,'customers':customers,'groups':groups,'profile':profile}
    return render(request,"users.html",context)
#users end here

#login start here
@unauthenticated_user
def loginPage(request):        
            if request.method =='POST':
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(request, username=username,password=password)
                if user is not None:
                        login(request,user)
                        return redirect('/dashboard/')
                else:
                    messages.info(request,'username or password incorrect')

            context = {}
            return render(request,"auth/auth-login.html", context)
#login end here
#company profile here
@login_required(login_url='login')
def profile(request):
        notifycount = Notifications.objects.filter(status=False).count()
        user = request.user.profile
        notify_msg= "profile updated successfully"
        username =request.user
        form = CreateProfileForm(instance=user)
        if request.method =='POST':
         form = CreateProfileForm(request.POST,request.FILES, instance= user)
         if form.is_valid():
              form.save()
              Notifications.objects.create(notify_details = notify_msg , added_by_user=username , status=False)
              messages.success(request,'Profile updated successfully ') 
        context ={
              'form':form,
              'notifycount':notifycount
        }
        return render(request,"auth/profile.html", context)
       
#company profile end here           
#logout start here
def logoutUser(request):
    logout(request)
    return redirect('/')
#logout end here

#dashboard start here
@login_required(login_url='login')
@admin_only
def dashboard(request):
        currentdate = datetime.today()
        formatDate = currentdate.strftime("%m-%d")
        checkDate = timezone.now()+ timedelta(days=15)
        upcomingDate = checkDate.strftime("%m-%d")
        NewDate = currentdate.strftime("%Y-%m-%d")
        DiffDate = checkDate.strftime("%Y-%m-%d")
        candidate = Candidate.objects.all().order_by('-id')
        filter = CandidateFilter(request.GET, queryset=candidate)
        filterrank = Rank.objects.all()
        filtervessel = Vessel.objects.all()
        filterexp = Experience.objects.all()
        filterlicense = Grade.objects.all()
        filtercountry = CountryName.objects.all()
        filterdocument = DocumentType.objects.all()
        #birthdate start here
        upcoming_birthdays = Candidate.objects.filter(birth_month__lte = upcomingDate, birth_month__gte = formatDate)
        upcoming_reminders = discussion.objects.filter(reminder_date__lte = DiffDate, reminder_date__gte = NewDate)
        notifycount = Notifications.objects.filter(status=False).count()
        avail_can = Candidate.objects.all().values('rank').distinct()
        #avil_count =Candidate.objects.filter(rank=avail_can).count()
        #county = Candidate.objects.all().values("rank").annotate(total=Count("rank"))
        rank = Candidate.objects.values('rank').annotate(count=models.Count('rank')).order_by()
        crew = CrewPlanner.objects.all().values('crew_status').distinct()
        crewplanner = CrewPlanner.objects.values('crew_status').annotate(count=models.Count('crew_status')).order_by()
        totalcrew = CrewPlanner.objects.filter(crew_status='POSITION OPEN').count()
        opencrew = CrewPlanner.objects.filter(crew_status='POSITION OPEN')

        context ={
             'filter':filter,
             'filterrank':filterrank,
             'filtervessel':filtervessel,
             'filterexp':filterexp,
             'filterlicense':filterlicense,
             'filtercountry':filtercountry,
             'filterdocument':filterdocument,
              'notifycount':notifycount,
              'avail_can':avail_can,
              'rank':rank,
              'crew':crew,
              'crewplanner':crewplanner,
              'totalcrew':totalcrew,
              'upcoming_birthdays':upcoming_birthdays,
              'upcoming_reminders':upcoming_reminders,
              'opencrew':opencrew,
              'upcomingDate':NewDate,
              'currentdate':DiffDate
             
                  }      
        return render(request,"dashboard/dashboard.html", context)
#dashboard end here
###

#search start here
@login_required(login_url='login')
@admin_only
def search(request):
        candidate = Candidate.objects.all().order_by('-id')
        notifycount = Notifications.objects.filter(status=False).count()
        get_rank = request.GET.get('rank')
        get_vessel = request.GET.get('vessel_type')
        get_experience = request.GET.get('experience')
        get_license = request.GET.get('license')
        get_status = request.GET.get('status')
        get_license_country = request.GET.get('license_country')
        get_zone = request.GET.get('zone')
        get_from_date = request.GET.get('availibity')
        get_to_date = request.GET.get('availibityto')
        get_ageabove = request.GET.get('ageabove')
        get_agebelow = request.GET.get('ageabelow')
        events_in_range = Candidate.objects.filter(availibity__gte=get_from_date, availibity__lte=get_to_date)   
        dob_in_range = Candidate.objects.filter(count_birth__gte=get_ageabove, count_birth__lte=get_agebelow)   

        if request.method == 'GET':
         first_name = request.GET.get('first_name')
        filter = CandidateFilter(request.GET, queryset=candidate)
        paginator = Paginator(filter.qs, 10)
        page = request.GET.get('page',1)
        try:
              users = paginator.page(page)
        except PageNotAnInteger:
              users = paginator.page(1)
        except EmptyPage: 
              users = paginator.page(paginator.num_pages)   
        
        filterrank = Rank.objects.all()
        filtervessel = Vessel.objects.all()
        filterexp = Experience.objects.all()
        filtercountry = CountryName.objects.all()
        filterlicense = Grade.objects.all()
        filterdocument = DocumentType.objects.all()
       
        context ={ 
                  'filter':filter,
                  'filterrank':filterrank,
                  'filtervessel':filtervessel,
                  'filterexp':filterexp,
                  'filterlicense':filterlicense,
                  'filtercountry':filtercountry,
                  'filterdocument':filterdocument,
                  'page_obj':users,
                  'first_name':first_name,
                  'notifycount':notifycount,
                  'get_rank':get_rank,
                  'get_vessel':get_vessel,
                  'get_experience':get_experience,
                  'get_license':get_license,
                  'get_status':get_status,
                  'get_license_country':get_license_country,
                  'get_zone':get_zone,
                  'get_from_date':get_from_date,
                  'get_to_date':get_to_date,
                  'events_in_range':events_in_range,
                  'dob_in_range' :dob_in_range
                  
                  }
        return render(request,"view/view-search.html",context)
#search end here

#search start here
@login_required(login_url='login')
@admin_only
def advancedsearch(request):
        candidate = Candidate.objects.all().order_by('-id')
        notifycount = Notifications.objects.filter(status=False).count()
        get_rank = request.GET.get('rank')
        get_vessel = request.GET.get('vessel_type')
        get_experience = request.GET.get('experience')
        get_license = request.GET.get('license')
        get_status = request.GET.get('status')
        get_license_country = request.GET.get('license_country')
        get_zone = request.GET.get('zone')
        if request.method == 'GET':
            first_name = request.GET.get('first_name')
        filter = CandidateFilter(request.GET, queryset=candidate)
        paginator = Paginator(filter.qs, 10)
        page = request.GET.get('page',1)
        try:
              users = paginator.page(page)
        except PageNotAnInteger:
              users = paginator.page(1)
        except EmptyPage: 
              users = paginator.page(paginator.num_pages)   
        
        rank = Rank.objects.all()
        vessel = Vessel.objects.all()
        exp = Experience.objects.all()
        country = CountryName.objects.all()
        license = Grade.objects.all()
        document = DocumentType.objects.all()
       
        context ={ 'filter':filter,
                  'rank':rank ,
                  'vessel':vessel,
                  'exp':exp,
                  'page_obj':users,
                  'first_name':first_name,
                  'notifycount':notifycount,
                  'get_rank':get_rank,
                  'get_vessel':get_vessel,
                  'get_experience':get_experience,
                  'country':country,
                  'license':license,
                  'get_license':get_license,
                  'get_status':get_status,
                  'get_license_country':get_license_country,
                  'get_zone':get_zone,
                  'document':document
                  }
        return render(request,"include/header.html",context)
#search end here



#user start here
@login_required(login_url='login')
@admin_only
def users(request):
        customers = User.objects.all()
        context ={'customers':customers}
        return render(request,"allusers.html",context)
#user end here


########Candidate start here
@login_required(login_url='login')
@admin_only
def viewcandidate(request):
        view = Candidate.objects.all().order_by('-id')
        notifycount = Notifications.objects.filter(status=False).count()
        paginator = Paginator(view, 40)
        page = request.GET.get('page',1)
        try:
              page_obj = paginator.page(page)
        except PageNotAnInteger:
              page_obj = paginator.page(1)
        except EmptyPage: 
              page_obj = paginator.page(paginator.num_pages) 
        context ={ 'page_obj':page_obj,'notifycount':notifycount }
        return render(request,"view/view-candidate.html", context)

#candidate start here
@login_required(login_url='login')
@admin_only
def addcandidate(request):
    form = CreateCandidateForm()
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    notify_msg = ('%(first_name)s %(last_name)s') % {'first_name': first_name ,'last_name': last_name}
    success_message = ('%(first_name)s %(last_name)s Candidate added successfully.') % {'first_name': first_name ,'last_name': last_name}
    if request.method =='POST':
         form = CreateCandidateForm(request.POST,request.FILES)
         if form.is_valid():
              obj = form.save(commit=False) # Return an object without saving to the DB
              #form.save() # Return an object without saving to the DB
              obj.added_by_user = request.user  # Add an author field which will contain current user's id
              obj.save()
              
              #form.save()
              Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='new',type='CANDIDATE', status=False)              
              messages.success(request,success_message)
              return redirect('/view-allcandidate')
    rank = Rank.objects.all()
    vessel = Vessel.objects.all()
    experience = Experience.objects.all()
    group = Group.objects.get(name='vendors')
    grade = Grade.objects.all()
    country = CountryName.objects.all()
    vendor = group.user_set.all()
    context ={'form':form, 'rank':rank,'vessel':vessel,'experience':experience,'grade':grade, 'country':country,'notifycount':notifycount,'vendor':vendor }
    
    return render(request,"add/add-candidate.html",context)
#######
#Edit candidate start here
@login_required(login_url='login')
@admin_only
def editcandidate(request ,pk):
    candidate = Candidate.objects.get(id = pk)
    candate = Candidate.objects.filter(id=pk)
    form = CreateCandidateForm( instance = candidate )
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    notify_msg = ('%(first_name)s %(last_name)s') % {'first_name': first_name ,'last_name': last_name}
    success_message = ('%(first_name)s %(last_name)s Candidate updated successfully.') % {'first_name': first_name ,'last_name': last_name}
    if request.method =='POST':
         form = CreateCandidateForm(request.POST,request.FILES, instance = candidate)
         if form.is_valid():
              form.save()
              Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='updated',type='CANDIDATE', status=False)              
              messages.success(request,success_message)
              return redirect('/view-allcandidate')

    rank = Rank.objects.all()
    vessel = Vessel.objects.all()
    experience = Experience.objects.all()
    grade = Grade.objects.all()
    country = CountryName.objects.all()
    group = Group.objects.get(name='vendors')
    vendor = group.user_set.all()
    context ={'form':form, 'rank':rank,'vendor':vendor,'vessel':vessel,'experience':experience,'grade':grade, 'country':country,'notifycount':notifycount,'pk':pk,'candidate':candate }
    return render(request,"edit/edit-candidate.html",context)
###########
@login_required(login_url='login')
@admin_only
def deleteall(request):
      Candidate.objects.all().delete()
      #DocumentType.objects.all().delete()
      return redirect('/view-allcandidate')

#################
def delete_objects(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_ids')
        objects_to_delete = Candidate.objects.filter(id__in=selected_ids)
        if not objects_to_delete:
            messages.add_message(request,messages.ERROR, "No objects selected for deletion.")
            return redirect('/view-allcandidate')
        return render(request, 'delete/multi-delete-candidate.html',{'objects_to_delete':objects_to_delete})      
##############   
def perform_delete(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_ids')
        objects_to_delete = Candidate.objects.filter(id__in=selected_ids)
        objects_to_delete.delete()
        messages.success(request, "Selected objects have been deleted.")
        return redirect('/view-allcandidate')

                  

###########
@login_required(login_url='login')
@admin_only
def deletecandidate(request ,pk):
    delete = Candidate.objects.get(id = pk)
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = delete
    pre_url = request.META.get('HTTP_REFERER').split("/")[-1]
    page = request.POST.get('url')
    success_message = ('%(notify_msg)s Candidate deleted successfully.') % {'notify_msg': notify_msg}
    if request.method == 'POST':
          delete.delete()
          Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='deleted',type='CANDIDATE', status=False)
          messages.success(request,success_message)
          return redirect(page)
    context ={'delete':delete,'notifycount':notifycount,'pre_url':pre_url}
    return render(request,"delete/delete-candidate.html",context)
################

@login_required(login_url='login')
@admin_only
def importcandidate(request):
    notifycount = Notifications.objects.filter(status=False).count()
    context ={'notifycount':notifycount}
    if request.method == 'POST':
            #company = CompanyResource()
            file = request.FILES['files']
            ExcelFiles.objects.create(
                  file = file
            )
            path = file.file 
            empexceldata = pd.read_excel(path)
            dbframe = empexceldata
            #print(path)
            for dbframe in dbframe.itertuples():
                  obj = Candidate.objects.create(   
                        first_name = dbframe.first_name,
                        last_name = dbframe.last_name,
                        rank = dbframe.rank,
                        availibity = dbframe.availibity,
                        nationality = dbframe.nationality,
                        marital_status = dbframe.marital_status,
                        date_birth = dbframe.date_birth,
                        birth_place = dbframe.birth_place,
                        worked_with_us = dbframe.worked_with_us,
                        vessel_type = dbframe.vessel_type,
                        experience = dbframe.experience,
                        zone = dbframe.zone,
                        grade = dbframe.grade,
                        boiler_suit_size = dbframe.boiler_suit_size,
                        safety_shoe_size = dbframe.safety_shoe_size,
                        height = dbframe.height,
                        weight = dbframe.weight,
                        license_country = dbframe.license_country,
                        INDoS_Number = dbframe.INDoS_Number,
                        permanent_address = dbframe.permanent_address,
                        permanent_city = dbframe.permanent_city,
                        permanent_state = dbframe.permanent_state,
                        permanent_pincode = dbframe.permanent_pincode,
                        temp_address = dbframe.temp_address,
                        temp_city = dbframe.temp_city,
                        temp_state = dbframe.temp_state,
                        temp_pincode = dbframe.temp_pincode,
                        mobile1 = dbframe.mobile1,
                        mobile2 = dbframe.mobile2,
                        landline = dbframe.landline,
                        email1 = dbframe.email1,
                        email2 = dbframe.email2


                        )                
            obj.save()
            messages.success(request,"Candidate Data uploaded")      
            return redirect ("/view-allcandidate/")
    return render(request,"exportsTemplates/exportCandidate.html",context)

##################
@login_required(login_url='login')
@admin_only
def exportcandidate(request):
      response = HttpResponse(content_type='text/csv')
      response['Content-Disposition'] = 'attachment; filename="Candidate.csv"'
      writer = csv.writer(response)
      #writer.writerow(['Grade Name'])  
      writer.writerow(['first_name','last_name','rank','availibity','nationality','marital_status','date_birth','birth_place','worked_with_us','vessel_type','experience','zone','grade','boiler_suit_size','safety_shoe_size','height','weight','license_country','INDoS_Number','permanent_address','permanent_city','permanent_state','permanent_pincode','temp_address','temp_city','temp_state','temp_pincode','mobile1','mobile2','landline','email1','email2'])     
      users = Candidate.objects.all().values_list('first_name','last_name','rank','availibity','nationality','marital_status','date_birth','birth_place','worked_with_us','vessel_type','experience','zone','grade','boiler_suit_size','safety_shoe_size','height','weight','license_country','INDoS_Number','permanent_address','permanent_city','permanent_state','permanent_pincode','temp_address','temp_city','temp_state','temp_pincode','mobile1','mobile2','landline','email1','email2')
      for user in users:
            writer.writerow(user)
      return response

##### candidate end here 







#### Add Medical Started
#################
#################
########
@login_required(login_url='login')
@admin_only
def viewmedical(request,pk):
     medicals = Medical.objects.filter(candidate=pk)
     candidate = Candidate.objects.filter(id=pk)
     notifycount = Notifications.objects.filter(status=False).count() 
     paginator = Paginator(medicals, 10)
     page = request.GET.get('page',1)
     try:
           page_obj = paginator.page(page)
     except PageNotAnInteger:
           page_obj = paginator.page(1)
     except EmptyPage: 
           page_obj = paginator.page(paginator.num_pages) 

     context={
           'pk':pk,
           'page_obj':page_obj,
           'notifycount':notifycount,
           'candidate':candidate
     }
     try:
        return render(request,"view/view-candidate-hospital.html",context)           
     
     except Medical.DoesNotExist:
        
        return render(request,"view/view-candidate-hospital.html",context)         


################
@login_required(login_url='login')
@admin_only
def editmedical(request ,pk):
      medical_id = Medical.objects.get(id = pk)
      form = CreateMedicalForm( instance = medical_id )
      notifycount = Notifications.objects.filter(status=False).count()
      notify_msg = request.POST.get("hospital_id")
      success_message = ('%(notify_msg)s medical updated successfully.') % {'notify_msg': notify_msg}
      user = request.user
      if request.method =='POST':
         form = CreateMedicalForm(request.POST,request.FILES, instance = medical_id)
         #page = request.POST('medical_id')
         page = request.POST.get('edit_id')
         red = ('/view-medical/%(page)s')% {'page': page}
         if form.is_valid():
              form.save()
              Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='updated',type='MEDICAL', status=False)              
              messages.success(request,success_message)
              return redirect(red)
      medicals = Medical.objects.filter(id = pk)  
      context ={'form':form,'notifycount':notifycount,'medicals':medicals}
      return render(request,"edit/edit-medical.html",context)     
############ 
def delete_medical_objects(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_ids')
        can_id = request.POST.get('can_id')
        red = ('/view-medical/%(can_id)s') % {'can_id':can_id}
        objects_to_delete = Medical.objects.filter(id__in=selected_ids)
        if not objects_to_delete:
            messages.add_message(request,messages.ERROR, "No objects selected for deletion.")
            return redirect(red)
        return render(request, 'delete/multi-delete-medical.html',{'objects_to_delete':objects_to_delete,'red':red})      
#################
def del_multi_medical(request):
      if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_ids')
        red = request.POST.get('url')
        objects_to_delete = Medical.objects.filter(id__in=selected_ids)
        objects_to_delete.delete()
        messages.success(request, "Selected objects have been deleted.")
        return redirect(red)
#######################
@login_required(login_url='login')
@admin_only
def deletemedical(request ,pk):
    delete = Medical.objects.get(id = pk)
    delete_id = Medical.objects.filter(id=pk)
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = delete
    pre_url = request.META.get('HTTP_REFERER').split("/")[-1]
    page = request.POST.get('url')
    success_message = ('%(notify_msg)s Medical deleted successfully.') % {'notify_msg': notify_msg}
    if request.method == 'POST':
          delete.delete()
          Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='deleted',type='MEDICAL', status=False)
          messages.success(request,success_message)
          return redirect(page)
    context ={'delete':delete,'notifycount':notifycount,'pre_url':pre_url,'delete_id':delete_id}
    return render(request,"delete/delete-medical.html",context)
################
@login_required(login_url='login')
@admin_only
def addmedical(request,pk):
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = request.POST.get("hospital_id")
    success_message = ('%(notify_msg)s medical added successfully.') % {'notify_msg': notify_msg} 
    red=('/view-medical/%(page_id)s') % {'page_id':pk}
    try:
          form = CreateMedicalForm()
          if request.method =='POST':
                form = CreateMedicalForm(request.POST,request.FILES)
                if form.is_valid():
                      obj = form.save(commit=False) # Return an object without saving to the DB
                      obj.candidate_id = pk
                      obj.save()
                      Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='new',type='MEDICAL', status=False)
                      messages.success(request,success_message)
                      return redirect(red)     
          #form = CreateMedicalForm(instance=medical_id)
          context ={'form':form,'notifycount':notifycount,'pk':pk}
          return render(request,"add/add-candidate-hospital.html",context)

    except Medical.DoesNotExist:
          form = CreateMedicalForm()
          if request.method =='POST':
                form = CreateMedicalForm(request.POST,request.FILES)
                if form.is_valid():
                      obj = form.save(commit=False) # Return an object without saving to the DB
                      obj.candidate_id = pk
                      obj.save()
                      Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='new',type='MEDICAL', status=False)
                      messages.success(request,success_message)
                      return redirect(red) 
          context ={'form':form,'notifycount':notifycount,'pk':pk}
          return render(request,"add/add-candidate-hospital.html",context)
#################
def delete_medical_objects(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_ids')
        can_id = request.POST.get('can_id')
        red = ('/view-medical/%(can_id)s') % {'can_id':can_id}
        objects_to_delete = Medical.objects.filter(id__in=selected_ids)
        if not objects_to_delete:
            messages.add_message(request,messages.ERROR, "No objects selected for deletion.")
            return redirect(red)
        return render(request, 'delete/multi-delete-medical.html',{'objects_to_delete':objects_to_delete,'red':red})      

def del_multi_medical(request):
      if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_ids')
        red = request.POST.get('url')
        objects_to_delete = Medical.objects.filter(id__in=selected_ids)
        objects_to_delete.delete()
        messages.success(request, "Selected objects have been deleted.")
        return redirect(red)
#######################
@login_required(login_url='login')
@admin_only
def deletemedical(request ,pk):
    delete = Medical.objects.get(id = pk)
    delete_id = Medical.objects.filter(id=pk)
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = delete
    pre_url = request.META.get('HTTP_REFERER').split("/")[-1]
    page = request.POST.get('url')
    success_message = ('%(notify_msg)s Medical deleted successfully.') % {'notify_msg': notify_msg}
    if request.method == 'POST':
          delete.delete()
          Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='deleted',type='MEDICAL', status=False)
          messages.success(request,success_message)
          return redirect(page)
    context ={'delete':delete,'notifycount':notifycount,'pre_url':pre_url,'delete_id':delete_id}
    return render(request,"delete/delete-medical.html",context)



###### ADD BANK SECTION ##########
########
#################
def del_multi_bank(request):
      if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_ids')
        red = request.POST.get('url')
        objects_to_delete = BankDetails.objects.filter(id__in=selected_ids)
        objects_to_delete.delete()
        messages.success(request, "Selected objects have been deleted.")
        return redirect(red)
def delete_bank_objects(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_ids')
        can_id = request.POST.get('can_id')
        red = ('/view-bank/%(can_id)s') % {'can_id':can_id}
        objects_to_delete = BankDetails.objects.filter(id__in=selected_ids)
        if not objects_to_delete:
            messages.add_message(request,messages.ERROR, "No objects selected for deletion.")
            return redirect(red)
        return render(request, 'delete/multi-delete-travel.html',{'objects_to_delete':objects_to_delete,'red':red})      

def del_multi_bank(request):
      if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_ids')
        red = request.POST.get('url')
        objects_to_delete = BankDetails.objects.filter(id__in=selected_ids)
        objects_to_delete.delete()
        messages.success(request, "Selected objects have been deleted.")
        return redirect(red)
#######################
@login_required(login_url='login')
@admin_only
def deletebank(request ,pk):
    delete = BankDetails.objects.get(id = pk)
    delete_id = BankDetails.objects.filter(id=pk)
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = delete
    pre_url = request.META.get('HTTP_REFERER').split("/")[-1]
    page = request.POST.get('url')
    success_message = ('%(notify_msg)s Travel deleted successfully.') % {'notify_msg': notify_msg}
    if request.method == 'POST':
          delete.delete()
          Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='deleted',type='MEDICAL', status=False)
          messages.success(request,success_message)
          return redirect(page)
    context ={'delete':delete,'notifycount':notifycount,'pre_url':pre_url,'delete_id':delete_id}
    return render(request,"delete/delete-travel.html",context)
@login_required(login_url='login')
@admin_only
def viewbank(request,pk):
     medicals = BankDetails.objects.filter(candidate=pk)
     candidate = Candidate.objects.filter(id=pk)
     notifycount = Notifications.objects.filter(status=False).count() 
     paginator = Paginator(medicals, 10)
     page = request.GET.get('page',1)
     try:
           page_obj = paginator.page(page)
     except PageNotAnInteger:
           page_obj = paginator.page(1)
     except EmptyPage: 
           page_obj = paginator.page(paginator.num_pages) 

     context={
           'pk':pk,
           'page_obj':page_obj,
           'notifycount':notifycount,
           'candidate':candidate
     }
     try:
        return render(request,"view/view-candidate-bank.html",context)           
     except BankDetails.DoesNotExist:   
        return render(request,"view/view-candidate-bank.html",context)         
     
################
@login_required(login_url='login')
@admin_only
def editbank(request ,pk):
      id = BankDetails.objects.get(id = pk)
      form = CreateBankDetailsForm( instance = id )
      notifycount = Notifications.objects.filter(status=False).count()
      notify_msg = request.POST.get("account_no")
      success_message = ('%(notify_msg)s Bank updated successfully.') % {'notify_msg': notify_msg}
      user = request.user
      if request.method =='POST':
         form = CreateBankDetailsForm(request.POST,request.FILES, instance = id)
         #page = request.POST('medical_id')
         page = request.POST.get('edit_id')
         red = ('/view-bank/%(page)s')% {'page': page}
         if form.is_valid():
              form.save()
              Notifications.objects.create(notify_details = notify_msg ,added_by_user=user ,alert='updated',type='BANK', status=False)              
              messages.success(request,success_message)
              return redirect(red)
      bank = BankDetails.objects.filter(id = pk)  
      context ={'form':form,'notifycount':notifycount,'bank':bank}
      return render(request,"edit/edit-bank.html",context)

################
@login_required(login_url='login')
@admin_only
def addbank(request,pk):
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = request.POST.get("account_no")
    success_message = ('%(notify_msg)s Bank added successfully.') % {'notify_msg': notify_msg} 
    red=('/view-bank/%(page_id)s') % {'page_id':pk}
    try:
          form = CreateBankDetailsForm()
          if request.method =='POST':
                form = CreateBankDetailsForm(request.POST,request.FILES)
                if form.is_valid():
                      obj = form.save(commit=False) # Return an object without saving to the DB
                      obj.candidate_id = pk
                      obj.save()
                      Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='new',type='TRAVEL', status=False)
                      messages.success(request,success_message)
                      return redirect(red)     
          #form = CreateMedicalForm(instance=medical_id)
          context ={'form':form,'notifycount':notifycount,'pk':pk}
          return render(request,"add/add-candidate-bank.html",context)

    except BankDetails.DoesNotExist:
          form = CreateBankDetailsForm()
          if request.method =='POST':
                form = CreateBankDetailsForm(request.POST,request.FILES)
                if form.is_valid():
                      obj = form.save(commit=False) # Return an object without saving to the DB
                      obj.candidate_id = pk
                      obj.save()
                      Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='new',type='MEDICAL', status=False)
                      messages.success(request,success_message)
                      return redirect(red) 
          context ={'form':form,'notifycount':notifycount,'pk':pk}
          return render(request,"add/add-candidate-bank.html",context)    

######ADD DICUSSION SECTION##########
########
################   
@login_required(login_url='login')
@admin_only
def viewdiscussion(request,pk):
     discusion = discussion.objects.filter(candidate=pk)
     candidate = Candidate.objects.filter(id=pk)
     can_contract = contract.objects.filter(candidate=pk)
     rank = Rank.objects.all()
     dis_rank = Candidate.objects.get(id = pk)
     vessel = Vessel.objects.all()
     notifycount = Notifications.objects.filter(status=False).count()
     try:
        id = discussion.objects.get(candidate = pk)
        form = CreateDiscussionForm( instance = id )
        context ={
          'form':form,
           'notifycount':notifycount,
           'dicussion':discusion,
           'candidate':candidate,
           'contract':can_contract,
           'rank':rank,
           'vessel':vessel,
           'dis_rank':dis_rank,
           'id':id   
        }

        return render(request,"edit/edit-discussion.html",context)
     except discussion.DoesNotExist:
        form = CreateDiscussionForm()
        id = Candidate.objects.get(id = pk)
        context ={'form':form,
                  'candidate':candidate, 
                  'contract':can_contract,
                  'notifycount':notifycount,
                  'rank':rank,
                  'vessel':vessel,
                  'dis_rank':dis_rank,
                  'id':id

                  }
                     
        return render(request,"view/view-discussion.html",context)
        

##################################################
@login_required(login_url='login')
@admin_only
def adddiscussion(request,pk):
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = request.POST.get("name")
    success_message = ('%(notify_msg)s Discussion added successfully.') % {'notify_msg': notify_msg} 
    red=('/view-discussion/%(page_id)s') % {'page_id':pk}
    try:
          form = CreateDiscussionForm()
          if request.method =='POST':
                form = CreateDiscussionForm(request.POST)
                if form.is_valid():
                      obj = form.save(commit=False) # Return an object without saving to the DB
                      obj.candidate_id = pk
                      obj.save()
                      #Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='new',type='DOCUMENT', status=False)
                      messages.success(request,success_message)
                      return redirect(red)     
          #form = CreateMedicalForm(instance=medical_id)
          context ={'form':form,'notifycount':notifycount,'pk':pk}
          return render(request,"add/add-candidate-document.html",context)

    except discussion.DoesNotExist:
          form = CreateDiscussionForm()
          if request.method =='POST':
                form = CreateDiscussionForm(request.POST,request.FILES)
                if form.is_valid():
                      obj = form.save(commit=False) # Return an object without saving to the DB
                      obj.candidate_id = pk
                      obj.save()
                      Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='new',type='DISCUSSION', status=False)
                      messages.success(request,success_message)
                      return redirect(red) 
          context ={'form':form,'notifycount':notifycount,'pk':pk}
          return render(request,"add/add-candidate-document.html",context)  

##################################################
@login_required(login_url='login')
@admin_only
def editdiscussion(request ,pk):
      id = discussion.objects.get(id = pk)
      form = CreateDiscussionForm( instance = id )
      notify_msg = ''
      success_message = ('%(notify_msg)s Discussion updated successfully.') % {'notify_msg': notify_msg}
      user = request.user
      if request.method =='POST':
         form = CreateDiscussionForm(request.POST,request.FILES, instance = id)
         page = request.POST.get('edit_id')
         red = ('/view-discussion/%(page)s')% {'page': page}
         if form.is_valid():
              form.save()
              Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='updated',type='DISCUSSION', status=False)              
              messages.success(request,success_message)
              return redirect(red)
      #pageid = discussion.objects.filter(id = pk)  
      #context ={'form':form,'notifycount':notifycount,'pageid':pageid}
      return redirect('/view-discussion/')
##################################################
@login_required(login_url='login')
@admin_only
def editcomment(request):
      id = request.POST.get('can_id')
      availiblity = request.POST.get('available')
      salary = request.POST.get('salary')
      company = request.POST.get('company')
      rank = request.POST.get('rank')
      vessel = request.POST.get('vessel')
      status = request.POST.get('status')
      red = ('/view-discussion/%(id)s')% {'id': id}
      notify_msg = availiblity
      success_message = ('%(notify_msg)s contract updated successfully.') % {'notify_msg': notify_msg}
      user = request.user
      if request.method =='POST':
           t = Candidate.objects.get(id=id)
           u = contract.objects.get(candidate=id)     
           t.availibity = availiblity  # change field
           t.rank = rank  # change field
           t.vessel_type = vessel
           t.status = status
           u.wages = salary
           t.save() # this will update only  
           u.save() # this will update only
                
           Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='updated',type='CONTRACT', status=False)              
           messages.success(request,success_message)
           return redirect(red)  
      return redirect(red)  




######ADD CONTRACT SECTION##########
########
#################  
@login_required(login_url='login')
@admin_only
def viewpdfcontract(request,pk):
     pdf = contract.objects.filter(candidate=pk)
     candidate = Candidate.objects.filter(id=pk)

     company_id = contract.objects.filter(candidate=pk).values_list('company', flat=True).first()
     
     #share = contract.objects.get(candidate=pk) 
     #id = contract.objects.get(candidate = pk)
     
     company = Company.objects.filter(pk=company_id)
     context={
      
          'candidate':candidate,
          'pdf':pdf,
          'company':company
          
     }
     return render(request,"view/pdf-contract.html",context)          

#########################     
@login_required(login_url='login')
@admin_only
def viewcontract(request,pk):
     medicals = contract.objects.filter(candidate=pk)
     candidate = Candidate.objects.filter(id=pk)
     notifycount = Notifications.objects.filter(status=False).count() 
     page = request.GET.get('page',1)
     exits = contract.objects.filter(candidate=pk).exists()
     try:
        context={
           'pk':pk,
           'page_obj':medicals,
           'notifycount':notifycount,
           'exits':exits,
           'candidate':candidate
            }
        return render(request,"view/view-contract.html",context)           
     except contract.DoesNotExist:
        context={
           'pk':pk,
           'page_obj':medicals,
           'notifycount':notifycount,
           'exits':exits,
           'candidate':candidate
            }   
        return render(request,"view/view-contract.html",context)          

##################################################
@login_required(login_url='login')
@admin_only
def editcontract(request ,pk):
      id = contract.objects.get(id = pk)
      form = CreateContractForm( instance = id )
      notifycount = Notifications.objects.filter(status=False).count()
      notify_msg = request.POST.get("emigrate_number")
      success_message = ('%(notify_msg)s contract updated successfully.') % {'notify_msg': notify_msg}
      user = request.user
      if request.method =='POST':
         form = CreateContractForm(request.POST,request.FILES, instance = id)
         #page = request.POST('medical_id')
         page = request.POST.get('edit_id')
         red = ('/view-contract/%(page)s')% {'page': page}
         if form.is_valid():
              form.save()
              Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='updated',type='CONTRACT', status=False)              
              messages.success(request,success_message)
              return redirect(red)
      pageid = contract.objects.filter(id = pk)  
      context ={'form':form,'notifycount':notifycount,'pageid':pageid}
      return render(request,"edit/edit-contract.html",context)

################
@login_required(login_url='login')
@admin_only
def addcontract(request,pk):
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = request.POST.get("vsl_name")
    success_message = ('%(notify_msg)s NKD added successfully.') % {'notify_msg': notify_msg} 
    red=('/view-contract/%(page_id)s') % {'page_id':pk}
    try:
          form = CreateContractForm()
          if request.method =='POST':
                form = CreateContractForm(request.POST,request.FILES)
                if form.is_valid():
                      obj = form.save(commit=False) # Return an object without saving to the DB
                      obj.candidate_id = pk
                      obj.save()
                      Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='new',type='CONTRACT', status=False)
                      messages.success(request,success_message)
                      return redirect(red)     
          #form = CreateMedicalForm(instance=medical_id)
          context ={'form':form,'notifycount':notifycount,'pk':pk}
          return render(request,"add/add-contract.html",context)

    except contract.DoesNotExist:
          form = CreateContractForm()
          if request.method =='POST':
                form = CreateContractForm(request.POST,request.FILES)
                if form.is_valid():
                      obj = form.save(commit=False) # Return an object without saving to the DB
                      obj.candidate_id = pk
                      obj.save()
                      Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='new',type='CONTRACT', status=False)
                      messages.success(request,success_message)
                      return redirect(red) 
          context ={'form':form,'notifycount':notifycount,'pk':pk}
          return render(request,"add/add-contract.html",context)  

##################################################
@login_required(login_url='login')
@admin_only
def deletecontract(request ,pk):
    delete = contract.objects.get(id = pk)
    delete_id = contract.objects.filter(id=pk)
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = delete
    pre_url = request.META.get('HTTP_REFERER').split("/")[-1]
    page = request.POST.get('url')
    success_message = ('%(notify_msg)s Contract deleted successfully.') % {'notify_msg': notify_msg}
    if request.method == 'POST':
          delete.delete()
          Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='deleted',type='NKD', status=False)
          messages.success(request,success_message)
          return redirect(page)
    context ={'delete':delete,'notifycount':notifycount,'pre_url':pre_url,'delete_id':delete_id}
    return render(request,"delete/delete-contract.html",context)
#################  





######ADD NKD SECTION##########
########
#################  
################
@login_required(login_url='login')
@admin_only
def addcandidatenkd(request,pk):
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = request.POST.get("kin_name")
    success_message = ('%(notify_msg)s NKD added successfully.') % {'notify_msg': notify_msg} 
    red=('/view-nkd/%(page_id)s') % {'page_id':pk}
    try:
          form = CreateCandidateNkdForm()
          if request.method =='POST':
                form = CreateCandidateNkdForm(request.POST,request.FILES)
                if form.is_valid():
                      obj = form.save(commit=False) # Return an object without saving to the DB
                      obj.candidate_id = pk
                      obj.save()
                      Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='new',type='NKD', status=False)
                      messages.success(request,success_message)
                      return redirect(red)     
          #form = CreateMedicalForm(instance=medical_id)
          context ={'form':form,'notifycount':notifycount,'pk':pk}
          return render(request,"add/add-nkd.html",context)

    except candidateNkd.DoesNotExist:
          form = CreateCandidateNkdForm()
          if request.method =='POST':
                form = CreateCandidateNkdForm(request.POST,request.FILES)
                if form.is_valid():
                      obj = form.save(commit=False) # Return an object without saving to the DB
                      obj.candidate_id = pk
                      obj.save()
                      Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='new',type='NKD', status=False)
                      messages.success(request,success_message)
                      return redirect(red) 
          context ={'form':form,'notifycount':notifycount,'pk':pk}
          return render(request,"add/add-nkd.html",context)  

##################################################

@login_required(login_url='login')
@admin_only
def viewcandidatenkd(request,pk):
     medicals = candidateNkd.objects.filter(candidate=pk)
     candidate = Candidate.objects.filter(id=pk)
     notifycount = Notifications.objects.filter(status=False).count() 
     paginator = Paginator(medicals, 10)
     page = request.GET.get('page',1)
     try:
           page_obj = paginator.page(page)
     except PageNotAnInteger:
           page_obj = paginator.page(1)
     except EmptyPage: 
           page_obj = paginator.page(paginator.num_pages) 

     context={
           'pk':pk,
           'page_obj':page_obj,
           'notifycount':notifycount,
           'candidate':candidate
     }
     try:
        return render(request,"view/view-candidate-nkd.html",context)           
     except candidateNkd.DoesNotExist:   
        return render(request,"view/view-candidate-nkd.html",context)         

################
@login_required(login_url='login')
@admin_only
def editcandidatenkd(request ,pk):
      id = candidateNkd.objects.get(id = pk)
      form = CreateCandidateNkdForm( instance = id )
      notifycount = Notifications.objects.filter(status=False).count()
      notify_msg = request.POST.get("kin_name")
      success_message = ('%(notify_msg)s NKD updated successfully.') % {'notify_msg': notify_msg}
      user = request.user
      if request.method =='POST':
         form = CreateCandidateNkdForm(request.POST,request.FILES, instance = id)
         #page = request.POST('medical_id')
         page = request.POST.get('edit_id')
         red = ('/view-nkd/%(page)s')% {'page': page}
         if form.is_valid():
              form.save()
              Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='updated',type='NKD', status=False)              
              messages.success(request,success_message)
              return redirect(red)
      pageid = candidateNkd.objects.filter(id = pk)  
      context ={'form':form,'notifycount':notifycount,'pageid':pageid}
      return render(request,"edit/edit-nkd.html",context)

#######################
@login_required(login_url='login')
@admin_only
def deletenkd(request ,pk):
    delete = candidateNkd.objects.get(id = pk)
    delete_id = candidateNkd.objects.filter(id=pk)
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = delete
    pre_url = request.META.get('HTTP_REFERER').split("/")[-1]
    page = request.POST.get('url')
    success_message = ('%(notify_msg)s NKD deleted successfully.') % {'notify_msg': notify_msg}
    if request.method == 'POST':
          delete.delete()
          Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='deleted',type='NKD', status=False)
          messages.success(request,success_message)
          return redirect(page)
    context ={'delete':delete,'notifycount':notifycount,'pre_url':pre_url,'delete_id':delete_id}
    return render(request,"delete/delete-nkd.html",context)
#################      
def delete_candidatenkd_objects(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_ids')
        can_id = request.POST.get('can_id')
        red = ('/view-nkd/%(can_id)s') % {'can_id':can_id}
        objects_to_delete = candidateNkd.objects.filter(id__in=selected_ids)
        if not objects_to_delete:
            messages.add_message(request,messages.ERROR, "No objects selected for deletion.")
            return redirect(red)
        return render(request, 'delete/multi-delete-nkd.html',{'objects_to_delete':objects_to_delete,'red':red})      

def del_multi_candidatenkd(request):
      if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_ids')
        red = request.POST.get('url')
        objects_to_delete = candidateNkd.objects.filter(id__in=selected_ids)
        objects_to_delete.delete()
        messages.success(request, "Selected objects have been deleted.")
        return redirect(red)


######ADD DOCUMENT SECTION##########
########
#################      
def delete_candidatedocument_objects(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_ids')
        can_id = request.POST.get('can_id')
        red = ('/view-candidate-document/%(can_id)s') % {'can_id':can_id}
        objects_to_delete = candidateDocument.objects.filter(id__in=selected_ids)
        if not objects_to_delete:
            messages.add_message(request,messages.ERROR, "No objects selected for deletion.")
            return redirect(red)
        return render(request, 'delete/multi-delete-document.html',{'objects_to_delete':objects_to_delete,'red':red})      

def del_multi_candidatedocument(request):
      if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_ids')
        red = request.POST.get('url')
        objects_to_delete = candidateDocument.objects.filter(id__in=selected_ids)
        objects_to_delete.delete()
        messages.success(request, "Selected objects have been deleted.")
        return redirect(red)
      
#######################
@login_required(login_url='login')
@admin_only
def deletecandidatedocument(request ,pk):
    delete = candidateDocument.objects.get(id = pk)
    delete_id = candidateDocument.objects.filter(id=pk)
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = delete
    pre_url = request.META.get('HTTP_REFERER').split("/")[-1]
    page = request.POST.get('url')
    success_message = ('%(notify_msg)s Document deleted successfully.') % {'notify_msg': notify_msg}
    if request.method == 'POST':
          delete.delete()
          Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='deleted',type='DOCUMENT', status=False)
          messages.success(request,success_message)
          return redirect(page)
    context ={'delete':delete,'notifycount':notifycount,'pre_url':pre_url,'delete_id':delete_id}
    return render(request,"delete/delete-candidate-document.html",context)

@login_required(login_url='login')
@admin_only
def viewcandidatedocument(request,pk):
     medicals = candidateDocument.objects.filter(candidate=pk)
     notifycount = Notifications.objects.filter(status=False).count() 
     candidate = Candidate.objects.filter(id=pk)
     paginator = Paginator(medicals, 10)
     page = request.GET.get('page',1)
     try:
           page_obj = paginator.page(page)
     except PageNotAnInteger:
           page_obj = paginator.page(1)
     except EmptyPage: 
           page_obj = paginator.page(paginator.num_pages) 

     context={
           'pk':pk,
           'page_obj':page_obj,
           'notifycount':notifycount,
           'candidate':candidate
     }
     try:
        return render(request,"view/view-candidate-document.html",context)           
     except candidateDocument.DoesNotExist:   
        return render(request,"view/view-candidate-document.html",context)         
     
################
@login_required(login_url='login')
@admin_only
def editcandidatedocument(request ,pk):
      id = candidateDocument.objects.get(id = pk)
      form = CreateCandidateDocumentForm( instance = id )
      notifycount = Notifications.objects.filter(status=False).count()
      notify_msg = request.POST.get("document")
      success_message = ('%(notify_msg)s Document updated successfully.') % {'notify_msg': notify_msg}
      user = request.user
      if request.method =='POST':
         form = CreateCandidateDocumentForm(request.POST,request.FILES, instance = id)
         #page = request.POST('medical_id')
         page = request.POST.get('edit_id')
         red = ('/view-candidate-document/%(page)s')% {'page': page}
         if form.is_valid():
              form.save()
              Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='updated',type='DOCUMENT', status=False)              
              messages.success(request,success_message)
              return redirect(red)
      pageid = candidateDocument.objects.filter(id = pk)  
      context ={'form':form,'notifycount':notifycount,'pageid':pageid}
      return render(request,"edit/edit-candidate-document.html",context)

################
@login_required(login_url='login')
@admin_only
def addcandidatedocument(request,pk):
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = request.POST.get("ticket_no")
    success_message = ('%(notify_msg)s Document added successfully.') % {'notify_msg': notify_msg} 
    red=('/view-candidate-document/%(page_id)s') % {'page_id':pk}
    try:
          form = CreateCandidateDocumentForm()
          if request.method =='POST':
                form = CreateCandidateDocumentForm(request.POST,request.FILES)
                if form.is_valid():
                      obj = form.save(commit=False) # Return an object without saving to the DB
                      obj.candidate_id = pk
                      obj.save()
                      #Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='new',type='DOCUMENT', status=False)
                      messages.success(request,success_message)
                      return redirect(red)     
          #form = CreateMedicalForm(instance=medical_id)
          context ={'form':form,'notifycount':notifycount,'pk':pk}
          return render(request,"add/add-candidate-document.html",context)

    except candidateDocument.DoesNotExist:
          form = CreateCandidateDocumentForm()
          if request.method =='POST':
                form = CreateCandidateDocumentForm(request.POST,request.FILES)
                if form.is_valid():
                      obj = form.save(commit=False) # Return an object without saving to the DB
                      obj.candidate_id = pk
                      obj.save()
                      Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='new',type='DOCUMENT', status=False)
                      messages.success(request,success_message)
                      return redirect(red) 
          context ={'form':form,'notifycount':notifycount,'pk':pk}
          return render(request,"add/add-candidate-document.html",context)    







######ADD TRAVEL SECTION##########
########
#################
def del_multi_travel(request):
      if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_ids')
        red = request.POST.get('url')
        objects_to_delete = Travel.objects.filter(id__in=selected_ids)
        objects_to_delete.delete()
        messages.success(request, "Selected objects have been deleted.")
        return redirect(red)
def delete_travel_objects(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_ids')
        can_id = request.POST.get('can_id')
        red = ('/view-travel/%(can_id)s') % {'can_id':can_id}
        objects_to_delete = Travel.objects.filter(id__in=selected_ids)
        if not objects_to_delete:
            messages.add_message(request,messages.ERROR, "No objects selected for deletion.")
            return redirect(red)
        return render(request, 'delete/multi-delete-travel.html',{'objects_to_delete':objects_to_delete,'red':red})      

def del_multi_travel(request):
      if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_ids')
        red = request.POST.get('url')
        objects_to_delete = Travel.objects.filter(id__in=selected_ids)
        objects_to_delete.delete()
        messages.success(request, "Selected objects have been deleted.")
        return redirect(red)
#######################
@login_required(login_url='login')
@admin_only
def deletetravel(request ,pk):
    delete = Travel.objects.get(id = pk)
    delete_id = Travel.objects.filter(id=pk)
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = delete
    pre_url = request.META.get('HTTP_REFERER').split("/")[-1]
    page = request.POST.get('url')
    success_message = ('%(notify_msg)s Travel deleted successfully.') % {'notify_msg': notify_msg}
    if request.method == 'POST':
          delete.delete()
          Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='deleted',type='MEDICAL', status=False)
          messages.success(request,success_message)
          return redirect(page)
    context ={'delete':delete,'notifycount':notifycount,'pre_url':pre_url,'delete_id':delete_id}
    return render(request,"delete/delete-travel.html",context)
@login_required(login_url='login')
@admin_only
def viewtravel(request,pk):
     medicals = Travel.objects.filter(candidate=pk)
     candidate = Candidate.objects.filter(id=pk)
     notifycount = Notifications.objects.filter(status=False).count() 
     paginator = Paginator(medicals, 10)
     page = request.GET.get('page',1)
     try:
           page_obj = paginator.page(page)
     except PageNotAnInteger:
           page_obj = paginator.page(1)
     except EmptyPage: 
           page_obj = paginator.page(paginator.num_pages) 

     context={
           'pk':pk,
           'page_obj':page_obj,
           'notifycount':notifycount,
           'candidate':candidate
     }
     try:
        return render(request,"view/view-candidate-travel.html",context)           
     except Travel.DoesNotExist:   
        return render(request,"view/view-candidate-travel.html",context)         
     
################
@login_required(login_url='login')
@admin_only
def edittravel(request ,pk):
      id = Travel.objects.get(id = pk)
      form = CreateTravelForm( instance = id )
      notifycount = Notifications.objects.filter(status=False).count()
      notify_msg = request.POST.get("ticket_no")
      success_message = ('%(notify_msg)s Travel updated successfully.') % {'notify_msg': notify_msg}
      user = request.user
      if request.method =='POST':
         form = CreateTravelForm(request.POST,request.FILES, instance = id)
         #page = request.POST('medical_id')
         page = request.POST.get('edit_id')
         red = ('/view-travel/%(page)s')% {'page': page}
         if form.is_valid():
              form.save()
              Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='updated',type='TRAVEL', status=False)              
              messages.success(request,success_message)
              return redirect(red)
      travel = Travel.objects.filter(id = pk)  
      context ={'form':form,'notifycount':notifycount,'travel':travel}
      return render(request,"edit/edit-travel.html",context)

################
@login_required(login_url='login')
@admin_only
def addtravel(request,pk):
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = request.POST.get("ticket_no")
    success_message = ('%(notify_msg)s Travel added successfully.') % {'notify_msg': notify_msg} 
    red=('/view-travel/%(page_id)s') % {'page_id':pk}
    try:
          form = CreateTravelForm()
          if request.method =='POST':
                form = CreateTravelForm(request.POST,request.FILES)
                if form.is_valid():
                      obj = form.save(commit=False) # Return an object without saving to the DB
                      obj.candidate_id = pk
                      obj.save()
                      Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='new',type='TRAVEL', status=False)
                      messages.success(request,success_message)
                      return redirect(red)     
          #form = CreateMedicalForm(instance=medical_id)
          context ={'form':form,'notifycount':notifycount,'pk':pk}
          return render(request,"add/add-candidate-travel.html",context)

    except Travel.DoesNotExist:
          form = CreateTravelForm()
          if request.method =='POST':
                form = CreateTravelForm(request.POST,request.FILES)
                if form.is_valid():
                      obj = form.save(commit=False) # Return an object without saving to the DB
                      obj.candidate_id = pk
                      obj.save()
                      Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='new',type='MEDICAL', status=False)
                      messages.success(request,success_message)
                      return redirect(red) 
          context ={'form':form,'notifycount':notifycount,'pk':pk}
          return render(request,"add/add-candidate-travel.html",context)    





########### Country start here
@login_required(login_url='login')
@admin_only
def country(request):
        country = CountryName.objects.all()
        paginator = Paginator(country, 10)
        page = request.GET.get('page',1)
        try:
              page_obj = paginator.page(page)
        except PageNotAnInteger:
              page_obj = paginator.page(1)
        except EmptyPage: 
              page_obj = paginator.page(paginator.num_pages)
        notifycount = Notifications.objects.filter(status=False).count()
        context ={ 'page_obj':page_obj,'notifycount':notifycount }
        return render(request,"view/view-country.html", context)

#############
@login_required(login_url='login')
@admin_only
def editcountry(request ,pk):
    country = CountryName.objects.get(id = pk)
    form = CreateCountryForm( instance = country )
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = request.POST.get("country_name")
    success_message = ('%(notify_msg)s Country updated successfully.') % {'notify_msg': notify_msg}
    if request.method =='POST':
         form = CreateCountryForm(request.POST, instance = country)
         if form.is_valid():
              form.save()  
              Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='updated',type='COUNTRY', status=False)
              messages.success(request,success_message) 
              return redirect ("/view-country/")
    context ={'form':form,'notifycount':notifycount}
    return render(request,"edit/edit-country.html",context)

#################
@login_required(login_url='login')
@admin_only
def addcountry(request):
        form = CreateCountryForm()
        notifycount = Notifications.objects.filter(status=False).count()
        user = request.user 
        notify_msg = request.POST.get("country_name")
        success_message = ('%(notify_msg)s Country added successfully.') % {'notify_msg': notify_msg}
        if request.method == 'POST':
              form = CreateCountryForm(request.POST)
              if form.is_valid():
                    form.save()
                    Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='new',type='COUNTRY', status=False)
                    messages.success(request, success_message)
                    return redirect ("/view-country/")
        context ={ 'form':form,'notifycount':notifycount}
        return render(request,"add/add-country.html", context)

###########
@login_required(login_url='login')
@admin_only
def deletecountry(request ,pk):
    delete = CountryName.objects.get(id = pk)
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = delete
    pre_url = request.META.get('HTTP_REFERER').split("/")[-1]
    page = request.POST.get('url')
    success_message = ('%(notify_msg)s Country Deleted successfully.') % {'notify_msg': notify_msg}
    if request.method == 'POST':
          delete.delete()
          Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='deleted',type='COUNTRY', status=False)
          messages.success(request, success_message)
          return redirect(page)
    context ={'delete':delete,'notifycount':notifycount,'pre_url':pre_url}
    return render(request,"delete/delete-country.html",context)

################
@login_required(login_url='login')
@admin_only
def importcountry(request):
    if request.method == 'POST':
            #company = CompanyResource()
            file = request.FILES['files']
            ExcelFiles.objects.create(
                  file = file
            )
            path = file.file 
            empexceldata = pd.read_excel(path)
            dbframe = empexceldata
            #print(path)
            for dbframe in dbframe.itertuples():
                  obj = CountryName.objects.create(   
                        country_name = dbframe.country_name,
                        country_code = dbframe.country_code,
                        country_phone_code = dbframe.country_phone_code
                        )                
            obj.save()
            messages.success(request,"Country Data uploaded")      
            return redirect ("/view-country/")
    return render(request,"exportsTemplates/exportCountry.html")

##################
@login_required(login_url='login')
@admin_only
def exportcountry(request):
      response = HttpResponse(content_type='text/csv')
      response['Content-Disposition'] = 'attachment; filename="Country.csv"'
      writer = csv.writer(response)
      #writer.writerow(['Grade Name'])  
      writer.writerow(['country_name'])     
      users = CountryName.objects.all().values_list('country_name')
      for user in users:
            writer.writerow(user)
      return response
#### Country End Here


####### Vendor Start here
#Vendor start here
@login_required(login_url='login')
@admin_only
def vendors(request):
        vendors = Vendors.objects.all()
        notifycount = Notifications.objects.filter(status=False).count()
        context ={ 'vendors':vendors,'notifycount':notifycount}
        return render(request,"viewTemplates/view-vendor.html", context)

#################
def addvendors(request):
        form = CreateVendorForm()
        notifycount = Notifications.objects.filter(status=False).count()
        user = request.user 
        notify_msg = 'Vendor Deleted successfully'
        if request.method == 'POST':
              form = CreateVendorForm(request.POST)
              if form.is_valid():
                    form.save()
                    Notifications.objects.create(notify_details = notify_msg , added_by_user=user , status=False)
                    messages.success(request, 'Vendor Added Successfully')
                    return redirect ("/view-vendor/")
        context ={ 'form':form,'notifycount':notifycount}
        return render(request,"addTemplates/add-vendor.html", context)

###############
@login_required(login_url='login')
@admin_only
def editvendors(request ,pk):
    vendor = Vendors.objects.get(id = pk)
    form = CreateVendorForm( instance = vendor )
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = 'Vendor updated successfully'
    if request.method =='POST':
         form = CreateVendorForm(request.POST, instance = vendor)
         if form.is_valid():
              form.save()  
              Notifications.objects.create(notify_details = notify_msg , added_by_user=user , status=False)            
              messages.success(request,'Vendor updated successfully ') 
              return redirect('/view-vendor')
    context ={'form':form,'notifycount':notifycount}
    return render(request,"editTemplates/edit-vendor.html",context)

##############
@login_required(login_url='login')
@admin_only
def deletevendors(request ,pk):
    delete = Vendors.objects.get(id = pk)
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = 'Vendor Deleted successfully'
    if request.method == 'POST':
          delete.delete()
          Notifications.objects.create(notify_details = notify_msg , added_by_user=user , status=False)
          messages.success(request, "Deleted successfully")
          return redirect('/view-vendor')
    context ={'delete':delete,'notifycount':notifycount}
    return render(request,"deleteTemplates/delete-vendor.html",context)

################
@login_required(login_url='login')
@admin_only
def importvendors(request):
    notifycount = Notifications.objects.filter(status=False).count()
    context={
          'notifycount':notifycount
    }
    if request.method == 'POST':
            #company = CompanyResource()
            file = request.FILES['files']
            ExcelFiles.objects.create(
                  file = file
            )
            path = file.file 
            empexceldata = pd.read_excel(path)
            dbframe = empexceldata
            #print(path)
            for dbframe in dbframe.itertuples():
                  obj = Vendors.objects.create(   
                        vendor_name = dbframe.vendor_name,
                        vendor_address = dbframe.vendor_address
                        )                
            obj.save()
            messages.success(request,"Vendors Data uploaded")      
            return redirect ("/view-vendor/")
    return render(request,"exportsTemplates/exportVendors.html",context)

##################
@login_required(login_url='login')
@admin_only
def exportvendors(request):
      response = HttpResponse(content_type='text/csv')
      response['Content-Disposition'] = 'attachment; filename="Vendors.csv"'
      writer = csv.writer(response)
      #writer.writerow(['Grade Name'])  
      writer.writerow(['vendor_name','vendor_address'])     
      users = Vendors.objects.all().values_list('vendor_name','vendor_address')
      for user in users:
            writer.writerow(user)
      return response



######## Office Document Start Here
#Office Document start here
#Document start here
@login_required(login_url='login')
@admin_only
def document(request):
        notifycount = Notifications.objects.filter(status=False).count()
        document = DocumentType.objects.all()
        context ={'document':document,'notifycount':notifycount }
        return render(request,"add/add-document.html", context)
@login_required(login_url='login')
@admin_only
def adddocument(request):
        form = CreateDocumentForm()
        notifycount = Notifications.objects.filter(status=False).count()
        user = request.user 
        notify_msg = request.POST.get("document_type")
        success_message = ('%(notify_msg)s Document updated successfully.') % {'notify_msg': notify_msg}
        if request.method == 'POST':
              form = CreateDocumentForm(request.POST, request.FILES)
              if form.is_valid():
                    form.save()
                    Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='new',type='DOCUMENT', status=False)
                    messages.success(request, success_message)
                    return redirect('/view-document')
        context ={ 'form':form,'notifycount':notifycount}
        return render(request,"add/add-document.html", context)
###############
@login_required(login_url='login')
@admin_only
def editdocument(request ,pk):
    document = DocumentType.objects.get(id = pk)
    form = CreateDocumentForm( instance = document )
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = request.POST.get("document_type")
    success_message = ('%(notify_msg)s Document updated successfully.') % {'notify_msg': notify_msg}
    pre_url = request.META.get('HTTP_REFERER').split("/")[-1]
    page = request.POST.get('url')
    if request.method =='POST':
         form = CreateDocumentForm(request.POST, instance = document)
         if form.is_valid():
              form.save()
              Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='new',type='COMPANY', status=False)
              messages.success(request,success_message) 
              return redirect(page)
    context ={'form':form,'notifycount':notifycount,'pre_url':pre_url}
    return render(request,"edit/edit-document.html",context)

################
@login_required(login_url='login')
@admin_only
def viewdocument(request):
        view = DocumentType.objects.all()
        paginator = Paginator(view, 10)
        page = request.GET.get('page',1)
        try:
              page_obj = paginator.page(page)
        except PageNotAnInteger:
              page_obj = paginator.page(1)
        except EmptyPage: 
              page_obj = paginator.page(paginator.num_pages) 
        notifycount = Notifications.objects.filter(status=False).count()
        context ={ 'page_obj':page_obj,'notifycount':notifycount }
        return render(request,"view/view-document.html", context)

###########
@login_required(login_url='login')
@admin_only
def deletedocument(request ,pk):
    delete = DocumentType.objects.get(id = pk)
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = delete
    pre_url = request.META.get('HTTP_REFERER').split("/")[-1]
    page = request.POST.get('url')
    success_message = ('%(notify_msg)s Document Deleted successfully.') % {'notify_msg': notify_msg}
    if request.method == 'POST':
          delete.delete()
          Notifications.objects.create(notify_details = notify_msg , added_by_user=user , status=False)
          messages.success(request, success_message)
          return redirect(page)
    context ={'delete':delete,'notifycount':notifycount,'pre_url':pre_url}
    return render(request,"delete/delete-document.html",context)
################
@login_required(login_url='login')
@admin_only
def importdocument(request):
    notifycount = Notifications.objects.filter(status=False).count()
    context={
          'notifycount':notifycount
    }

    if request.method == 'POST' and bool(request.FILES.get('files', False)) == True:            
            file = request.FILES['files']
            ExcelFiles.objects.create(
                  file = file
            )
            path = file.file 
            empexceldata = pd.read_excel(path)
            dbframe = empexceldata
            #print(path)
            for dbframe in dbframe.itertuples():
                  obj = DocumentType.objects.create(   
                        document_type = dbframe.document_type,
                        hide_expiry_date = dbframe.hide_expiry_date
                        )                
            obj.save()
            messages.success(request,"Document Data uploaded")      
            return redirect ("/view-document/")
    else:
     messages.success(request,"File is empty")      
     return redirect ("/view-document/")
       
    
##################
@login_required(login_url='login')
@admin_only
def exportdocument(request):
      response = HttpResponse(content_type='text/csv')
      response['Content-Disposition'] = 'attachment; filename="DocumentType.csv"'
      writer = csv.writer(response)
      #writer.writerow(['Grade Name'])  
      writer.writerow(['DocumentType'])     
      users = DocumentType.objects.all().values_list('DocumentType')
      for user in users:
            writer.writerow(user)
      return response
### Document End Here


####### Hospital Start Here
#hospital start here
@login_required(login_url='login')
@admin_only
def hospital(request):
        hospital = Hospital.objects.all()
        paginator = Paginator(hospital, 10)
        page = request.GET.get('page',1)
        try:
              page_obj = paginator.page(page)
        except PageNotAnInteger:
              page_obj = paginator.page(1)
        except EmptyPage: 
              page_obj = paginator.page(paginator.num_pages) 
        notifycount = Notifications.objects.filter(status=False).count()
        context ={ 'page_obj':page_obj,'notifycount':notifycount }
        return render(request,"view/view-hospital.html" ,context)

########################
@login_required(login_url='login')
@admin_only
def edithospital(request ,pk):

    hospital = Hospital.objects.get(id = pk)
    form = CreateHospitalForm( instance = hospital )
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = request.POST.get("hospital_name")
    success_message = ('%(notify_msg)s Company updated successfully.') % {'notify_msg': notify_msg}
    pre_url = request.META.get('HTTP_REFERER').split("/")[-1]
    page = request.POST.get('url')
    if request.method =='POST':
         form = CreateHospitalForm(request.POST, instance = hospital)
         if form.is_valid():
              form.save()
              Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='updated',type='HOSPITAL', status=False)
              messages.success(request,success_message) 
              return redirect(page)
    context ={'form':form,'notifycount':notifycount,'pre_url':pre_url}
    return render(request,"edit/edit-hospital.html",context)
#hospital start here
@login_required(login_url='login')
@admin_only
def addhospital(request):
        form = CreateHospitalForm()
        notifycount = Notifications.objects.filter(status=False).count()
        user = request.user 
        notify_msg = request.POST.get("hospital_name")
        success_message = ('%(notify_msg)s Hospital added successfully.') % {'notify_msg': notify_msg}
        pre_url = request.META.get('HTTP_REFERER').split("/")[-1]
        page = request.POST.get('url')
        if request.method == 'POST':
              form = CreateHospitalForm(request.POST, request.FILES)
              if form.is_valid():
                    form.save()
                    Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='new',type='HOSPITAL', status=False)
                    messages.success(request, success_message)
                    return redirect(page)
        context ={ 'form':form,'notifycount':notifycount,'pre_url':pre_url}
        return render(request,"add/add-hospital.html" ,context)
###########
@login_required(login_url='login')
@admin_only
def deletehospital(request ,pk):
    delete = Hospital.objects.get(id = pk)
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = delete
    pre_url = request.META.get('HTTP_REFERER').split("/")[-1]
    page = request.POST.get('url')
    success_message = ('%(notify_msg)s Company Deleted successfully.') % {'notify_msg': notify_msg}
    if request.method == 'POST':
          delete.delete()
          Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='deleted',type='HOSPITAL', status=False)
          messages.success(request, success_message)
          return redirect(page)
    context ={'delete':delete,'notifycount':notifycount,'pre_url':pre_url}
    return render(request,"delete/delete-hospital.html",context)

#####################
@login_required(login_url='login')
@admin_only
def importhospital(request):
    notifycount = Notifications.objects.filter(status=False).count()
    context={
          'notifycount':notifycount
    }
    if request.method == 'POST':
            #company = CompanyResource()
            file = request.FILES['files']
            ExcelFiles.objects.create(
                  file = file
            )
            path = file.file 
            empexceldata = pd.read_excel(path)
            dbframe = empexceldata
            #print(path)
            for dbframe in dbframe.itertuples():
                  obj = Hospital.objects.create(   
                        hospital_name = dbframe.hospital_name,
                        doctor_name = dbframe.doctor_name,
                        hospital_address = dbframe.hospital_address,
                        hospital_city = dbframe.hospital_city,
                        hospital_state = dbframe.hospital_state,
                        hospital_phone = dbframe.hospital_phone,
                        hospital_email = dbframe.hospital_email
                        
                        )
                            
            obj.save()
            messages.success(request,"Port Agent Data uploaded")      
            return redirect ("/view-hospital/")
    return render(request,"exportsTemplates/exportHospital.html",context)
##################
@login_required(login_url='login')
@admin_only
def exporthospital(request):
      response = HttpResponse(content_type='text/csv')
      response['Content-Disposition'] = 'attachment; filename="Hospital.csv"'
      writer = csv.writer(response)
      #writer.writerow(['Grade Name'])  
      writer.writerow(['hospital_name','doctor_name','hospital_address','hospital_city','hospital_state','hospital_phone','hospital_email','hospital_image'])     
      users = Hospital.objects.all().values_list('hospital_name','doctor_name','hospital_address','hospital_city','hospital_state','hospital_phone','hospital_email','hospital_image')
      for user in users:
            writer.writerow(user)
      return response
##### Hospital End Here



##### Port agent start here
@login_required(login_url='login')
@admin_only
def portagent(request):
        notifycount = Notifications.objects.filter(status=False).count()
        portagent = PortAgent.objects.all()
        paginator = Paginator(portagent, 10)
        page = request.GET.get('page',1)
        try:
              page_obj = paginator.page(page)
        except PageNotAnInteger:
              page_obj = paginator.page(1)
        except EmptyPage: 
              page_obj = paginator.page(paginator.num_pages) 
        context ={ 'page_obj':page_obj,'notifycount':notifycount }
        return render(request,"view/view-agentport.html" ,context)
######################
@login_required(login_url='login')
@admin_only
def addportagent(request):
        form = CreatePortAgentForm()
        notifycount = Notifications.objects.filter(status=False).count()
        user = request.user 
        notify_msg = request.POST.get("port_agent")
        success_message = ('%(notify_msg)s added successfully.') % {'notify_msg': notify_msg}
        if request.method == 'POST':
              form = CreatePortAgentForm(request.POST)
              if form.is_valid():
                    form.save()
                    Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='new',type='AGENT', status=False)
                    messages.success(request,success_message)
                    return redirect ("/view-agentport/")
              
        context ={ 'form':form,'notifycount':notifycount}
        return render(request,"add/add-agentport.html" ,context)
########
@login_required(login_url='login')
@admin_only
def editportagent(request ,pk):

    country = PortAgent.objects.get(id = pk)
    form = CreatePortAgentForm( instance = country )
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = request.POST.get("port_agent")
    success_message = ('%(notify_msg)s Agent edited successfully.') % {'notify_msg': notify_msg}
    pre_url = request.META.get('HTTP_REFERER').split("/")[-1]
    page = request.POST.get('url')

    if request.method =='POST':
         form = CreatePortAgentForm(request.POST, instance = country)
         if form.is_valid():
              form.save() 
              Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='updated',type='AGENT', status=False)
              messages.success(request,success_message)
              return redirect(page) 
    context ={'form':form,'notifycount':notifycount,'pre_url':pre_url}
    return render(request,"edit/edit-agentport.html" ,context)

@login_required(login_url='login')
@admin_only
def deleteportagent(request ,pk):

    delete = PortAgent.objects.get(id = pk)
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = delete
    pre_url = request.META.get('HTTP_REFERER').split("/")[-1]
    page = request.POST.get('url')
    success_message = ('%(notify_msg)s Deleted successfully.') % {'notify_msg': notify_msg}
    if request.method == 'POST':
          delete.delete()
          Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='deleted',type='AGENT', status=False)
          messages.success(request, success_message)
          return redirect(page)

    context ={'delete':delete,'notifycount':notifycount,'pre_url':pre_url}
    return render(request,"delete/delete-agentport.html",context)
################
@login_required(login_url='login')
@admin_only
def importportagent(request):
    notifycount = Notifications.objects.filter(status=False).count()
    context={
          'notifycount':notifycount
    }
    if request.method == 'POST':
            #company = CompanyResource()
            file = request.FILES['files']
            ExcelFiles.objects.create(
                  file = file
            )
            path = file.file 
            empexceldata = pd.read_excel(path)
            dbframe = empexceldata
            #print(path)
            for dbframe in dbframe.itertuples():
                  obj = PortAgent.objects.create(   
                        port_agent = dbframe.port_agent,
                        port_contact_person = dbframe.port_contact_person,
                        port_agent_address = dbframe.port_agent_address,
                        port_agent_phone = dbframe.port_agent_phone,
                        port_agent_email = dbframe.port_agent_email,
                        port_agent_city = dbframe.port_agent_city,
                        port_agent_state = dbframe.port_agent_state,
                        port_agent_country = dbframe.port_agent_country
                        )           
            obj.save()
            messages.success(request,"Port Agent Data uploaded")      
            return redirect ("/view-agentport/")
    return render(request,"exportsTemplates/exportPortagent.html",context)
##################
@login_required(login_url='login')
@admin_only
def exportportagent(request):
      response = HttpResponse(content_type='text/csv')
      response['Content-Disposition'] = 'attachment; filename="PortAgentData.csv"'
      writer = csv.writer(response)
      #writer.writerow(['Grade Name'])  
      writer.writerow(['port_agent','port_contact_person','port_agent_address','port_agent_phone','port_agent_email','port_agent_city','port_agent_state','port_agent_country'])     
      users = PortAgent.objects.all().values_list('port_agent','port_contact_person','port_agent_address','port_agent_phone','port_agent_email','port_agent_city','port_agent_state','port_agent_country')
      for user in users:
            writer.writerow(user)
      return response

######Port agent end here


#### port start here
@login_required(login_url='login')
@admin_only
def port(request):
        port = Port.objects.all()
        paginator = Paginator(port, 10)
        page = request.GET.get('page',1)
        try:
              page_obj = paginator.page(page)
        except PageNotAnInteger:
              page_obj = paginator.page(1)
        except EmptyPage: 
              page_obj = paginator.page(paginator.num_pages) 
        notifycount = Notifications.objects.filter(status=False).count()            
        context ={'page_obj':page_obj,'notifycount':notifycount}
        return render(request,"view/view-port.html", context)
#grade port end
@login_required(login_url='login')
@admin_only
def addport(request):
        form = CreatePortForm()
        notifycount = Notifications.objects.filter(status=False).count()
        user = request.user 
        notify_msg = request.POST.get("port_name")
        success_message = ('%(notify_msg)s Port added successfully.') % {'notify_msg': notify_msg}
        if request.method == 'POST':
              form = CreatePortForm(request.POST)
              if form.is_valid():
                    form.save()
                    Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='new',type='PORT', status=False)
                    messages.success(request,success_message)          

        context ={'form':form,'notifycount':notifycount}
        return render(request,"add/add-port.html", context)

@login_required(login_url='login')
@admin_only
def editport(request ,pk):

    edit = Port.objects.get(id = pk)
    form = CreatePortForm( instance = edit )
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = request.POST.get("port_name")
    success_message = ('%(notify_msg)s Port updated successfully.') % {'notify_msg': notify_msg}
    pre_url = request.META.get('HTTP_REFERER').split("/")[-1]
    page = request.POST.get('url')
    

    if request.method =='POST':
         form = CreatePortForm(request.POST, instance = edit)
         if form.is_valid():
              form.save()
              Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='updated',type='PORT', status=False)
              messages.success(request,success_message) 
              return redirect(page)

    context ={'form':form,'notifycount':notifycount,'pre_url':pre_url}
    return render(request,"edit/edit-port.html",context)
##########
@login_required(login_url='login')
@admin_only
def deleteport(request ,pk):
    delete = Port.objects.get(id = pk)
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = delete
    pre_url = request.META.get('HTTP_REFERER').split("/")[-1]
    page = request.POST.get('url')
    success_message = ('%(notify_msg)s Port Deleted successfully.') % {'notify_msg': notify_msg}
    if request.method == 'POST':
          delete.delete()
          Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='deleted',type='PORT', status=False)
          messages.success(request,success_message)
          return redirect(page)

    context ={'delete':delete,'notifycount':notifycount,'pre_url':pre_url}
    return render(request,"delete/delete-port.html",context)
##############
def importport(request):
    notifycount = Notifications.objects.filter(status=False).count()
    context={
          'notifycount':notifycount
    }
    if request.method == 'POST':
            #company = CompanyResource()
            file = request.FILES['files']
            ExcelFiles.objects.create(
                  file = file
            )
            path = file.file 
            empexceldata = pd.read_excel(path)
            dbframe = empexceldata
            #print(path)
            for dbframe in dbframe.itertuples():
                  obj = Port.objects.create(   
                        port_name = dbframe.port_name
                        )           
            obj.save()
            messages.success(request,"Port Data uploaded")      
            return redirect ("/view-port/")
    return render(request,"exportsTemplates/exportPort.html",context)
#############
def exportport(request):
      response = HttpResponse(content_type='text/csv')
      response['Content-Disposition'] = 'attachment; filename="PortData.csv"'
      writer = csv.writer(response)
      #writer.writerow(['Grade Name'])  
      writer.writerow(['port_name'])     
      users = Port.objects.all().values_list('port_name')

      for user in users:
            writer.writerow(user)
      return response





#### Grade star here

#grade start here
@login_required(login_url='login')
def grade(request):
        grade = Grade.objects.all() 
        paginator = Paginator(grade, 10)
        page = request.GET.get('page',1)
        try:
              page_obj = paginator.page(page)
        except PageNotAnInteger:
              page_obj = paginator.page(1)
        except EmptyPage: 
              page_obj = paginator.page(paginator.num_pages) 
        notifycount = Notifications.objects.filter(status=False).count() 
        context ={'page_obj':page_obj,'notifycount':notifycount}              
        return render(request,"view/view-grade.html",context)
## Grade Add here
@login_required(login_url='login')
def addgrade(request):
        form = CreateGradeForm()
        notifycount = Notifications.objects.filter(status=False).count()
        user = request.user 
        notify_msg = request.POST.get("grade_name")
        success_message = ('%(notify_msg)s Grade added successfully.') % {'notify_msg': notify_msg}
        if request.method=='POST':
              form = CreateGradeForm(request.POST)
              if form.is_valid():
                form.save()
                Notifications.objects.create(notify_details = notify_msg , added_by_user=user , status=False)
                messages.success(request,success_message)
                return redirect('/view-grade/')

        context ={'form':form,'notifycount':notifycount }
        return render(request,"add/add-grade.html",context)

@login_required(login_url='login')
@admin_only
def editgrade(request ,pk):

    edit = Grade.objects.get(id = pk)
    form = CreateGradeForm( instance = edit )
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = request.POST.get("grade_name")
    success_message = ('%(notify_msg)s Grade updated successfully.') % {'notify_msg': notify_msg}
    pre_url = request.META.get('HTTP_REFERER').split("/")[-1]
    page = request.POST.get('url')
    if request.method =='POST':
         form = CreateGradeForm(request.POST, instance = edit)
         if form.is_valid():
              form.save()
              Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='updated',type='GRADE', status=False)
              messages.success(request,success_message) 
              return redirect(page)

    context ={'form':form,'notifycount':notifycount,'pre_url':pre_url}
    return render(request,"edit/edit-grade.html",context)

@login_required(login_url='login')
@admin_only
def deletegrade(request ,pk):

    delete = Grade.objects.get(id = pk)
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = delete
    pre_url = request.META.get('HTTP_REFERER').split("/")[-1]
    page = request.POST.get('url')
    success_message = ('%(notify_msg)s Grade Deleted successfully.') % {'notify_msg': notify_msg}
    if request.method == 'POST':
          delete.delete()
          Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='deleted',type='GRADE', status=False)
          messages.success(request, success_message)
          return redirect(page)

    context ={'delete':delete,'notifycount':notifycount,'pre_url':pre_url}
    return render(request,"delete/delete-grade.html",context)


def importgrade(request):
    notifycount = Notifications.objects.filter(status=False).count()
    context={
          'notifycount':notifycount
    }
    if request.method == 'POST':
            #company = CompanyResource()
            file = request.FILES['files']
            ExcelFiles.objects.create(
                  file = file
            )
            path = file.file 
            empexceldata = pd.read_excel(path)
            dbframe = empexceldata
            #print(path)
            for dbframe in dbframe.itertuples():
                  obj = Grade.objects.create(   
                        grade_name = dbframe.grade_name
                        )           
            obj.save()
            messages.success(request,"Grade Data uploaded")      
            return redirect ("/view-grade/")
    return render(request,"exportsTemplates/exportGrade.html",context)

def exportgrade(request):
      response = HttpResponse(content_type='text/csv')
      response['Content-Disposition'] = 'attachment; filename="GradeData.csv"'
      writer = csv.writer(response)
      #writer.writerow(['Grade Name'])  
      writer.writerow(['grade_name'])     
      users = Grade.objects.all().values_list('grade_name')

      for user in users:
            writer.writerow(user)
      return response

##### Grade end here


##### Rank start here
#rank view here
@login_required(login_url='login')
def rank(request):
        rank = Rank.objects.all()
        paginator = Paginator(rank, 10)
        page = request.GET.get('page',1)
        try:
              page_obj = paginator.page(page)
        except PageNotAnInteger:
              page_obj = paginator.page(1)
        except EmptyPage: 
              page_obj = paginator.page(paginator.num_pages) 
        notifycount = Notifications.objects.filter(status=False).count()
        context ={'page_obj':page_obj,'notifycount':notifycount}
        return render(request,"view/view-rank.html",context)

### rank edit here
@login_required(login_url='login')
@admin_only
def editrank(request ,pk):

    edit = Rank.objects.get(id = pk)
    form = CreateRankForm( instance = edit )
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user
    notify_msg = request.POST.get("rank_name")
    success_message = ('%(notify_msg)s Rank edit successfully.') % {'notify_msg': notify_msg} 

    if request.method =='POST':
         form = CreateRankForm(request.POST, instance = edit)
         if form.is_valid():
              form.save() 
              Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='updated',type='RANK', status=False)
              messages.success(request,success_message)
              return redirect('/view-rank/')

    context ={'form':form,'notifycount':notifycount}
    return render(request,"edit/edit-rank.html",context)

#Rank add here
@login_required(login_url='login')
def addrank(request):
        form = CreateRankForm()
        notifycount = Notifications.objects.filter(status=False).count()
        user = request.user 
        notify_msg = request.POST.get("rank_name")
        success_message = ('%(notify_msg)s Rank added successfully.') % {'notify_msg': notify_msg}
        if request.method=='POST':
              form = CreateRankForm(request.POST)
              if form.is_valid():
                form.save()
                Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='new',type='RANK', status=False)
                messages.success(request,success_message)
                return redirect('/view-rank/')

        context ={'form':form ,'notifycount':notifycount}
        return render(request,"add/add-rank.html",context)

## Rank delete Here
@login_required(login_url='login')
@admin_only
def deleterank(request ,pk):

    delete = Rank.objects.get(id = pk)
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = delete
    pre_url = request.META.get('HTTP_REFERER').split("/")[-1]
    page = request.POST.get('url')
    success_message = ('%(notify_msg)s Rank Deleted successfully.') % {'notify_msg': notify_msg}
    if request.method == 'POST':
          delete.delete()
          Notifications.objects.create(notify_details = notify_msg , added_by_user=user , status=False)
          messages.success(request, success_message)
          return redirect(page)

    context ={'delete':delete,'notifycount':notifycount,'pre_url':pre_url}
    return render(request,"delete/delete-rank.html",context)


def importrank(request):
    notifycount = Notifications.objects.filter(status=False).count()
    context = {
          'notifycount':notifycount
    }
    if request.method == 'POST':
            #company = CompanyResource()
            file = request.FILES['files']
            ExcelFiles.objects.create(
                  file = file
            )
            path = file.file 
            empexceldata = pd.read_excel(path)
            dbframe = empexceldata
            #print(path)
            for dbframe in dbframe.itertuples():
                  obj = Rank.objects.create(   
                        rank_name = dbframe.rank_name,
                        rank_order = dbframe.rank_order,
                        rank_category = dbframe.rank_category
                        )           
            obj.save()
            messages.success(request,"Rank Data uploaded")      
            return redirect ("/view-rank/")
    return render(request,"exportsTemplates/exportRank.html",context)

def exportrank(request):
      response = HttpResponse(content_type='text/csv')
      response['Content-Disposition'] = 'attachment; filename="RankData.csv"'
      writer = csv.writer(response)
      writer.writerow(['Rank Name'])  
      writer.writerow(['rank_name','rank_order','rank_category'])     
      users = Rank.objects.all().values_list('rank_name','rank_order','rank_category')

      for user in users:
            writer.writerow(user)
      return response

######Rank end here

###### Experience start here

#experience end here
@login_required(login_url='login')
@admin_only
def experience(request):
        exp = Experience.objects.all()
        paginator = Paginator(exp, 10)
        page = request.GET.get('page',1)
        try:
              page_obj = paginator.page(page)
        except PageNotAnInteger:
              page_obj = paginator.page(1)
        except EmptyPage: 
              page_obj = paginator.page(paginator.num_pages) 
        notifycount = Notifications.objects.filter(status=False).count()       
        context ={'page_obj':page_obj,'notifycount':notifycount}
        return render(request,"view/view-experience.html",context)
#experience end here

@login_required(login_url='login')
@admin_only
def editexperience(request ,pk):

    edit = Experience.objects.get(id = pk)
    form = CreateExperienceForm( instance = edit )
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = request.POST.get("experience")
    success_message = ('%(notify_msg)s Experience edited successfully.') % {'notify_msg': notify_msg}

    if request.method =='POST':
         form = CreateExperienceForm(request.POST, instance = edit)
         if form.is_valid():
              form.save()
              Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='updated',type='EXPERIENCE', status=False)
              messages.success(request,success_message) 
              return redirect('/view-experience/')

    context ={'form':form,'notifycount':notifycount}
    return render(request,"edit/edit-experience.html",context)

#experience end here
@login_required(login_url='login')
def addexperience(request):
        form = CreateExperienceForm()
        notifycount = Notifications.objects.filter(status=False).count()
        user = request.user 
        notify_msg = request.POST.get("experience")
        success_message = ('%(notify_msg)s Experience added successfully.') % {'notify_msg': notify_msg}
        if request.method=='POST':
              form = CreateExperienceForm(request.POST)
              if form.is_valid():
                form.save()
                Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='new',type='EXPERIENCE', status=False)
                messages.success(request,success_message) 
                return redirect('/view-experience')

        context ={'form':form ,'notifycount':notifycount }
        return render(request,"add/add-experience.html",context)

## delete experience
@login_required(login_url='login')
@admin_only
def deleteexperience(request ,pk):

    delete = Experience.objects.get(id = pk)
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = delete
    pre_url = request.META.get('HTTP_REFERER').split("/")[-1]
    page = request.POST.get('url')
    success_message = ('%(notify_msg)s Experience Deleted successfully.') % {'notify_msg': notify_msg}
    if request.method == 'POST':
          delete.delete()
          Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='deleted',type='EXPERIENCE', status=False)
          messages.success(request,success_message) 
          return redirect(page)

    context ={'delete':delete,'notifycount':notifycount,'pre_url':pre_url}
    return render(request,"delete/delete-experience.html",context)

#experience end here
def importexperience(request):
    notifycount = Notifications.objects.filter(status=False).count()
    context={
          'notifycount':notifycount
    }
    if request.method == 'POST':
            #company = CompanyResource()
            file = request.FILES['files']
            ExcelFiles.objects.create(
                  file = file
            )
            path = file.file 
            empexceldata = pd.read_excel(path)
            dbframe = empexceldata
            #print(path)
            for dbframe in dbframe.itertuples():
                  obj = Experience.objects.create(   
                        experience = dbframe.experience
                        )           
            obj.save()
            messages.success(request,"Experience Data uploaded")      

            return redirect ("/view-experience/")
    return render(request,"exportsTemplates/exportExperience.html",context)
######################################
def exportexperience(request):
      response = HttpResponse(content_type='text/csv')
      response['Content-Disposition'] = 'attachment; filename="ExperienceData.csv"'
      writer = csv.writer(response)
      writer.writerow(['Experience Name'])  
      writer.writerow(['experience'])     
      users = Experience.objects.all().values_list('experience')

      for user in users:
            writer.writerow(user)
      return response



##### VSL starts here
#Edit VSL start here
@login_required(login_url='login')
@admin_only
def editvsl(request ,pk):

    editvessel = Vessel.objects.get(id = pk)
    form = CreateVesselForm( instance = editvessel )
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = 'Vessel edited successfully'
    if request.method =='POST':
         form = CreateVesselForm(request.POST, instance = editvessel)
         if form.is_valid():
              form.save()
              Notifications.objects.create(notify_details = notify_msg , added_by_user=user , status=False)              
              messages.success(request,'Vessel updated successfully ') 
              return redirect('/view-vessel/')

    vessel = Vessel.objects.all()
    context ={'form':form,'vessel':vessel,'notifycount':notifycount }
    return render(request,"editTemplates/edit-vessel.html",context)


@login_required(login_url='login')
def addvsl(request):
        form = CreateVslForm()
        notifycount = Notifications.objects.filter(status=False).count()
        user = request.user 
        notify_msg = 'VSL Name added successfully'
        if request.method == 'POST':
              form = CreateVslForm(request.POST)
              if form.is_valid():
                    form.save()
                    Notifications.objects.create(notify_details = notify_msg , added_by_user=user , status=False)
                    messages.success(request, 'VSL Name Added Successfully')

        context ={ 'form':form,'notifycount':notifycount}
        return render(request,"addTemplates/add-vsl.html", context)


@login_required(login_url='login')
def vsl(request):
        vsl = VslType.objects.all()
        notifycount = Notifications.objects.filter(status=False).count()
        context ={ 'vsl':vsl ,'notifycount':notifycount}
        return render(request,"viewTemplates/view-vsl.html", context)

def importvsl(request):
    notifycount = Notifications.objects.filter(status=False).count()
    context ={
          'notifycount':notifycount
    }
    if request.method == 'POST':
            #company = CompanyResource()
            file = request.FILES['files']
            ExcelFiles.objects.create(
                  file = file
            )
            path = file.file 
            empexceldata = pd.read_excel(path)
            dbframe = empexceldata
            #print(file)
            for dbframe in dbframe.itertuples():
                  obj = Vessel.objects.create(   
                        vsl_name = dbframe.vsl_name,
                        vsl_type = dbframe.vsl_type,
                        vsl_company = dbframe.vsl_company,
                        IMO_Number = dbframe.IMO_Number,
                        vsl_flag = dbframe.vsl_flag
                        )           
            obj.save()
            messages.success(request,"VSL Data uploaded")      

            return redirect ("/view-vsl/")
    return render(request,"exportsTemplates/exportVsl.html", context)

def exportvsl(request):
      response = HttpResponse(content_type='text/csv')
      response['Content-Disposition'] = 'attachment; filename="VslData.csv"'
      writer = csv.writer(response)
      writer.writerow(['Vsl Name'])  
      writer.writerow(['vsl_name','vsl_type','vsl_company','IMO_Number','vsl_flag'])     
      users = VslType.objects.all().values_list('vsl_name','vsl_type','vsl_company','IMO_Number','vsl_flag')

      for user in users:
            writer.writerow(user)
      return response

#####vessel start here
@login_required(login_url='login')
@admin_only
def vessel(request):
        vessel = Vessel.objects.all()
        paginator = Paginator(vessel, 10)
        page = request.GET.get('page',1)
        try:
            vessel = paginator.page(page)
        except PageNotAnInteger:
            vessel = paginator.page(1)
        except EmptyPage: 
            vessel = paginator.page(paginator.num_pages) 
        notifycount = Notifications.objects.filter(status=False).count()      
        context ={'page_obj':vessel,'notifycount':notifycount}
        return render(request,"view/view-vessel.html" ,context)

#################################

@login_required(login_url='login')
@admin_only
def addvessel(request):
        form = CreateVesselForm()
        notifycount = Notifications.objects.filter(status=False).count()
        user = request.user 
        notify_msg = request.POST.get("vessel_name")
        success_message = ('%(notify_msg)s Vessel Added successfully.') % {'notify_msg': notify_msg}
        if request.method =='POST':
            form = CreateVesselForm(request.POST)
            if form.is_valid():
                form.save()
                Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='new',type='VESSEL', status=False)
                messages.success(request,success_message)
                return redirect('/view-vessel/')
        
        context ={'form':form,'notifycount':notifycount}
        return render(request,"add/add-vessel.html" ,context)
# vessel end here
#Edit company start here
@login_required(login_url='login')
@admin_only
def editvessel(request ,pk):

    edit = Vessel.objects.get(id = pk)
    form = CreateVesselForm( instance = edit )
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = edit
    pre_url = request.META.get('HTTP_REFERER').split("/")[-1]
    page = request.POST.get('url')
    success_message = ('%(edit)s Vessel updated successfully.') % {'edit': edit}


    if request.method =='POST':
         form = CreateVesselForm(request.POST, instance = edit)
         if form.is_valid():
              form.save()
              Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='updated',type='VESSEL', status=False)
              messages.success(request,success_message) 
              return redirect(page)
    vessel = Vessel.objects.all()
    context ={'form':form,'vessel':vessel,'notifycount':notifycount,'pre_url':pre_url}
    return render(request,"edit/edit-vessel.html",context)

#vessel end here
@login_required(login_url='login')
@admin_only
def deletevessel(request ,pk):

    delete = Vessel.objects.get(id = pk)
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = delete
    pre_url = request.META.get('HTTP_REFERER').split("/")[-1]
    page = request.POST.get('url')
    success_message = ('%(delete)s Vessel Deleted successfully.') % {'delete': delete}
    if request.method == 'POST':
          delete.delete()
          Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='deleted',type='VESSEL', status=False)
          messages.success(request, success_message)
          return redirect(page)

    context ={'delete':delete, 'notifycount':notifycount,'pre_url':pre_url}
    return render(request,"delete/delete-vessel.html",context)


# import using django import   
def importvessel(request):
    notifycount = Notifications.objects.filter(status=False).count()
    context={
          'notifycount':notifycount
    }
    if request.method == 'POST':
            #company = CompanyResource()
            file = request.FILES['files']
            ExcelFiles.objects.create(
                  file = file
            )
            path = file.file 
            empexceldata = pd.read_excel(path)
            dbframe = empexceldata
            #print(file)
            for dbframe in dbframe.itertuples():
                  obj = Vessel.objects.create(   
                        vessel_name = dbframe.vessel_name
                        )           
            obj.save()
            messages.success(request,"Vessel Data uploaded")      

            return redirect ("/view-vessel/")
    return render(request,"exportsTemplates/exportVessel.html", context)

def exportvessel(request):
      response = HttpResponse(content_type='text/csv')
      response['Content-Disposition'] = 'attachment; filename="VesselData.csv"'
      writer = csv.writer(response)
      writer.writerow(['Vessel Name'])  
      writer.writerow(['vessel_name'])     
      users = Vessel.objects.all().values_list('vessel_name')

      for user in users:
            writer.writerow(user)
      return response



######Edit company start here
@login_required(login_url='login')
@admin_only
def editcompany(request ,pk):

    editcompany = Company.objects.get(id = pk)
    form = CreateCompanyForm( instance = editcompany )
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = editcompany
    success_message = ('%(editcompany)s Company updated successfully.') % {'editcompany': editcompany}
 
    if request.method =='POST':
         form = CreateCompanyForm(request.POST, instance = editcompany)
         if form.is_valid():
              form.save()
              Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='updated',type='COMPANY', status=False)
              messages.success(request,success_message) 
              return redirect('/view-company')

    company = Company.objects.all()
    context ={'form':form,'companys':company,'notifycount':notifycount }
    return render(request,"edit/edit-company.html",context)


##company start here
@login_required(login_url='login')
def company(request):
    company = Company.objects.all()
    paginator = Paginator(company, 10)
    page = request.GET.get('page',1)
    try:
       company = paginator.page(page)
    except PageNotAnInteger:
       company = paginator.page(1)
    except EmptyPage: 
       company = paginator.page(paginator.num_pages) 
    notifycount = Notifications.objects.filter(status=False).count()
    context ={'page_obj':company,'notifycount':notifycount}
    return render(request,"view/view-company.html", context)
#company end here

########################################
@login_required(login_url='login')
def addcompany(request):
    form = CreateCompanyForm()
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = request.POST.get("company_name")
    success_message = ('%(notify_msg)s Company updated successfully.') % {'notify_msg': notify_msg}
    if request.method =='POST':
         form = CreateCompanyForm(request.POST)
         if form.is_valid():
              form.save()
              Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='new',type='COMPANY', status=False)
              messages.success(request,success_message)
              return redirect('/view-company')
               
    companys = Company.objects.all()
    context ={'form':form,'companys':companys,'notifycount':notifycount}           
    return render(request,"add/add-company.html", context)

#####################################
@login_required(login_url='login')
@admin_only
def deletecompany(request ,pk):
    delete = Company.objects.get(id = pk)
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = delete
    pre_url = request.META.get('HTTP_REFERER').split("/")[-1]
    page = request.POST.get('url')
    success_message = ('%(notify_msg)s Company Deleted successfully.') % {'notify_msg': notify_msg}
    if request.method == 'POST':
          delete.delete()
          Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='deleted',type='COMPANY', status=False)
          messages.success(request, success_message)
          return redirect(page)

    context ={'delete':delete, 'notifycount':notifycount,'pre_url':pre_url}
    return render(request,"delete/delete-company.html",context)

######################################
@login_required(login_url='login')
@admin_only   
def importcompany(request):
    notifycount = Notifications.objects.filter(status=False).count()
    context ={'notifycount':notifycount}
    if request.method == 'POST':
            #company = CompanyResource()
            file = request.FILES['files']
            ExcelFiles.objects.create(
                  file = file
            )
            path = file.file 
            empexceldata = pd.read_excel(path)
            dbframe = empexceldata
            #print(path)
            for dbframe in dbframe.itertuples():
                  obj = Company.objects.create(   
                        company_name = dbframe.company_name,
                        contact_person = dbframe.contact_person,
                        address = dbframe.address,
                        phone = dbframe.phone,
                        email = dbframe.email,
                        management = dbframe.management
                        )           
            obj.save()
            messages.success(request,"Company Data uploaded")      

            return redirect ("/view-company/")
    return render(request,"exportsTemplates/exportCompany.html",context)
@login_required(login_url='login')
@admin_only
def exportcompany(request):
      response = HttpResponse(content_type='text/csv')
      response['Content-Disposition'] = 'attachment; filename="CompanyData.csv"'
      writer = csv.writer(response)
      writer.writerow(['Company Name'])  
      writer.writerow(['company_name','contact_person','address','Phone','Email','Management'])     
      users = Company.objects.all().values_list('company_name','contact_person' , 'address' , 'phone','email','management')

      for user in users:
            writer.writerow(user)
      return response

######Edit Crew Planner start here
@login_required(login_url='login')
@admin_only
def editcrew(request ,pk):
    
    editcrew = CrewPlanner.objects.get(id = pk)
    form = CreateCrewForm( instance = editcrew )
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = request.POST.get("crew_company_name")
    success_message = ('%(notify_msg)s CrewPlanner updated successfully.') % {'notify_msg': notify_msg}
    if request.method =='POST':
         form = CreateCrewForm(request.POST, instance = editcrew)
         if form.is_valid():
              form.save()
              Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='updated',type='CREWPLANNER', status=False)
              messages.success(request,success_message)
              return redirect('/view-crewplanner')
    context ={'form':form,'notifycount':notifycount }
    return render(request,"edit/edit-crew.html",context)


##company start here
@login_required(login_url='login')
@admin_only
def crew(request):
    crew = CrewPlanner.objects.all()
    paginator = Paginator(crew, 10)
    page = request.GET.get('page',1)
    try:
       page_obj = paginator.page(page)
    except PageNotAnInteger:
       page_obj = paginator.page(1)
    except EmptyPage: 
       page_obj = paginator.page(paginator.num_pages) 
    notifycount = Notifications.objects.filter(status=False).count()
    context ={'page_obj':page_obj,'notifycount':notifycount}
    return render(request,"view/view-crew.html", context)
#company end here

#company start here
@login_required(login_url='login')
@admin_only
def addcrew(request):
    form = CreateCrewForm()
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = request.POST.get("crew_company_name")
    success_message = ('%(notify_msg)s CrewPlanner Created successfully.') % {'notify_msg': notify_msg}
    
    if request.method =='POST':
         form = CreateCrewForm(request.POST)
         if form.is_valid():
              obj = form.save(commit=False)
              obj.crew_created_by = request.user
              obj.save()
              Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='new',type='CREWPLANNER', status=False)
              messages.success(request,success_message)
              return redirect('/view-crewplanner') 
    context ={'form':form,'notifycount':notifycount}
           
    return render(request,"add/add-crewplanner.html", context)
#company end here
@login_required(login_url='login')
@admin_only
def deletecrew(request ,pk):
    delete = CrewPlanner.objects.get(id = pk)
    notifycount = Notifications.objects.filter(status=False).count()
    user = request.user 
    notify_msg = delete
    pre_url = request.META.get('HTTP_REFERER').split("/")[-1]
    page = request.POST.get('url')
    success_message = ('%(notify_msg)s Company Deleted successfully.') % {'notify_msg': notify_msg}
    if request.method == 'POST':
          delete.delete()
          Notifications.objects.create(notify_details = notify_msg , added_by_user=user ,alert='deleted',type='CREWPLANNER', status=False)
          messages.success(request, success_message)
          return redirect(page)

    context ={'delete':delete, 'notifycount':notifycount}
    return render(request,"delete/delete-crew.html",context)

# import using django import  
@login_required(login_url='login')
@admin_only  
def importcrew(request):
    notifycount = Notifications.objects.filter(status=False).count()
    context ={'notifycount':notifycount}
    if request.method == 'POST':
            #company = CompanyResource()
            file = request.FILES['files']
            ExcelFiles.objects.create(
                  file = file
            )
            path = file.file 
            empexceldata = pd.read_excel(path)
            dbframe = empexceldata
            #print(path)
            for dbframe in dbframe.itertuples():
                  obj = CrewPlanner.objects.create(   
                        crew_rank = dbframe.crew_rank,
                        crew_company_name = dbframe.crew_company_name,
                        crew_vessel = dbframe.crew_vessel,
                        crew_vsl_name = dbframe.crew_vsl_name,
                        crew_trading = dbframe.crew_trading,
                        crew_wages = dbframe.crew_wages,
                        crew_doj = dbframe.crew_doj,
                        crew_immediate = dbframe.crew_immediate,
                        crew_other_info = dbframe.crew_other_info,
                        crew_status = dbframe.crew_status,
                        )           
            obj.save()
            messages.success(request,"Crew Data uploaded")      
            return redirect ("/'view-crewplanner/")
    return render(request,"exportsTemplates/exportCrew.html",context)

@login_required(login_url='login')
@admin_only
def exportcrew(request):
      response = HttpResponse(content_type='text/csv')
      response['Content-Disposition'] = 'attachment; filename="CrewData.csv"'
      writer = csv.writer(response)
      writer.writerow(['Crew Name'])  
      writer.writerow(['crew_rank','crew_company_name','crew_vessel','crew_vsl_name','crew_trading','crew_wages','crew_doj','crew_immediate','crew_other_info','crew_status','crew_created_by','crew_updated_by'])     
      users = CrewPlanner.objects.all().values_list('crew_rank','crew_company_name','crew_vessel','crew_vsl_name','crew_trading','crew_wages','crew_doj','crew_immediate','crew_other_info','crew_status','crew_created_by','crew_updated_by')

      for user in users:
            writer.writerow(user)
      return response

####### AutoComplete Search Box ####################
@login_required(login_url='login')
@admin_only
def get_names(request):
      search = request.GET.get('search')
      payload= []
      if search:
         objs = Candidate.objects.filter(first_name__startswith = search)      
         for objs in objs:
               payload.append({
                     'name' :objs.first_name
               })
      return JsonResponse({
            'status': True,
            'payload': payload

      })

####### Notification Alert ####################
###########
@login_required(login_url='login')
@admin_only
def deleteallnotify(request):
      Notifications.objects.all().delete()
      #DocumentType.objects.all().delete()
      return redirect('/dashboard/')

@login_required(login_url='login')
@admin_only
def notification(request):
      notify = Notifications.objects.all().order_by('-id')
      context ={'notify':notify}
      return render(request,"notifications.html",context)

@login_required(login_url='login')
@admin_only
def getnotify(request):
      notify = Notifications.objects.filter(status = False).order_by('-id')
      #JsonData = serializers.serialize('json', notify)
      totalUnread= Notifications.objects.filter(status = False).count()
      JsonData =[]
      for d in notify:
            JsonData.append({
               'pk':d.id,
               #'date_created': d.date_created,
               'added_by_user': d.added_by_user,
               'notify_details':d.notify_details,
               'time' : d.date_created,
               'alert' : d.alert,
               'type' : d.type,
               'totalUnread':totalUnread
            })
      return JsonResponse({'data':JsonData,'totalUnread':totalUnread})
###############
@login_required(login_url='login')
@admin_only
def get_read_notify(request):
      notify = request.GET['notify']
      notify = Notifications.objects.get(pk=notify)
      user = request.user
      form = CreateNotificationForm( instance = notify )
      if request.method =='GET':
               form = CreateNotificationForm(request.GET, instance = notify)
               if form.is_valid():
                     referral = form.save(commit=False)
                     referral.ready_by_user = user
                     referral.status = True
                     referral.save()
      ReadNotification.objects.create(notify=notify,readuser=user,status=True)
      return JsonResponse({'bool':True})

@login_required(login_url='login')
@admin_only
def readllnotify(request):
    readnotify = Notifications.objects.all().order_by('-id')
    notifycount = Notifications.objects.filter(status=False).count()
    context ={'readnotify':readnotify, 'notifycount':notifycount}         
    return render(request,"notifications.html", context)



## Birthday 
@login_required(login_url='login')
@admin_only
def viewbirthday(request):
    #page_obj = Candidate.objects.all()
    currentdate = datetime.today()
    
    #2023-05-17
    formatDate = currentdate.strftime("%m-%d")
    checkDate = timezone.now() + timedelta(days=15)
    upcomingDate = checkDate.strftime("%m-%d")
    #crew = Candidate.objects.all()
    upcoming_birthdays = Candidate.objects.filter(birth_month__lte = upcomingDate, birth_month__gte =formatDate )
    paginator = Paginator(upcoming_birthdays, 10)
    page = request.GET.get('page',1)
    try:
       page_obj = paginator.page(page)
    except PageNotAnInteger:
       page_obj = paginator.page(1)
    except EmptyPage: 
       page_obj = paginator.page(paginator.num_pages) 
    notifycount = Notifications.objects.filter(status=False).count()
    context={
            'page_obj':page_obj,
            'date':formatDate,
            'check':upcomingDate,
            'notifycount':notifycount,
            'upcoming_birthdays':upcoming_birthdays,
            'formatDate':formatDate,
            'checkDate':checkDate
      }
    
    return render(request, 'view/view-birthday.html', context)
     

                   




                    
                    
            





