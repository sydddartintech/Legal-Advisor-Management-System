# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AdvocateMilestone(models.Model):
    adv_ms_id = models.AutoField(primary_key=True)
    adv_id = models.IntegerField()
    title = models.TextField()
    description = models.TextField()
    posted_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'advocate_milestone'


class Advocates(models.Model):
    adv_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=20)
    experience = models.CharField(max_length=70)
    case_cat_id = models.IntegerField()
    email = models.CharField(max_length=70)
    photo = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'advocates'


class Bank(models.Model):
    bank_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    card_number = models.CharField(max_length=200)
    expiry = models.CharField(max_length=200)
    cvv = models.IntegerField()
    amount = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'bank'


class CaseCategory(models.Model):
    cat_id = models.AutoField(primary_key=True)
    cat_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'case_category'


class CaseDetails(models.Model):
    case_no = models.AutoField(primary_key=True)
    case_cat_id = models.IntegerField()
    description = models.TextField()
    case_register_date = models.DateField()
    case_start_date = models.DateField()
    remark = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20)
    clientid = models.IntegerField()
    advocate_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'case_details'


class CaseDocuments(models.Model):
    doc_id = models.AutoField(primary_key=True)
    doc_title = models.CharField(max_length=100)
    doc_desc = models.TextField()
    doc_file = models.CharField(max_length=50)
    doc_uploaded_date = models.DateField()
    case_id = models.CharField(max_length=50)
    uploaded_by = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'case_documents'


class CaseHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    case_no = models.CharField(max_length=50)
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'case_history'


class CaseSchedules(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    sh_date = models.DateField()
    case_id = models.CharField(max_length=50)
    remark = models.TextField()

    class Meta:
        managed = False
        db_table = 'case_schedules'


class ClientTransaction(models.Model):
    trans_id = models.AutoField(primary_key=True)
    fk_client_email = models.CharField(max_length=200)
    trans_date = models.DateField()
    amount = models.IntegerField()
    remarks = models.TextField()

    class Meta:
        managed = False
        db_table = 'client_transaction'


class Clients(models.Model):
    client_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    dob = models.DateField()
    state = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    pin = models.IntegerField()
    mobile = models.CharField(max_length=20)
    email_id = models.CharField(max_length=70)
    aadhaar_no = models.CharField(max_length=20)
    photo = models.CharField(max_length=50)
    identity_type = models.CharField(max_length=50)
    identity_file = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'clients'


class Enquiry(models.Model):
    enq_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=70)
    address = models.CharField(max_length=150)
    email = models.CharField(max_length=100)
    mobile = models.CharField(max_length=20)
    case_details = models.TextField()
    post_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'enquiry'


class ForgotPassword(models.Model):
    forgotpassword_id = models.AutoField(primary_key=True)
    email_id = models.CharField(max_length=70)
    random_code = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'forgot_password'


class Login(models.Model):
    username = models.CharField(primary_key=True, max_length=70)
    password = models.CharField(max_length=50)
    user_type = models.CharField(max_length=20)
    status = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'login'


class MessagePanel(models.Model):
    message_id = models.AutoField(primary_key=True)
    message = models.TextField()
    posted_by = models.CharField(max_length=100, blank=True, null=True)
    post_date = models.DateField()
    parent_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'message_panel'
