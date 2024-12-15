from django.contrib import admin
from django.urls import path
from .import views
urlpatterns = [
path('advocate_dashboard/',views.advocate_dashboard,name='advocate_dashboard'),

path('change_password/',views.change_password,name='change_password'),
path('update_password/',views.update_password,name='update_password'),

path('adv_profile/',views.adv_profile,name='adv_profile'),

path('ongoing_case_client/',views.ongoing_case_client,name='ongoing_case_client'),
path('schedule_details_client/<int:cno>/',views.schedule_details_client,name='schedule_details_client'),
path('case_details/<int:cno>/',views.case_details,name='case_details'),

path('case_history_view/<int:cno>/',views.case_history_view,name='case_history_view'),
path('case_history_add/<int:cno>/',views.case_history_add,name='case_history_add'),
path('save_history/',views.save_history,name='save_history'),
path('edit_case_history/<int:hid>/',views.edit_case_history,name='edit_case_history'),
path('update_history/',views.update_history,name='update_history'),
path('delete_history/<int:hid>/',views.delete_history,name='delete_history'),

path('case_documents_view/<int:cno>/',views.case_documents_view,name='case_documents_view'),
path('case_doc_add/<int:cno>/',views.case_doc_add,name='case_doc_add'),
path('save_doc/',views.save_doc,name='save_doc'),
path('change_document/<int:doid>/',views.change_document,name='change_document'),
path('update_document/',views.update_document,name='update_document'),
path('edit_document/<int:doid>/',views.edit_document,name='edit_document'),
path('update_doc_details/',views.update_doc_details,name='update_doc_details'),
path('delete_document/<int:doid>/',views.delete_document,name='delete_document'),

path('closed_case/',views.closed_case,name='closed_case'),

path('message_panel/',views.message_panel,name='message_panel'),
path('message_rply/<int:msgid>/',views.message_rply,name='message_rply'),
path('save_rply/',views.save_rply,name='save_rply'),

]