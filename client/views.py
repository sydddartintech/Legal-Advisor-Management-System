from django.shortcuts import render,redirect
from legal import models
from django.utils import timezone
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
import os
# Create your views here.
def client_dashboard(request):
    return render(request,"client_dashboard/client.html")

def my_profile(request):
    client_id = request.session.get('client_id', None)
    # profile = models.Advocates.objects.get(email=uname)
    profile = models.Clients.objects.raw("select * from clients as c join case_details as cd on c.client_id=cd.clientid where client_id=%s",[client_id])
    
    context = {
        'prof': profile[0]
    }
    return render(request, "client_dashboard/profile.html", context)

def ongoing_case(request):
    client_id = request.session.get('client_id', None)
    case=models.CaseDetails.objects.raw("select * from case_details inner join case_category on case_details.case_cat_id=case_category.cat_id where case_details.clientid=%s and case_details.status='Progressing'",[client_id])
    context={
    'case_list':case
    }
    return render(request,"client_dashboard/ongoing_case.html",context) 

def schedule_details(request,cno):
    sh_list=models.CaseSchedules.objects.filter(case_id=cno)
    context={
    'sch_list':sh_list
    }
    # return HttpResponse(case_no)
    return render(request,"client_dashboard/case_schedule.html",context)

def case_details_client(request,cno):
    case=models.CaseDetails.objects.get(case_no=cno)
    case_no=case.case_no
    case_details=models.CaseDetails.objects.raw("select * from case_details as cd join case_category as c on cd.case_cat_id=c.cat_id where cd.case_no=%s",[case_no])
    clients=models.Clients.objects.raw("select * from clients as c join case_details as cd on c.client_id=cd.clientid where cd.case_no=%s",[case_no])
    context={
    'case_list':case_details[0],
    'client_list':clients[0]
    }
    return render(request,"client_dashboard/case_details_viewmore.html",context)

def case_history_view_client(request,cno):
    case=models.CaseDetails.objects.get(case_no=cno)
    case_no=case.case_no
    history=models.CaseHistory.objects.raw("select * from case_history where case_no=%s",[case_no])
    context={
    'case_list':case,
    'case_no':case_no,
    'history_list':history
    }
    return render(request,"client_dashboard/case_history_view.html",context)

def case_documents_view_client(request,cno):
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
    return render(request,"client_dashboard/document_view.html",context)

def case_doc_add_client(request,cno):
    case=models.CaseDetails.objects.get(case_no=cno)
    case_no=case.case_no
    context={
    'case_no':case_no
    }
    return render(request,"client_dashboard/add_case_doc.html",context)

def save_doc_client(request):
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

    return redirect('case_documents_view_client',cno=case_no)

def change_document_client(request,doid):
    docs=models.CaseDocuments.objects.get(doc_id=doid)
    context={
    "dlist":docs
    }
    return render(request,"client_dashboard/change_document.html",context)

def update_document_client(request):
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

    return redirect('case_documents_view_client',cno=case_id)

def edit_document_client(request,doid):
    docs=models.CaseDocuments.objects.get(doc_id=doid)
    context={
    "dlist":docs
    }
    return render(request,"client_dashboard/edit_document.html",context)

def update_doc_details_client(request): 
    doc_id=request.POST['doid']
    title=request.POST['docname'] 
    description=request.POST['docdesc'] 
    case_no=request.POST['cno'] 
    
    obj_doc=models.CaseDocuments.objects.get(doc_id=doc_id)
    obj_doc.doc_title=title
    obj_doc.doc_desc=description

    obj_doc.save()
    messages.success(request,'updated successfully!!!!')
    return redirect('case_documents_view_client',cno=case_no)

def delete_document_client(request,doid):
    docs=models.CaseDocuments.objects.get(doc_id=doid)
    case_no=docs.case_id
    docs.delete()
    messages.success(request,'Deleted successfully!!!!')
    return redirect('case_documents_view_client',cno=case_no)

def closed_case_client(request):
    client_id = request.session.get('client_id', None)
    case=models.CaseDetails.objects.raw("select * from case_details inner join case_category on case_details.case_cat_id=case_category.cat_id where case_details.clientid=%s and case_details.status='Closed'",[client_id])
    context={
    'case_list':case
    }
    return render(request,"client_dashboard/closed_case.html",context) 

def adv_details(request,cno):
    cas_list=models.CaseDetails.objects.get(case_no=cno)
    adv_id=cas_list.advocate_id
    advocates=models.Advocates.objects.raw("select * from advocates inner join case_category on advocates.case_cat_id=case_category.cat_id where advocates.adv_id=%s",[adv_id])
    adv_milestone=models.AdvocateMilestone.objects.raw("select * from advocate_milestone where adv_id=%s",[adv_id])
    context={
    'adv_list':advocates[0],
    'mile_list':adv_milestone
    }
    return render(request,"client_dashboard/view_advocate_details.html",context)

def transactions(request):
    user = request.session.get('semail', None)
    trans_details=models.ClientTransaction.objects.filter(fk_client_email=user)
    context={
    'transactions':trans_details
    }
    return render(request,"client_dashboard/my_transactions.html",context)

def client_payment(request):
    return render(request,"client_dashboard/create_payment.html")

def client_transaction(request):
    user = request.session.get('semail', None)
    clients = models.Clients.objects.filter(email_id=user)

    # Check if clients is not empty before proceeding
    if clients.exists():
        cardname = request.POST["cardname"]
        cardNumber = request.POST["cardNumber"]
        expdate = request.POST["expdate"]
        cvv = request.POST["cvv"]
        totalamount = float(request.POST["amount"])  # Convert amount to float
        remark = request.POST['remarks']

        # Use get() instead of raw SQL query to retrieve bank_data
        try:
            bank_data = models.Bank.objects.get(card_number=cardNumber, expiry=expdate, cvv=cvv)
        except models.Bank.DoesNotExist:
            messages.error(request, 'Invalid Card')
            return redirect("transactions")

        if totalamount <= bank_data.amount:
            fk_client_email = user
            transfer_date = timezone.now().date()
            pay_amount = totalamount
            remarks = remark
            payment = models.ClientTransaction(fk_client_email=fk_client_email, trans_date=transfer_date,
                                              amount=pay_amount, remarks=remarks)
            payment.save()
            messages.success(request, 'Payment successfully completed')
        else:
            messages.error(request, 'Insufficient Fund')
    else:
        messages.error(request, 'Invalid Client')

    return redirect("transactions")

def change_password(request):
    return render(request,"client_dashboard/change_password.html")

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
    