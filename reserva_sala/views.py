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
        # Consultar las salas disponibles (todas las salas para mostrar su estado)
        salas_disponibles = Sala.objects.all().order_by('nombre')
        
        # Pasar las salas al contexto
        context = {
            'salas_disponibles': salas_disponibles
        }
        
        return render(request, self.template_name, context)


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


def validar_rut_chileno(rut):
    rut = rut.upper().replace(".", "").replace("-", "")
    cuerpo = rut[:-1]
    dv = rut[-1]

    if not cuerpo.isdigit():
        return False

    suma = 0
    multiplo = 2

    for c in reversed(cuerpo):
        suma += int(c) * multiplo
        multiplo = multiplo + 1 if multiplo < 7 else 2

    dv_calculado = 11 - (suma % 11)
    if dv_calculado == 10:
        dv_calculado = 'K'
    elif dv_calculado == 11:
        dv_calculado = '0'
    else:
        dv_calculado = str(dv_calculado)

    return dv == dv_calculado


@require_POST
@user_passes_test(lambda u: u.is_superuser)
def create_user(request):
    try:
        rut = request.POST.get("rut").upper().replace(".", "").replace("-", "")
        
        if not validar_rut_chileno(rut):
            messages.error(request, "RUT inválido")
            return redirect("dashboard")
            
        # Formatear RUT con guión: 12345678-9
        rut_formateado = f"{rut[:-1]}-{rut[-1]}"
        
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        estado = request.POST.get("estado")

        # Crear el usuario
        user = Usuario.objects.create_user(
            email=email,
            rut=rut_formateado,
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


@require_POST
@user_passes_test(lambda u: u.is_superuser)
def create_classroom(request):
    try:
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        estado = request.POST.get("estado")

        # Crear la sala
        sala = Sala.objects.create(
            nombre=nombre, descripcion=descripcion, estado=estado
        )

        messages.success(request, f"Sala '{nombre}' creada exitosamente")
        return redirect("dashboard")
    except Exception as e:
        messages.error(request, f"Error al crear sala: {str(e)}")
        return redirect("dashboard")


# Vistas para listar usuarios
@login_required
@user_passes_test(lambda u: u.is_superuser)
def list_users(request):
    users = Usuario.objects.all().order_by("last_name", "first_name")
    return render(request, "reserva_sala/admin/user_list.html", {"users": users})


# Vista para listar salas
@login_required
@user_passes_test(lambda u: u.is_superuser)
def list_classrooms(request):
    classrooms = Sala.objects.all().order_by("nombre")
    return render(
        request, "reserva_sala/admin/classroom_list.html", {"classrooms": classrooms}
    )


# Vista para eliminar usuario
@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    try:
        user = Usuario.objects.get(id=user_id)
        name = f"{user.first_name} {user.last_name}"
        user.delete()
        messages.success(request, f"Usuario {name} eliminado correctamente")
    except Exception as e:
        messages.error(request, f"Error al eliminar usuario: {str(e)}")
    return redirect("list_users")


# Vista para eliminar sala
@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_classroom(request, classroom_id):
    try:
        classroom = Sala.objects.get(id=classroom_id)
        name = classroom.nombre
        classroom.delete()
        messages.success(request, f"Sala {name} eliminada correctamente")
    except Exception as e:
        messages.error(request, f"Error al eliminar sala: {str(e)}")
    return redirect("list_classrooms")


# Vista para actualizar usuario
@login_required
@user_passes_test(lambda u: u.is_superuser)
def update_user(request, user_id):
    try:
        user = Usuario.objects.get(id=user_id)
        if request.method == "POST":
            user.rut = request.POST.get("rut")
            user.first_name = request.POST.get("first_name")
            user.last_name = request.POST.get("last_name")
            user.email = request.POST.get("email")
            user.estado = request.POST.get("estado")

            # Solo actualizar la contraseña si se proporciona una nueva
            password = request.POST.get("password")
            if password and password.strip():
                user.set_password(password)

            user.save()
            messages.success(
                request,
                f"Usuario {user.first_name} {user.last_name} actualizado correctamente",
            )
        else:
            return JsonResponse({"error": "Método no permitido"}, status=405)
    except Exception as e:
        messages.error(request, f"Error al actualizar usuario: {str(e)}")
    return redirect("list_users")


# Vista para actualizar sala
@login_required
@user_passes_test(lambda u: u.is_superuser)
def update_classroom(request, classroom_id):
    try:
        classroom = Sala.objects.get(id=classroom_id)
        if request.method == "POST":
            classroom.nombre = request.POST.get("nombre")
            classroom.descripcion = request.POST.get("descripcion")
            classroom.estado = request.POST.get("estado")
            classroom.save()
            messages.success(
                request, f"Sala {classroom.nombre} actualizada correctamente"
            )
        else:
            return JsonResponse({"error": "Método no permitido"}, status=405)
    except Exception as e:
        messages.error(request, f"Error al actualizar sala: {str(e)}")
    return redirect("list_classrooms")
