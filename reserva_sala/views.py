from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import AccesoSala, Sala, Usuario
from django.http import JsonResponse
from django.views.decorators.http import require_POST


class LoginView(View):
    template_name = "login.html"

    def get(self, request):
        # Si el usuario ya está autenticado, redirigir al dashboard
        if request.user.is_authenticated:
            return redirect("dashboard")
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            # Redirigir a la página después del login
            return redirect("dashboard")
        else:
            messages.error(request, "Email o contraseña incorrectos")
            return render(request, self.template_name, {"email": email})


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Has cerrado sesión correctamente")
        return redirect("login")


@method_decorator(login_required, name="dispatch")
class DashboardView(View):
    template_name = "dashboard.html"

    def get(self, request):
        return render(request, self.template_name)


# Vista de reserva
class ReservationView(CreateView):
    model = AccesoSala
    template_name = "reserva_sala/reserva_form.html"
    fields = ["fecha_reserva", "bloque_horario"]

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.sala = Sala.objects.get(id=self.kwargs["pk"])
        return super().form_valid(form)


# Vistas de administración
class ManageUserView(UpdateView):
    model = Usuario
    template_name = "reserva_sala/admin/user_form.html"
    fields = ["rut", "first_name", "last_name", "email", "is_active"]
    success_url = reverse_lazy("dashboard")


class ManageClassroomView(UpdateView):
    model = Sala
    template_name = "reserva_sala/admin/classroom_form.html"
    fields = ["nombre", "descripcion", "estado"]
    success_url = reverse_lazy("dashboard")


@require_POST
@user_passes_test(lambda u: u.is_superuser)
def create_user(request):
    try:
        rut = request.POST.get("rut")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        estado = request.POST.get("estado")

        # Crear el usuario
        user = Usuario.objects.create_user(
            email=email,
            rut=rut,
            password=password,
            first_name=first_name,
            last_name=last_name,
            estado=estado,
        )

        messages.success(
            request, f"Usuario {first_name} {last_name} creado exitosamente"
        )
        return redirect("dashboard")
    except Exception as e:
        messages.error(request, f"Error al crear usuario: {str(e)}")
        return redirect("dashboard")
