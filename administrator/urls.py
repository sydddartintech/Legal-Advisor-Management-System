from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),

path('change_pass/',views.change_pass,name='change_pass'),
path('update_pass/',views.update_pass,name='update_pass'),
    
    path('add_categ/',views.add_categ,name='add_categ'),
path('save_category/',views.save_category,name='save_category'),
path('show_category/',views.show_category,name='show_category'),
path('edit_category/<int:cid>/',views.edit_category,name='edit_category'),
path('update_category/',views.update_category,name='update_category'),
path('delete_category/<int:cid>/',views.delete_category,name='delete_category'),

    

path('add_advocates/',views.add_advocates,name='add_advocates'),
path('save_advocate/',views.save_advocate,name='save_advocate'),
path('show_advocates/',views.show_advocates,name='show_advocates'),
path('edit_advocates/<int:ad_id>/',views.edit_advocates,name='edit_advocates'),
path('update_advocates/',views.update_advocates,name='update_advocates'),
path('delete_adv/<int:aid>/',views.delete_adv,name='delete_adv'),
path('change_adv_image/<int:aid>/',views.change_adv_image,name='change_adv_image'),
path('update_adv_image/',views.update_adv_image,name='update_adv_image'),

path('add_milestone/<int:ad_id>/',views.add_milestone,name='add_milestone'),
path('show_milestone/<int:ad_id>/',views.show_milestone,name='show_milestone'),
path('save_milestone/',views.save_milestone,name='save_milestone'),
path('edit_milestone/<int:mid>/',views.edit_milestone,name='edit_milestone'),
path('update_milestone/',views.update_milestone,name='update_milestone'),
path('delete_milestone/<int:mid>/',views.delete_milestone,name='delete_milestone'),
    

path('add_client/',views.add_client,name='add_client'),
path('show_client/',views.show_client,name='show_client'),
path('save_client/',views.save_client,name='save_client'),

path('change_image/<int:clid>/',views.change_image,name='change_image'),
path('update_image/',views.update_image,name='update_image'),
path('change_idproof/<int:clid>/',views.change_idproof,name='change_idproof'),
path('update_proof/',views.update_proof,name='update_proof'),

path('client_details/<int:clid>/',views.client_details,name='client_details'),
path('client_edit/<int:clid>/',views.client_edit,name='client_edit'),
path('update_client/',views.update_client,name='update_client'),
path('delete_client/<int:clid>/',views.delete_client,name='delete_client'),

path('show_case_details/<int:clid>/',views.show_case_details,name='show_case_details'),
path('add_case_details/<int:clid>/',views.add_case_details,name='add_case_details'),
path('get_advocate/',views.get_advocate,name='get_advocate'),
path('save_case_details/',views.save_case_details,name='save_case_details'),

path('view_case_documents/<int:cno>/',views.view_case_documents,name='view_case_documents'),
path('view_case_history/<int:cno>/',views.view_case_history,name='view_case_history'),

path('edit_case_details/<int:cno>/',views.edit_case_details,name='edit_case_details'),
path('update_case_details/',views.update_case_details,name='update_case_details'),
path('delete_case_details/<int:cno>/',views.delete_case_details,name='delete_case_details'),

path('view_case_schedule/<int:cno>/',views.view_case_schedule,name='view_case_schedule'),
path('add_case_schedule/<int:cno>/',views.add_case_schedule,name='add_case_schedule'),
path('save_case_schedule/',views.save_case_schedule,name='save_case_schedule'),
path('edit_case_schedule/<int:sid>/',views.edit_case_schedule,name='edit_case_schedule'),
path('update_case_schedule/',views.update_case_schedule,name='update_case_schedule'),
path('delete_schedule/<int:sid>/',views.delete_schedule,name='delete_schedule'),
path('profile/',views.profile,name='profile'),
    
path('enquiry_list/',views.enquiry_list,name='enquiry_list'),
path('enquiry_details/<int:eid>/',views.enquiry_details,name='enquiry_details'),   

path('trans_details/',views.trans_details,name='trans_details'),
    
]