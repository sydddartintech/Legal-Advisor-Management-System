from django.shortcuts import render,redirect
from legal import models
from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings
import os
# Create your views here.
def advocate_dashboard(request):
    return render(request,"advocate_dashboard/advocate.html")

def change_password(request):
    return render(request,"advocate_dashboard/change_password.html")

def update_password(request):
    crnt_pass=request.POST['cpwd']
    new_pass=request.POST['npwd']
    con_pass=request.POST['copwd']

    uname=request.session.get('semail', None)

    if new_pass == con_pass:
        obj_login=models.Login.objects.get(username=uname)
        obj_login.password=new_pass
        obj_login.save()
        return render(request,"home/index.html")
    else:
        messages.success(request,'New and Confirm passwordare not same!!!!')

def adv_profile(request):
    adv_id = request.session.get('adv_id', None)
    # profile = models.Advocates.objects.get(email=uname)
    profile = models.Advocates.objects.raw("select * from advocates as a join case_category as c on a.case_cat_id=c.cat_id where adv_id=%s",[adv_id])
    milestone=models.AdvocateMilestone.objects.raw("select * from advocate_milestone where adv_id=%s",[adv_id])
    context = {
        'prof': profile[0],
        'mile_list':milestone
    }
    return render(request, "advocate_dashboard/profile.html", context)

def ongoing_case_client(request):
    adv_id = request.session.get('adv_id', None)
    case=models.CaseDetails.objects.raw("select * from case_details inner join case_category on case_details.case_cat_id=case_category.cat_id where case_details.advocate_id=%s and case_details.status='Progressing'",[adv_id])
    context={
    'case_list':case
    }
    return render(request,"advocate_dashboard/ongoing_case.html",context) 

def schedule_details_client(request,cno):
    sh_list=models.CaseSchedules.objects.filter(case_id=cno)
    context={
    'sch_list':sh_list
    }
    # return HttpResponse(case_no)
    return render(request,"advocate_dashboard/case_schedule.html",context)

def case_details(request,cno):
    case=models.CaseDetails.objects.get(case_no=cno)
    case_no=case.case_no
    case_details=models.CaseDetails.objects.raw("select * from case_details as cd join case_category as c on cd.case_cat_id=c.cat_id where cd.case_no=%s",[case_no])
    clients=models.Clients.objects.raw("select * from clients as c join case_details as cd on c.client_id=cd.clientid where cd.case_no=%s",[case_no])
    context={
    'case_list':case_details[0],
    'client_list':clients[0]
    }
    return render(request,"advocate_dashboard/case_details_viewmore.html",context)

def case_history_view(request,cno):
    case=models.CaseDetails.objects.get(case_no=cno)
    case_no=case.case_no
    history=models.CaseHistory.objects.raw("select * from case_history where case_no=%s",[case_no])
    context={
    'case_list':case,
    'case_no':case_no,
    'history_list':history
    }
    return render(request,"case_history/case_history_view.html",context)

def case_history_add(request,cno):
    case=models.CaseDetails.objects.get(case_no=cno)
    case_no=case.case_no
    context={
    'case_no':case_no
    }
    return render(request,"case_history/add_case_history.html",context)

def save_history(request):
    title=request.POST['title']
    description=request.POST['desc']
    caseno=request.POST['cno']
    posted_date = timezone.now().date()
    obj_history=models.CaseHistory(title=title,description=description,case_no=caseno,date=posted_date)
    obj_history.save()
    return  redirect('case_history_view',cno=caseno)

def edit_case_history(request,hid):
    history=models.CaseHistory.objects.get(history_id=hid)
    context={
    'history_list':history
    }
    return render(request,"case_history/edit_history.html",context)

def update_history(request): 
    hist_id=request.POST['hno']
    title=request.POST['title'] 
    description=request.POST['desc'] 
    case_no=request.POST['cno'] 
    
    obj_history=models.CaseHistory.objects.get(history_id=hist_id)
    obj_history.title=title
    obj_history.description=description

    obj_history.save()
    messages.success(request,'updated successfully!!!!')
    return redirect('case_history_view',cno=case_no)

def delete_history(request,hid):
    history=models.CaseHistory.objects.get(history_id=hid)
    case_no=history.case_no
    history.delete()
    messages.success(request,'Deleted successfully!!!!')
    return redirect('case_history_view',cno=case_no)

def case_documents_view(request,cno):
    uname = request.session.get('semail', None)
    case=models.CaseDetails.objects.get(case_no=cno)
    case_no=case.case_no
    docs=models.CaseDocuments.objects.raw("select * from case_documents where case_id=%s",[case_no])
    context={
    'case_list':case,
    'case_no':case_no,
    'doc_list':docs,
    'user':uname
    }
    return render(request,"advocate_dashboard/document_view.html",context)

def case_doc_add(request,cno):
    case=models.CaseDetails.objects.get(case_no=cno)
    case_no=case.case_no
    context={
    'case_no':case_no
    }
    return render(request,"advocate_dashboard/add_case_doc.html",context)

def save_doc(request):
    if request.method == 'POST':
        uploaded_by = request.session.get('semail',None)
        doc_name = request.POST.get('docname')
        doc_desc = request.POST.get('docdesc')
        case_no = request.POST.get('caseno')
        uploaded_date = timezone.now().date()

        if 'docfile' in request.FILES:

            document = request.FILES['docfile']
            doc_path = os.path.join(settings.MEDIA_ROOT, 'documents', document.name)

            with open(doc_path, 'wb') as file:
                for chunk in document.chunks():
                    file.write(chunk)

            obj_client = models.CaseDocuments(doc_title=doc_name,doc_desc=doc_desc,doc_file=os.path.join(document.name),doc_uploaded_date=uploaded_date,case_id=case_no,uploaded_by=uploaded_by)
            obj_client.save()

            messages.success(request, 'Saved successfully!!!')
        
    else:
        messages.error(request, 'Invalid request method')

    return redirect('case_documents_view',cno=case_no)

def change_document(request,doid):
    docs=models.CaseDocuments.objects.get(doc_id=doid)
    context={
    "dlist":docs
    }
    return render(request,"advocate_dashboard/change_document.html",context)

def update_document(request):
    try:
        doc_id = request.POST.get('docid')
        case_id = request.POST.get('cno')
        docs = models.CaseDocuments.objects.get(doc_id=doc_id)

        if 'docfile' in request.FILES:
            document = request.FILES['docfile']
            doc_path = os.path.join(settings.MEDIA_ROOT, 'documents', document.name)

            with open(doc_path, 'wb') as file:
                for chunk in document.chunks():
                    file.write(chunk)

            # Update client photo and save
            
            docs.doc_file = os.path.join(document.name)  # Corrected path

            docs.save()

            messages.success(request, 'Updated successfully!')
        else:
            messages.error(request, 'No photo file provided.')

    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')

    return redirect('case_documents_view',cno=case_id)

def edit_document(request,doid):
    docs=models.CaseDocuments.objects.get(doc_id=doid)
    context={
    "dlist":docs
    }
    return render(request,"advocate_dashboard/edit_document.html",context)

def update_doc_details(request): 
    doc_id=request.POST['doid']
    title=request.POST['docname'] 
    description=request.POST['docdesc'] 
    case_no=request.POST['cno'] 
    
    obj_doc=models.CaseDocuments.objects.get(doc_id=doc_id)
    obj_doc.doc_title=title
    obj_doc.doc_desc=description

    obj_doc.save()
    messages.success(request,'updated successfully!!!!')
    return redirect('case_documents_view',cno=case_no)

def delete_document(request,doid):
    docs=models.CaseDocuments.objects.get(doc_id=doid)
    case_no=docs.case_id
    docs.delete()
    messages.success(request,'Deleted successfully!!!!')
    return redirect('case_documents_view',cno=case_no)

def closed_case(request):
    adv_id = request.session.get('adv_id', None)
    case=models.CaseDetails.objects.raw("select * from case_details inner join case_category on case_details.case_cat_id=case_category.cat_id where case_details.advocate_id=%s and case_details.status='Closed'",[adv_id])
    context={
    'case_list':case
    }
    return render(request,"advocate_dashboard/closed_case.html",context) 

def message_panel(request):
    msgs=models.MessagePanel.objects.raw("select * from message_panel where parent_id IS NULL")
    context={
    'msg_list':msgs
    }
    return render(request,"advocate_dashboard/view_message.html",context)

def message_rply(request,msgid):
    uname=request.session.get('semail', None)
    msgs=models.MessagePanel.objects.get(message_id=msgid)
    msg_rply=models.MessagePanel.objects.raw("select * from message_panel where parent_id=%s",[msgid])
    advs=models.Advocates.objects.get(email=uname)
    context={
    'msg_list':msgs,
    'adv_list':advs,
    'rply':msg_rply
    }
    # return HttpResponse(pid)
    return render(request,"advocate_dashboard/view_message_rply.html",context)
def save_rply(request):
    parent_id=request.POST['messageid']
    message=request.POST['reply']
    posted_by=request.session.get('semail', None)
    posted_date=timezone.now().date()
    msg_id=request.POST['fmessageid']
    obj_msg=models.MessagePanel(message=message,posted_by=posted_by,post_date=posted_date,parent_id=parent_id)
    obj_msg.save()
    return  redirect('message_rply',msgid=msg_id)