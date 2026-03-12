from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("login/", auth_views.LoginView.as_view(template_name="predictor/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),

    path("dashboard/", views.dashboard, name="dashboard"),

    path("patients/", views.patient_list, name="patient_list"),
    path("patients/add/", views.add_patient, name="add_patient"),
    path("patients/<int:patient_id>/", views.patient_detail, name="patient_detail"),

    path("history/", views.history, name="history"),
]