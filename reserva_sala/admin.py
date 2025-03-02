from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Sala, AccesoSala


class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = (
        "email",
        "rut",
        "first_name",
        "last_name",
        "estado",
        "is_active",
        "is_staff",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "estado")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Información Personal", {"fields": ("rut", "first_name", "last_name")}),
        (
            "Permisos",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Estado", {"fields": ("estado",)}),
        ("Fechas importantes", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "rut",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "estado",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    search_fields = ("email", "rut", "first_name", "last_name")
    ordering = ("email",)

    def save_model(self, request, obj, form, change):
        # Para manejar correctamente el password al crear/editar usuarios
        if "password" in form.changed_data:
            obj.set_password(form.cleaned_data["password"])
        super().save_model(request, obj, form, change)


class SalaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "estado", "fecha_creacion")
    list_filter = ("estado",)
    search_fields = ("nombre", "descripcion")
    ordering = ("nombre",)


class AccesoSalaAdmin(admin.ModelAdmin):
    list_display = ("usuario", "sala", "fecha_reserva", "bloque_horario")
    list_filter = ("sala", "fecha_reserva")
    search_fields = ("usuario__email", "sala__nombre")
    ordering = ("-fecha_reserva",)


admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Sala, SalaAdmin)
admin.site.register(AccesoSala, AccesoSalaAdmin)
