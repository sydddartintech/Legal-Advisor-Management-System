from django.shortcuts import render,redirect
from django.contrib import admin
from legal import models
from django.http import HttpResponse
from django.contrib import admin
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
from django.conf import settings
import os
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def admin_dashboard(request):
    return render(request,"admin/admin.html")

def change_pass(request):
    return render(request,"admin/change_password.html")

def update_pass(request):
    crnt_pass=request.POST['cpwd']
    new_pass=request.POST['npwd']
    con_pass=request.POST['copwd']

    uname=request.session.get('username', None)
    
    if new_pass == con_pass:
        obj_login=models.Login.objects.filter(username=uname)
        obj_login.update(password=new_pass)
        return render(request,"home/index.html")
    else:
        messages.success(request,'New and Confirm passwordare not same!!!!')

def add_categ(request):
    return render(request,"category/category_add.html")
def save_category(request):
    cname = request.POST['category']

    # Check if the category already exists
    existing_category = models.CaseCategory.objects.filter(cat_name=cname).first()

    if existing_category:
        # Category already exists, handle this case (e.g., show an error message)
        # return HttpResponse("Category already exists!")
        messages.success(request,'Category already exists!!!!!')
        return redirect('show_category')

    # If the category does not exist, save it
    obj_categ = models.CaseCategory(cat_name=cname)
    obj_categ.save()

    return redirect('show_category')

def show_category(request):
	category=models.CaseCategory.objects.all()
	context={
	"categ_list":category
	}
	return render(request,"category/show_category.html",context)

def edit_category(request,cid):
     categ_list=models.CaseCategory.objects.get(cat_id =cid)
     context= {
     "category":categ_list
      }
     return render(request,"category/edit_categ.html",context)

def update_category(request): 
    categ_id=request.POST['categ_id']
    categ_name=request.POST['category'] 
    existing_category = models.CaseCategory.objects.filter(cat_name=categ_name).first()
    if existing_category:
        # Category already exists, handle this case (e.g., show an error message)
        # return HttpResponse("Category already exists!")
        messages.success(request,'Category already exists!!!!!')
        return redirect('show_category')
    
    obj_categ=models.CaseCategory.objects.get(cat_id=categ_id)
    obj_categ.cat_name=categ_name
    
    
    obj_categ.save()
    messages.success(request,'updated successfully!!!!')
    return redirect('show_category')

def delete_category(request,cid):
    categ=models.CaseCategory.objects.get(cat_id=cid)
    
    # case_count = models.CaseDetails.objects.filter(case_cat_id=cid).count()

    adv_count = models.Advocates.objects.filter(case_cat_id=cid).count()

    if adv_count == 0:
        # No associated schedules, delete CaseDetails
        categ.delete()
        messages.success(request, 'Deleted successfully!!!!')
        return redirect('show_category')
    else:
        # Display a message indicating that there are associated schedules
        messages.warning(request, 'Cannot delete CaseDetails. Associated schedules exist.')
    
    return redirect('show_category')


def add_advocates(request):
	category=models.CaseCategory.objects.all()
	context={
	"categ_list":category
	}
	return render(request,"advocates/add_advocates.html",context)

def save_advocate(request):

    adv_fname = request.POST['fname']
    adv_lname = request.POST['lname']
    adv_address = request.POST['address']
    adv_gender = request.POST['gender']
    adv_phno = request.POST['pno']
    adv_expe = request.POST['experience']
    adv_categ = request.POST['cat']
    adv_email = request.POST['Email']
    password = request.POST['password']
    user_type='advocate'
    status='active'
    
    if request.method == 'POST' and request.FILES['Photo']:
        picture = request.FILES['Photo']
        fss = FileSystemStorage()
        file = fss.save(f'advocates/{picture.name}', picture)
        log_info = models.Login.objects.filter(username=adv_email)
        obj_adv = models.Advocates(first_name =adv_fname,last_name=adv_lname,address=adv_address,phone=adv_phno,gender=adv_gender,experience=adv_expe,case_cat_id=adv_categ,email=adv_email,photo=file)
        if len(log_info)==0:
            obj_adv.save()
            obj_log=models.Login(username=adv_email,password=password,user_type=user_type,status=status)
            obj_log.save()
        else:
            messages.success(request,'Email id already exists.. Try another one!!')   
            return redirect('show_advocates')
        

        messages.success(request, 'Saved successfully!!!')
    else:
        messages.error(request, 'Please select a file')

    return redirect('show_advocates')

def show_advocates(request):
	adv_list=models.CaseCategory.objects.raw("select * from case_category c join advocates e on c.cat_id =e.case_cat_id")
	context={
	"advocate_list":adv_list
	}
	return render(request,"advocates/list_advocates.html",context)

def edit_advocates(request,ad_id):
     adv_list=models.Advocates.objects.get(adv_id=ad_id)
     category=models.CaseCategory.objects.all()
     context= {
     "advocates":adv_list,
     "categ_list":category
      }
     return render(request,"advocates/edit_advocate.html",context)

def update_advocates(request): 
    advid=request.POST['adv_id']
    adv_fname=request.POST['fname'] 
    adv_lname=request.POST['lname']
    adv_address=request.POST['address']
    adv_gender=request.POST['gender']
    adv_mob=request.POST['pno']
    adv_exp=request.POST['experience']
    adv_categ=request.POST['cat']
    
    
    obj_adv=models.Advocates.objects.get(adv_id=advid)
    obj_adv.first_name=adv_fname
    obj_adv.last_name=adv_lname
    obj_adv.address=adv_address
    obj_adv.phone=adv_mob
    obj_adv.gender=adv_gender
    obj_adv.experience=adv_exp
    obj_adv.case_cat_id=adv_categ
    
    
    obj_adv.save()
    messages.success(request,'updated successfully!!!!')
    return redirect('show_advocates')

def delete_adv(request,aid):
    # Get the CaseDetails object
    advs = models.Advocates.objects.get(adv_id=aid)
    
    # Get the client_id from CaseDetails
    advo_id = advs.adv_id
    
    # Check if there are any associated CaseSchedules
    details_count = models.CaseDetails.objects.filter(advocate_id=advo_id).count()

    if details_count == 0:
        # No associated schedules, delete CaseDetails
        advs.delete()
        messages.success(request, 'Deleted successfully!!!!')
    else:
        # Display a message indicating that there are associated schedules
        messages.warning(request, 'Cannot delete Advocate. Associated Case Details exist.')

    return redirect('show_advocates')

def change_adv_image(request,aid):
    advocates=models.Advocates.objects.get(adv_id=aid)
    context={
    "adv_list":advocates
    }
    return render(request,"advocates/change_image.html",context)

def update_adv_image(request):
    try:
        adv_id = request.POST['aid']
        client = models.Advocates.objects.get(adv_id=adv_id)

        if 'Photo' in request.FILES:
            picture = request.FILES['Photo']
            fss = FileSystemStorage()

            # Generate a unique file name
            file_name = f'advocates/{picture.name}'  # Fix the tuple issue here
            file_path = fss.save(file_name, picture)

            
            client.photo = file_path
            client.save()

            messages.success(request, 'Updated successfully!')
        else:
            messages.error(request, 'No photo file provided.')

    except ObjectDoesNotExist:
        messages.error(request, 'Client not found.')

    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')

    return redirect('show_advocates')

def add_milestone(request,ad_id):
    adv_list=models.Advocates.objects.get(adv_id=ad_id)
    adv_id=adv_list.adv_id
    context={
    "advocate_list":adv_list,
    "advid":adv_id
    }
    return render(request,"advocates/adv_milestone.html",context)

def show_milestone(request,ad_id):
    adv_list=models.Advocates.objects.get(adv_id=ad_id)
    adv_id=adv_list.adv_id
    mile_list=models.AdvocateMilestone.objects.raw("select * from advocate_milestone where adv_id=%s",[adv_id])
    
    context={
    "milestone_list":mile_list,
    "advocate":adv_list,
    "advid":adv_id
    }
    return render(request,"advocates/milestone_list.html",context)

def save_milestone(request):
    title=request.POST['title']
    description=request.POST['desc']
    adv_id=request.POST['adv_id']
    posted_date = timezone.now().date()

    obj_milestone=models.AdvocateMilestone(adv_id=adv_id,title=title,description=description,posted_date=posted_date)
    obj_milestone.save()
      
    return redirect('show_milestone',ad_id=adv_id)

def edit_milestone(request,mid):
     milestone_list=models.AdvocateMilestone.objects.get(adv_ms_id =mid)
     advid=milestone_list.adv_id
     ad_list=models.Advocates.objects.get(adv_id=advid)
     context= {
     "milestone":milestone_list,
     "advocates":ad_list
      }
     return render(request,"advocates/edit_milestone.html",context)

def update_milestone(request): 
    milestone_id=request.POST['admid']
    adv_id=request.POST['advid']
    mtitle=request.POST['title'] 
    mdesc=request.POST['desc'] 
    posted_date = timezone.now().date()
    
    obj_milestone=models.AdvocateMilestone.objects.get(adv_ms_id=milestone_id)
    obj_milestone.title=mtitle
    obj_milestone.description=mdesc
    obj_milestone.posted_date=posted_date
    
    obj_milestone.save()
    messages.success(request,'updated successfully!!!!')
    return redirect('show_milestone',ad_id=adv_id)

def delete_milestone(request,mid):
    milestone=models.AdvocateMilestone.objects.get(adv_ms_id=mid)
    advid=milestone.adv_id
    milestone.delete()
    messages.success(request,'Deleted successfully!!!!')
    return redirect('show_milestone',ad_id=advid)


def add_client(request):
    return render(request,"client/client_add.html")

def save_client(request):
    if request.method == 'POST':
        cl_fname = request.POST.get('fname')
        cl_lname = request.POST.get('lname')
        cl_address = request.POST.get('address')
        cl_dob = request.POST.get('dob')
        cl_gender = request.POST.get('gender')
        cl_phno = request.POST.get('pno')
        cl_email = request.POST.get('Email')
        cl_state = request.POST.get('state')
        cl_district = request.POST.get('district')
        cl_location = request.POST.get('location')
        cl_pin = request.POST.get('pincode')
        cl_aadhar = request.POST.get('aadhaarno')
        cl_idtype = request.POST.get('idtype')
        password = request.POST.get('password')
        user_type = 'client'
        status = 'active'

        if 'Photo' in request.FILES and 'idproof' in request.FILES:
            picture = request.FILES['Photo']
            fss = FileSystemStorage()
            file_path = fss.save(f'client/{picture.name}', picture)

            id_proof = request.FILES['idproof']
            id_proof_path = os.path.join(settings.MEDIA_ROOT, 'proof', id_proof.name)

            with open(id_proof_path, 'wb') as file:
                for chunk in id_proof.chunks():
                    file.write(chunk)
          
            obj_client = models.Clients(
                first_name=cl_fname, last_name=cl_lname, address=cl_address,
                gender=cl_gender, dob=cl_dob, state=cl_state, district=cl_district,
                location=cl_location, pin=cl_pin, mobile=cl_phno, email_id=cl_email,
                aadhaar_no=cl_aadhar, photo=file_path, identity_type=cl_idtype,
                identity_file=os.path.join(id_proof.name)
            )
            log_info = models.Login.objects.filter(username=cl_email)
            if len(log_info)==0:
                obj_client.save()
                obj_log = models.Login(username=cl_email, password=password, user_type=user_type, status=status)
                obj_log.save()
            else:
                messages.success(request,'Email id already exists.. Try another one!!')   
                return redirect('add_client')

            

            messages.success(request, 'Saved successfully!!!')
        
    else:
        messages.error(request, 'Invalid request method')

    return redirect('show_client')

def show_client(request):
    clients=models.Clients.objects.all()
    context={
    "client_list":clients
    }
    return render(request,"client/client_list.html",context)

def change_image(request,clid):
    clients=models.Clients.objects.get(client_id=clid)
    context={
    "clist":clients
    }
    return render(request,"client/change_image.html",context)

def update_image(request):
    try:
        client_id = request.POST['clid']
        client = models.Clients.objects.get(client_id=client_id)

        if 'Photo' in request.FILES:
            picture = request.FILES['Photo']
            fss = FileSystemStorage()

            # Generate a unique file name
            file_name = f'client/{picture.name}'  # Fix the tuple issue here
            file_path = fss.save(file_name, picture)

            # Update client photo and save
            client.photo = file_path
            client.save()

            messages.success(request, 'Updated successfully!')
        else:
            messages.error(request, 'No photo file provided.')

    except ObjectDoesNotExist:
        messages.error(request, 'Client not found.')

    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')

    return redirect('show_client')

def change_idproof(request,clid):
    clients=models.Clients.objects.get(client_id=clid)
    context={
    "clist":clients
    }
    return render(request,"client/change_idproof.html",context)

def update_proof(request):
    try:
        client_id = request.POST.get('clid')
        cl_filetype = request.POST['idtype']
        client = models.Clients.objects.get(client_id=client_id)

        if 'idproof' in request.FILES:
            id_proof = request.FILES['idproof']
            
            id_proof_path = os.path.join(settings.MEDIA_ROOT, 'proof', id_proof.name)

            with open(id_proof_path, 'wb') as file:
                for chunk in id_proof.chunks():
                    file.write(chunk)

            # Update client photo and save
            client.identity_type = cl_filetype
            client.identity_file = os.path.join(id_proof.name)  # Corrected path

            client.save()

            messages.success(request, 'Updated successfully!')
        else:
            messages.error(request, 'No photo file provided.')

    except ObjectDoesNotExist:
        messages.error(request, 'Client not found.')

    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')

    return redirect('show_client')

def client_details(request,clid):
    client = models.Clients.objects.get(client_id=clid)
    context={
    "cl_li":client
    }
    return render(request,"client/view_client_details.html",context)

def client_edit(request,clid):
    client = models.Clients.objects.get(client_id=clid)
    context={
    "cl_li":client
    }
    return render(request,"client/client_edit.html",context)

def update_client(request): 
    client_id=request.POST['cl_id']
    cl_fname=request.POST['fname']
    cl_lname=request.POST['lname'] 
    cl_addr=request.POST['address'] 
    cl_dob=request.POST['dob'] 
    cl_gender=request.POST['gender'] 
    cl_phno=request.POST['pno'] 
    cl_state=request.POST['state'] 
    cl_dist=request.POST['district'] 
    cl_loc=request.POST['location'] 
    cl_pin=request.POST['pincode'] 
    cl_aano=request.POST['aadhaarno'] 

    obj_client=models.Clients.objects.get(client_id=client_id)
    obj_client.first_name=cl_fname
    obj_client.last_name=cl_lname
    obj_client.address=cl_addr
    obj_client.gender=cl_gender
    obj_client.dob=cl_dob
    obj_client.state=cl_state
    obj_client.district=cl_dist
    obj_client.location=cl_loc
    obj_client.pin=cl_pin
    obj_client.mobile=cl_phno
    obj_client.aadhaar_no=cl_aano
    
    obj_client.save()
    messages.success(request,'updated successfully!!!!')
    return redirect('client_details',clid=client_id)

def delete_client(request,clid):
    # Get the CaseDetails object
    clients = models.Clients.objects.get(client_id=clid)
    
    # Get the client_id from CaseDetails
    client_id = clients.client_id
    
    # Check if there are any associated CaseSchedules
    details_count = models.CaseDetails.objects.filter(clientid=client_id).count()

    if details_count == 0:
        # No associated schedules, delete CaseDetails
        clients.delete()
        messages.success(request, 'Deleted successfully!!!!')
    else:
        # Display a message indicating that there are associated schedules
        messages.warning(request, 'Cannot delete Clients. Associated Case Details exist.')

    return redirect('show_client')

def show_case_details(request,clid):
    clients=models.Clients.objects.get(client_id=clid)
    clid=clients.client_id
    case_details=models.CaseDetails.objects.raw("select * from case_details  join advocates on case_details.advocate_id=advocates.adv_id inner join case_category on case_details.case_cat_id=case_category.cat_id where case_details.clientid=%s",[clid])
    context={
    "client_list":clients,
    "clid":clid,
    "case_list":case_details
    }
    return render(request,"case_details/case_list.html",context)

def add_case_details(request,clid):
    categ_list=models.CaseCategory.objects.all()
    adv_list=models.Advocates.objects.all()
    clients=models.Clients.objects.get(client_id=clid)
    cl_id=clients.client_id
    context={
    "cat_list":categ_list,
    "ad_li":adv_list,
    "clid":cl_id
    }
    return render(request,"case_details/case_details_add.html",context)
@csrf_exempt
def get_advocate(request):
    cat_id = request.GET['catid']
    advocates = models.Advocates.objects.raw("SELECT * FROM advocates WHERE case_cat_id=%s", [cat_id])

    options_html = ""  # Initialize the variable

    for adv in advocates:
        options_html += f'<option value="{adv.adv_id}">{adv.first_name}</option>'

    context = {'adv_list': advocates, 'options_html': options_html}

    # Depending on your use case, you might return a JsonResponse or render a template with this context
    return JsonResponse({'options_html': options_html})

def save_case_details(request):
    case_categ=request.POST['cat']
    case_desc=request.POST['desc']
    case_rd=request.POST['regdate']
    case_sd=request.POST['stdate']
    case_adv=request.POST['adv']
    case_rem=request.POST['remarks']
    case_status=request.POST['status']
    client_id=request.POST['cli_id']

    obj_casedetails=models.CaseDetails(case_cat_id=case_categ,description=case_desc,case_register_date=case_rd,case_start_date=case_sd,remark=case_rem,status=case_status,clientid=client_id,advocate_id=case_adv)
    obj_casedetails.save()
      
    return redirect('show_case_details',clid=client_id)

def view_case_documents(request,cno):
    case_details=models.CaseDetails.objects.get(case_no=cno)
    case_no=case_details.case_no
    client_id=case_details.clientid
    documents=models.CaseDocuments.objects.raw("select * from case_documents where case_id=%s",[cno])
    context={
    "doc_list":documents,
    "clientid":client_id,
    'cno':case_no
    }

    return render(request,"case_details/view_documents.html",context)

def view_case_history(request,cno):
    case_details=models.CaseDetails.objects.get(case_no=cno)
    case_no=case_details.case_no
    client_id=case_details.clientid
    history=models.CaseHistory.objects.raw("select * from case_history where case_no=%s",[cno])
    context={
    "hist_list":history,
    "clientid":client_id,
    'cno':case_no
    }

    return render(request,"case_details/view_history.html",context)

def edit_case_details(request,cno):
    case_details=models.CaseDetails.objects.get(case_no=cno)
    category=models.CaseCategory.objects.all()
    context={
    "case_list":case_details,
    "cat_list":category
    }

    return render(request,"case_details/case_details_edit.html",context)

def update_case_details(request): 
    client_id=request.POST['clid']
    case_id=request.POST['cno']
    case_desc=request.POST['desc']
    reg_date=request.POST['regdate']
    sta_date=request.POST['stdate'] 
    remarks=request.POST['remarks'] 
    status=request.POST['status'] 
    
    obj_details=models.CaseDetails.objects.get(case_no=case_id)
    obj_details.description=case_desc
    obj_details.case_register_date=reg_date
    obj_details.case_start_date=sta_date
    obj_details.remark=remarks
    obj_details.status=status
    
    obj_details.save()
    messages.success(request,'updated successfully!!!!')
    return redirect('show_case_details',clid=client_id)

def delete_case_details(request, cno):
    # Get the CaseDetails object
    details = models.CaseDetails.objects.get(case_no=cno)
    
    # Get the client_id from CaseDetails
    client_id = details.clientid
    
    # Check if there are any associated CaseSchedules
    schedule_count = models.CaseSchedules.objects.filter(case_id=details.case_no).count()

    if schedule_count == 0:
        # No associated schedules, delete CaseDetails
        details.delete()
        messages.success(request, 'Deleted successfully!!!!')
    else:
        # Display a message indicating that there are associated schedules
        messages.warning(request, 'Cannot delete CaseDetails. Associated schedules exist.')

    return redirect('show_case_details', clid=client_id)

def view_case_schedule(request,cno):
    case_details=models.CaseDetails.objects.get(case_no=cno)
    case_num=case_details.case_no
    case_schedule=models.CaseSchedules.objects.raw("select * from case_schedules where case_id=%s",[case_num])
    context={
    "ca_list":case_details,
    "case_no":case_num,
    "sh_list":case_schedule
    }
    return render(request,"schedule/schedule_list.html",context)

def add_case_schedule(request,cno):
    case_details=models.CaseDetails.objects.get(case_no=cno)
    case_num=case_details.case_no
    clid=case_details.cliebtid
    context={
    "ca_list":case_details,
    "case_no":case_num,
    "cid":clid
    }
    return render(request,"schedule/add_schedule.html",context)

def save_case_schedule(request):
    sh_date=request.POST['sdate']
    sh_remarks=request.POST['remarks']
    case_no=request.POST['cno']
    
    obj_schedule=models.CaseSchedules(sh_date=sh_date,case_id=case_no,remark=sh_remarks)
    obj_schedule.save()
      
    return redirect('view_case_schedule',cno=case_no)

def edit_case_schedule(request,sid):
    sh_details=models.CaseSchedules.objects.get(schedule_id=sid)
    context={
    "sh_list":sh_details

    }
    return render(request,"schedule/edit_schedule.html",context)

def update_case_schedule(request): 
    schedule_id=request.POST['sid']
    sh_date=request.POST['sdate']
    sh_remark=request.POST['remarks'] 
    case_no=request.POST['cno']
    
    obj_schedule=models.CaseSchedules.objects.get(schedule_id=schedule_id)
    obj_schedule.sh_date=sh_date
    obj_schedule.remark=sh_remark
    
    
    obj_schedule.save()
    messages.success(request,'updated successfully!!!!')
    return redirect('view_case_schedule',cno=case_no)

def delete_schedule(request,sid):
    schedule=models.CaseSchedules.objects.get(schedule_id=sid)
    case_num=schedule.case_id
    schedule.delete()
    messages.success(request,'Deleted successfully!!!!')
    return redirect('view_case_schedule',cno=case_num)

def enquiry_list(request):
    enquiry=models.Enquiry.objects.all()
    context={
    "enq_list":enquiry
    }
    return render(request,"enquiry/enquiry_list.html",context)

def enquiry_details(request,eid):
    enquiry=models.Enquiry.objects.get(enq_id=eid)
    context={
    "eq_list":enquiry
    }
    return render(request,"enquiry/enquiry_details.html",context)

def trans_details(request):
    trans_details=models.ClientTransaction.objects.raw("SELECT * FROM client_transaction ct inner join clients c ON ct.fk_client_email=c.email_id")
    context={
    'transactions':trans_details
    }
    return render(request,"admin/transactions.html",context)
def profile(request):
    return render(request,"advocate_dashboard/profile.html")
