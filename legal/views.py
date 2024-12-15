from django.shortcuts import render,redirect
from django.contrib.sessions.models import Session
from django.contrib import messages
from legal import models
import random
from legal.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.utils import timezone
def home(request):
  return render(request,"home/index.html")
def about(request):
    return render(request,"home/about.html")
def enquiry(request):
    return render(request,"home/enquiry.html")  
def send_enquiry(request):
	name=request.POST['fname']
	posted_date = timezone.now().date()
	emailid=request.POST['Email']
	phno=request.POST['number']
	address=request.POST['add']
	case_det=request.POST['case']

	obj_enq=models.Enquiry(name=name,address=address,email=emailid,mobile=phno,case_details=case_det,post_date=posted_date)
	obj_enq.save()
	return redirect('home')

def ask_question(request):
	qu_li=models.MessagePanel.objects.raw("select * from message_panel where parent_id is null")
	context={
	'qlist':qu_li
	}
	return render(request,"home/question.html",context)  
def save_question(request):
	msg=request.POST['question']
	posted_date = timezone.now().date()

	obj_msg=models.MessagePanel(message=msg,post_date=posted_date)
	obj_msg.save()
	return redirect('ask_question')
def contact(request):
    return render(request,"home/contact.html")
def login(request):
    return render(request,"login/login.html")


def check_login(request):
    username = request.POST['uname']
    password = request.POST['password']

    log_info = models.Login.objects.filter(username=username, password=password)

    for info in log_info:
        if info.username == username and info.password == password:
            if info.user_type == 'admin':
                request.session['username'] = info.username
                request.session['user_type'] = info.user_type
                return redirect("../administrator/admin_dashboard")

            elif info.user_type == 'advocate':
                request.session['semail'] = info.username
                adv_list = models.Advocates.objects.filter(email=info.username)

                if len(adv_list) > 0:
                    advocate = adv_list[0]
                    request.session['adv_id'] = advocate.adv_id
                    request.session['usertype'] = info.user_type
                    request.session['first_name'] = advocate.first_name
                    return redirect("../advocate/advocate_dashboard")
                else:
                    messages.error(request, 'Advocate not found. Login failed')
                    return redirect("login")

            elif info.user_type == 'client':
                    request.session['semail'] = info.username
                    cli_list=models.Clients.objects.filter(email_id=info.username)
                    if(len(cli_list)>0):
                        clients= cli_list[0];
                        request.session['client_id'] = clients.client_id
                        request.session['usertype'] = info.user_type
                        request.session['first_name'] = clients.first_name
                        
                       
                        return redirect("../client/client_dashboard")
                    else:

                        messages.error(request, 'client not found. Login failed')
                        return redirect("login")

    # If no matching user is found, display an error message and redirect to login page
    messages.error(request, 'Invalid username or password. Login failed')
    return redirect("login")

    #   else:
    #     messages.error(request,'Invalid Email Address')
    #     return redirect("login")
    # messages.error(request,'Invalid Email Address')
    # return redirect("login")
def change_password(request):
  return render(request,'admin/change_password.html')
def update_password(request):
  newpassword=request.POST['newpassword']
  confirmpassword=request.POST['confirmpassword']
  username=request.session['username']
  if newpassword==confirmpassword:
    log=models.Login.objects.filter(username=username)
    log.update(password=newpassword)
    return render(request,"home/index.html")
  else:
    return render(request,"admin/change_password.html") 
def logout(request):
  Session.objects.all().delete()
  return redirect('login')
def forgot(request):
  return render(request,"login/forgot.html")
def otp(request):
  if request.method=="POST":
    otp_now=request.POST.get('otp_code')
    otp=request.session['otp']
    if otp_now==otp:
      return render(request,"login/new_password.html")
  else:
    messages.error(request,'Invalid OTP')
  messages.error(request,'Invalid Data Entered')
  return render(request,"login/otp.html")
def new_password(request):
   newpassword=request.POST['npassword']
   confirmpassword=request.POST['cpassword']
   username=request.session['otpemail']
   if newpassword==confirmpassword:
    log=models.Login.objects.filter(username=username)
    log.update(password=newpassword)
    return redirect('login')
def email_verify(request):
  if request.method=='POST':
    username=request.POST.get('username')
    log_info=models.Login.objects.filter(username=username)
    for info in log_info:
      if info.username == username:
        otp=str(random.randint(1000,9999))
        request.session['otp']=otp
        request.session['otpemail']=info.username
        subject='PASSWORD RESETTING FOR LEGAL SUPPORT SYSTEM'
        message="Your OTP is:"+otp
        email_id=request.session['otpemail']
        send_mail(subject,message,EMAIL_HOST_USER,[email_id],fail_silently=False)
        return render(request,'login/otp.html')
      else:
          messages.error(request,'Invalid Email Address')
          return redirect("forgot")
  messages.error(request,'Invalid Email Address')
  return redirect("forgot")

  
  



    


