from django.contrib import admin
from django.urls import path
from .import views
urlpatterns = [
path('client_dashboard/',views.client_dashboard,name='client_dashboard'),
path('my_profile/',views.my_profile,name='my_profile'),
path('ongoing_case/',views.ongoing_case,name='ongoing_case'),
path('schedule_details/<int:cno>/',views.schedule_details,name='schedule_details'),
path('case_details_client/<int:cno>/',views.case_details_client,name='case_details_client'),
path('case_history_view_client/<int:cno>/',views.case_history_view_client,name='case_history_view_client'),

path('case_documents_view_client/<int:cno>/',views.case_documents_view_client,name='case_documents_view_client'),
path('case_doc_add_client/<int:cno>/',views.case_doc_add_client,name='case_doc_add_client'),
path('save_doc_client/',views.save_doc_client,name='save_doc_client'),
path('change_document_client/<int:doid>/',views.change_document_client,name='change_document_client'),
path('update_document_client/',views.update_document_client,name='update_document_client'),
path('edit_document_client/<int:doid>/',views.edit_document_client,name='edit_document_client'),
path('update_doc_details_client/',views.update_doc_details_client,name='update_doc_details_client'),
path('delete_document_client/<int:doid>/',views.delete_document_client,name='delete_document_client'),

path('closed_case_client/',views.closed_case_client,name='closed_case_client'),
path('adv_details/<int:cno>/',views.adv_details,name='adv_details'),

path('transactions/',views.transactions,name='transactions'),
path('client_payment/',views.client_payment,name='client_payment'),
path('client_transaction/',views.client_transaction,name='client_transaction'),

path('change_password/',views.change_password,name='change_password'),
path('update_password/',views.update_password,name='update_password'),
]