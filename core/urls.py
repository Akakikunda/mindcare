from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from .views import role_redirect_view
from . import views
from .views import resources_view  # add this
from .views import assessments_view
from .views import notifications_view, profile_view, logout_view



from .views import (
    register_view, profile_view, home_view, book_appointment, appointment_success,
    take_assessment, my_assessments, view_resources, therapist_directory,
    send_message, inbox, crisis_support, patient_profile, therapist_dashboard,
    edit_profile, admin_dashboard, dashboard, update_appointment_status,
    individual_assessment, couple_assessment, family_assessment, teen_assessment
)

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('login/', views.custom_login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('login/', views.custom_login, name='login'),


    # Profile
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('patient/profile/', patient_profile, name='patient_profile'),

    # Bookings
    path('book/', book_appointment, name='book_appointment'),
    path('book/success/', appointment_success, name='appointment_success'),
    path('appointment/<int:appointment_id>/<str:status>/', update_appointment_status, name='update_appointment_status'),
    path('appointments/', views.appointments_view, name='appointments'),
    
 
    # Assessments
    path('assessments/take/', take_assessment, name='take_assessment'),
    path('assessments/results/', my_assessments, name='my_assessments'),
    path('assessment/individual/', individual_assessment, name='individual_assessment'),
    path('assessment/couple/', couple_assessment, name='couple_assessment'),
    path('assessment/family/', family_assessment, name='family_assessment'),
    path('assessment/teen/', teen_assessment, name='teen_assessment'),
    path('assessment/', views.assessment_view, name='assessment'),
    
    path('assessments/', assessments_view, name='assessments'),  # ✅ Fixes your error
    
       # Dashboard
    path('dashboard/', dashboard, name='dashboard'),
    path('therapist/dashboard/', therapist_dashboard, name='therapist_dashboard'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),



    # Therapists & Resources
    path('therapists/', therapist_directory, name='therapist_directory'),
    path('therapist/<int:therapist_id>/', views.therapist_profile_view, name='therapist_profile'),
    path('resources/', view_resources, name='view_resources'),
    path('resources/', views.view_resources, name='view_resources'),


    # Messaging
    path('message/send/', send_message, name='send_message'),
    path('message/inbox/', inbox, name='inbox'),

    # Crisis Support
    path('crisis/', crisis_support, name='crisis_support'),

    # Admin
    path('admin/users/', views.manage_users, name='manage_users'),
    path('admin/users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),  # point this to client dashboard

        



    path('role-redirect/', role_redirect_view, name='role_redirect'),
    
    #appointments
    

    #projects 
    path('projects/', views.projects_view, name='projects'),
    
    path('', views.landing_page, name='landing'),
    

    path('resources/', resources_view, name='resources'),  # ✅ this line fixes your error
    

    path('notifications/', notifications_view, name='notifications'),
    path('profile/', profile_view, name='profile'),
    path('logout/', logout_view, name='logout'),






    path('admin/users/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('admin/users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('admin/resources/upload/', views.upload_resource, name='upload_resource'),


    #path('admin/resources/upload/', views.upload_resource, name='upload_resource'),
   # path('admin/resources/<int:resource_id>/edit/', views.edit_resource, name='edit_resource'),
    #path('admin/resources/<int:resource_id>/delete/', views.delete_resource, name='delete_resource'),
    
    path('dashboard/resources/upload/', views.upload_resource, name='upload_resource'),
    path('dashboard/resources/<int:resource_id>/edit/', views.edit_resource, name='edit_resource'),
    path('dashboard/resources/<int:resource_id>/delete/', views.delete_resource, name='delete_resource'),



    path('redirect/', views.redirect_user_by_role, name='redirect_user'),



    # Password Reset
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
