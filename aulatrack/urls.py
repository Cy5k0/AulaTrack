from django.contrib import admin
from django.urls import path, include
from reserva_sala import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("reserva_sala.urls")),
    path("reservar/<int:pk>/", views.ReservationView.as_view(), name="reservar_sala"),
    path(
        "admin/users/<str:action>/", views.ManageUserView.as_view(), name="manage_user"
    ),
    path(
        "admin/classrooms/<str:action>/",
        views.ManageClassroomView.as_view(),
        name="manage_classroom",
    ),
]
