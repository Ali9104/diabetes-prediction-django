from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='predictor/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/add/', views.add_patient, name='add_patient'),
    path('patients/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('predictions/<int:prediction_id>/treatment/', views.add_treatment, name='add_treatment'),

    path('mon-espace/', views.patient_dashboard, name='patient_dashboard'),
    
    path('mon-espace/test/', views.take_test, name='take_test'),
    
    path('mon-espace/resultats/<int:prediction_id>/', views.test_result, name='test_result'),

]