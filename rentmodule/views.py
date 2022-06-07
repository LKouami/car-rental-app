import uuid
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
from collections import namedtuple
from authentication.models import CustomUser
from rentmodule.models import Bill, Car, CarImages, Reservation
from django.contrib.auth.decorators import login_required
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from borb.pdf import Document
from borb.pdf.page.page import Page
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from decimal import Decimal
from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable as Table
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.canvas.layout.layout_element import Alignment
import datetime
import random
from borb.pdf.pdf import PDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
# Create your views here.
    
@login_required(login_url="auth:login")
def home(request):
    return render(request, "rent/home.html")

@login_required(login_url="auth:login")
def locations_list(request):
    current_user = CustomUser.objects.get(pk = request.user.pk) 
    user_reservations = Reservation.objects.filter(client = current_user )
    context = {
        "user_reservations" : user_reservations
        }
    return render(request, "rent/my_locations.html", context)

@login_required(login_url="auth:login")
def billgen(request, reservation_id):
    current_user = CustomUser.objects.get(pk = request.user.pk) 
    current_reservation = Reservation.objects.get(pk = reservation_id )
    print(current_reservation)
    user_bill = Bill.objects.get( reservation = current_reservation)
    num_btw_date = (current_reservation.end_date_time - current_reservation.begin_date_time).days
    total_due_amount = num_btw_date * user_bill.car.price
    print(total_due_amount)
    # Create a file-like buffer to receive PDF data.
    print(type(user_bill.date_of_bill))
    # x = datetime.datetime(user_bill.date_of_bill)
    print(user_bill.date_of_bill.strftime('%x  %X'))
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.setLineWidth(.3)
    p.setFont('Helvetica', 12)
    p.drawString(30,750,'FACTURE A PAYER')
    p.drawString(30,735,'LOCATION DE VOITURE')
    p.drawString(315,750, 'DATE DE LA FACTURATION :' )
    p.drawString(490,750, str(user_bill.date_of_bill.strftime('%x %X')) )
    p.drawString(220,690,'DETAILS DE LA FACTURE')
    p.line(220,688,370,688)
    p.drawString(30,650, 'DATE DEBUT :' )
    p.drawString(150,650, str(current_reservation.begin_date_time.strftime('%x %X')) )
    p.drawString(30,620, 'DATE FIN :' )
    p.drawString(150,620, str(current_reservation.end_date_time.strftime('%x %X')) )
    p.drawString(30,590,'NOMBRE DE JOUR:')
    p.drawString(150,590,str(num_btw_date))
    p.drawString(30,560,'MONTANT TOTAL:')
    p.drawString(150,560,str(total_due_amount))
    p.drawString(30,530,'ADRESSEE A:')
    p.drawString(150,530, str(current_user.first_name +'  ' + current_user.last_name))
    p.drawString(30,500,'PAYABLE PAR FLOOZ : 96969696 OU TMONEY : 90909090')
    p.drawString(30,470,'NB : GARDEZ VOTRE NUMERO TXN ID POUR VERIFIER LE PAYEMENT A L\'AGENCE, MERCI ')
    p.showPage()
    p.save()
    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')


@login_required(login_url="auth:login")
def about(request):
    return render(request, "rent/about.html")

@login_required(login_url="auth:login")
def reservation_actions(request, car_id):
    print('dbuuuuuuuuuuuuuuuuuuuuuuuuuuuuuut')
    if request.method == "POST":
        begin_date = request.POST["begin_date"]
        end_date = request.POST["end_date"]
        tel = request.POST["tel"]
        cni_num = request.POST["cni_num"]
        dlicense_num = request.POST["dlicense_num"]
        current_user = CustomUser.objects.get(pk = request.user.pk) 
        current_car = Car.objects.get(pk = car_id) 
        current_user.tel = tel
        current_user.cni_num = cni_num
        current_user.dlicense_num = dlicense_num
        current_user.save()
        unique_id = str(uuid.uuid4()) 
        new_reservation = Reservation.objects.create(
            begin_date_time = begin_date,
            end_date_time = end_date,
            unique_id = unique_id,
            state = "En attente",
            car = current_car,
            client = current_user
        )
        new_reservation.save()
        current_reservation = Reservation.objects.get(unique_id = unique_id) 
        new_bill = Bill.objects.create(
            client = current_user,
            car = current_car,
            reservation = current_reservation
        )
        new_bill.save()
        current_car.state = 'Réservée'
        current_car.save()
        context = {
            
        }
    print('fiiiiiinnnnnnnnnnnnnnnnn')
    return redirect("rent:cars_list")

@login_required(login_url="auth:login")
def cars_detail(request, car_id):
    print(request.user)
    print('Je viens ici')
    car_detail = get_object_or_404(Car,  id=car_id)
    print(car_detail)
    context = {
        "car_detail": car_detail,
    }
    print(car_id)
    return render(request, "rent/my_cars_details.html", context)

@login_required(login_url="auth:login")
def cars_list(request):
    cars = Car.objects.order_by('-brand')
    paginator = Paginator(cars, 8)
    page = request.GET.get('page')
    try:
        total = paginator.num_pages
        cars = paginator.page(page)
    except PageNotAnInteger:
        cars = paginator.page(1)
    except EmptyPage:
        cars = paginator.page(paginator.num_pages)
    context = {
        "cars": cars,
        "total": total
    }
    return render(request, "rent/my_cars.html", context=context)