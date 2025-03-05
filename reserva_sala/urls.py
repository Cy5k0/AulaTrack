from django.urls import path
from . import views

urlpatterns = [
    path("", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("create-user/", views.create_user, name="create_user"),
    path("create-classroom/", views.create_classroom, name="create_classroom"),
    path("users/list/", views.list_users, name="list_users"),
    path("classrooms/list/", views.list_classrooms, name="list_classrooms"),
    path("users/delete/<int:user_id>/", views.delete_user, name="delete_user"),
    path(
        "classrooms/delete/<int:classroom_id>/",
        views.delete_classroom,
        name="delete_classroom",
    ),
    path("users/update/<int:user_id>/", views.update_user, name="update_user"),
    path(
        "classrooms/update/<int:classroom_id>/",
        views.update_classroom,
        name="update_classroom",
    ),
    path('reservar/<int:pk>/', views.ReservationView.as_view(), name='reservar_sala'),
]
