from django.shortcuts import render, redirect, get_object_or_404
from .models import Reserva  # Asegúrate de que este es el modelo correcto
from datetime import datetime

# Vista para la página de inicio
def inicio_vista(request):
    reservas = Reserva.objects.all()
    print("Reservas actuales en la base de datos:", list(reservas))  # Verifica qué reservas se están pasando al template
    return render(request, 'GestionarReserva.html', {'reservas': reservas})
def editarReserva(request, id):
    reserva = get_object_or_404(Reserva, Id_Reserva=id)

    if request.method == 'POST':
        # Obtener la fecha enviada desde el formulario
        fecha_reserva = request.POST.get("txtFecha_Reserva")
        
        # Verificar el formato de la fecha
        try:
            # Intenta convertirla a un objeto datetime
            fecha_obj = datetime.strptime(fecha_reserva, "%Y-%m-%d")
        except ValueError:
            # Si la fecha no tiene el formato adecuado, muestra un error
            return render(request, "editarReserva.html", {
                "reserva": reserva,
                "error": "La fecha debe estar en formato YYYY-MM-DD."
            })

        # Si la fecha es válida, actualiza los demás campos
        reserva.Id_pasajero = request.POST["txtId_pasajero"]
        reserva.Id_vuelo = request.POST["txtId_vuelo"]
        reserva.Fecha_Reserva = fecha_obj
        reserva.Estado_reserva = request.POST["txtEstado_reserva"]
        reserva.Clase_Servicio = request.POST["txtClase_Servicio"]
        reserva.Numero_Reserva = request.POST["txtNumero_Reserva"]

        # Guardar los cambios
        reserva.save()

        # Redirigir a la página de listado
        return redirect('Reserva')

    return render(request, "editarReserva.html", {"reserva": reserva})

# Vista para registrar una reserva
def registrarReserva(request):
    if request.method == "POST":
        # Obtener los datos del formulario
        id_pasajero = request.POST.get('txtId_pasajero')
        id_vuelo = request.POST.get('txtId_vuelo')
        fecha_reserva = request.POST.get('txtFecha_Reserva')
        estado_reserva = request.POST.get('txtEstado_reserva')
        clase_servicio = request.POST.get('txtClase_Servicio')
        numero_reserva = request.POST.get('txtNumero_Reserva')

        # Crear un objeto Reserva con los datos
        reserva = Reserva(
            Id_pasajero=id_pasajero,
            Id_vuelo=id_vuelo,
            Fecha_Reserva=fecha_reserva,
            Estado_reserva=estado_reserva,
            Clase_Servicio=clase_servicio,
            Numero_Reserva=numero_reserva
        )
        # Guardar la reserva en la base de datos
        reserva.save()
        
        # Redirigir a la página principal tras registrar
        return redirect('Reserva')  # Asume que 'Reserva' es la URL de listado

    # Si el formulario no fue enviado (GET), renderiza la página con las reservas
    reservas = Reserva.objects.all()
    return render(request, 'GestionarReserva.html', {'reservas': reservas})


# Vista para seleccionar la reserva para editar
def seleccionarReserva(request, id_reserva):
    reserva = get_object_or_404(Reserva, Id_Reserva=id_reserva)
    return render(request, "editarReserva.html", {"reserva": reserva})

# Vista para editar los datos de la reserva
def editarReserva(request, id):
    # Obtener la reserva a editar
    reserva = get_object_or_404(Reserva, Id_Reserva=id)

    if request.method == 'POST':
        # Actualizar los campos con los valores del formulario
        reserva.Id_pasajero = request.POST["txtId_pasajero"]
        reserva.Id_vuelo = request.POST["txtId_vuelo"]
        reserva.Fecha_Reserva = request.POST["txtFecha_Reserva"]
        reserva.Estado_reserva = request.POST["txtEstado_reserva"]
        reserva.Clase_Servicio = request.POST["txtClase_Servicio"]
        reserva.Numero_Reserva = request.POST["txtNumero_Reserva"]

        # Guardar los cambios en la base de datos
        reserva.save()
        print("Reserva actualizada con éxito:", reserva)

        # Redirigir a la página de listado
        return redirect('Reserva')

    # Si es GET, renderizar el formulario con los datos actuales de la reserva
    return render(request, "editarReserva.html", {"Reserva": reserva})

# Vista para borrar una reserva
def borrarReserva(request, Id_Reserva):
    try:
        reserva = Reserva.objects.get(Id_Reserva=Id_Reserva)
        reserva.delete()
        return redirect("Reserva")
    except Reserva.DoesNotExist:  # Corrige el modelo al correcto
        return render(request, "error.html", {"mensaje": "La reserva no existe"})
