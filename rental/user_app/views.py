import re

from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse
from requests import request
from .models import Contact, User, login, veh_listing, Booking, Review
import razorpay
from django.db.models import Sum



def index(request):
    return render(request,'index.html')

def user_show(request):
    return render(request,'user_reg.html')

def user_registration(request):
    if request.method == 'POST':
        
        em = request.POST['email']
        un = request.POST['name']
        pw = request.POST['password']
        cpw = request.POST['confirm_password']
        

        if pw != cpw:
            return render(request, 'index.html', {'error': 'Passwords do not match'})
        if User.objects.filter(email=em).exists():
            return render(request, 'index.html', {
                'error': 'Email already registered'
            })
        # Create a new User object and save it to the database
        user = User(name=un, email=em)
        user.save()
        user_login = login(email=em, password=pw, status=1)
        user_login.save()
        print("login saved")
        return render(request,'index.html', {'success': 'User registered successfully!'})
    else:
        return render(request, 'index.html', {'error': 'Invalid request method'})


def profile(request):
    reviews = Review.objects.all().order_by('-id')
    print("Total reviews:", reviews.count())

    if 'a_id' in request.session:
        return redirect(admin_dashboard)

    elif 'u_id' in request.session:
        u = request.session['u_id']
        data = User.objects.get(email=u)

        return render(request, 'index2.html', {
            'user': data,
            'reviews': reviews
        })

    return render(request, 'index.html', {
        'reviews': reviews
    })


def login_fun(request):
    u = request.POST['email']
    p = request.POST['password']

    print("Entered:", u, p)

    if u == 'admin' and p == 'admin':
        request.session['a_id'] = u
        return redirect(profile)

    try:
        data = login.objects.get(email=u)

        print("DB Email:", data.email)
        print("DB Password:", data.password)

        if data.password == p:

            if data.status == 1:
                request.session['u_id'] = u
                return redirect(profile)
            else:
                return render(request, 'index.html', {
                    'error': 'Account blocked'
                })

        else:
            return render(request, 'index.html', {
                'error': 'Invalid password'
            })

    except login.DoesNotExist:
        return render(request, 'index.html', {
            'error': 'Invalid username'
        })
def logout(request):
        request.session.flush()  # Clear all session data
        return redirect('/')  # Redirect to the profile view (or login page)
            
# def login_show(request):
#     reviews = Review.objects.all().order_by('-id')  # fetch all reviews, newest first
#     return render(request, 'login.html', {'reviews': reviews})
   



def veh_add_show(request):
    return render (request, 'vehicle_add.html')

from django.shortcuts import render
from django.http import HttpResponse
from .models import veh_listing

def veh_add(request):
    print(request.session['u_id'])
  

    if request.method == 'POST':

        number_plate = request.POST.get('number_plate')

        brand = request.POST.get('brand')
        year = request.POST.get('year')
        veh_type = request.POST.get('type')

        # reg_no = request.POST.get('reg_number', '').upper().strip()

        # if not reg_no:
        #  return HttpResponse("Registration Number is required")

        price_per_day = request.POST.get('price_day')
        price_per_hour = request.POST.get('price_hour')
        price_per_month = request.POST.get('price_month')

        location = request.POST.get('location')
        pickup_location = request.POST.get('pickup')

        fuel_type = request.POST.get('fuel')
        transmission = request.POST.get('trans')

        mileage = request.POST.get('mileage')

        availability = request.POST.get('availability')

        description = request.POST.get('desc')

        image1 = request.FILES.get('im1')
        image2 = request.FILES.get('im2')
        image3 = request.FILES.get('im3')
        image4 = request.FILES.get('im4')


        vim1 = request.FILES.get('vimg1')
        vim2 = request.FILES.get('vimg2')

        # CHECK DUPLICATE REGISTRATION
        if veh_listing.objects.filter(number_plate=number_plate).exists():
            return render(request,
                 "vehicle_add.html",
                    {
                        "vehicle_exists": True
                    }
                )

        user_id = request.session.get('u_id')
        print(user_id)
        owner = User.objects.get(email=user_id) if user_id else None

        vehicle = veh_listing(
           
            owner=owner,
            number_plate=number_plate,
            brand=brand,
            year=year,
            type=veh_type,

            # reg_no=reg_no,

            price_per_day=price_per_day,
           
            location=location,
            pickup_location=pickup_location,

            fuel=fuel_type,
            trans=transmission,

            mileage=mileage,

            is_available=True if availability == 'available' else False,

            description=description,

            image1=image1,
            image2=image2,
            image3=image3,
            image4=image4,
            img1=vim1,
            img2=vim2,
        )
    
        
        vehicle.save()

        return render(
            request,
            "vehicle_add.html",
            {
                "success": True
            }
        )

    return render(request, 'vehicle_add.html')


# view to display all vehicles in the database

def vehicle_list(request):
    data = veh_listing.objects.filter(is_verified=True)
    location = request.GET.get('location')
    if location:
        data = data.filter(location__iexact=location)
    type = request.GET.get('type')
    if type:
        data = data.filter(type__iexact=type)
    
    fuel = request.GET.get('fuel')
    if fuel:
        data = data.filter(fuel__iexact=fuel)
    
    
    print(data)
    return render(request,'vehicle_list.html',{'data':data})


def vehicle_details(request,id):
    data = veh_listing.objects.get(id=id)
    return render(request,'vehicle_details.html',{'data':data})


#   view to book a vehicle
from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
import re
from datetime import datetime
from .models import veh_listing, User, Booking

def book_vehicle(request, id):
    vehicle = veh_listing.objects.get(id=id)
    user = User.objects.get(email=request.session.get('u_id'))
    if vehicle.owner == user:
        return render(request, 'vehicle_booking.html', {
            'vehicle': vehicle,
            'is_owner': True,
            'error': 'You cannot book your own vehicle.'
        })

    if request.method == "POST":
        customer_name = request.POST.get('name')
        customer_phone = request.POST.get('phone')
        phone_pattern = r'^[6-9][0-9]{9}$'

        if not re.match(phone_pattern, customer_phone):
            return render(request, 'vehicle_booking.html', {
                'vehicle': vehicle,
                'error': 'Invalid Phone Number'
            })

        pickup_date = request.POST.get('pickup_date')
        return_date = request.POST.get('return_date')

        aadhar = request.POST.get('aadhar')
        if len(aadhar) != 12 or not aadhar.isdigit():
            return render(request, 'vehicle_booking.html', {
                'vehicle': vehicle,
                'error': 'Invalid Aadhaar Number'
            })

        license_no = request.POST.get('license')
        license_pattern = r'^[A-Z]{2}[0-9]{2}[0-9]{4}[0-9]{7}$'
        if not re.match(license_pattern, license_no):
            return render(request, 'vehicle_booking.html', {
                'vehicle': vehicle,
                'error': 'Invalid License Number'
            })

        license_image = request.FILES.get('license_image')
        aadhar_image = request.FILES.get('aadhar_image')

        # Date calculation
        pickup = datetime.strptime(pickup_date, "%Y-%m-%d")
        return_d = datetime.strptime(return_date, "%Y-%m-%d")
        total_days = (return_d - pickup).days

        if total_days <= 0:
            return render(request, 'vehicle_booking.html', {
                'vehicle': vehicle,
                'error': 'Return date must be after pickup date'
            })

        total_price = (total_days * float(vehicle.price_per_day)) 
        advance_payment = total_price * 0.2  # 20% advance payment

        # Create booking
        Booking.objects.create(
            vehicle=vehicle,
            user=user,
            customer_name=customer_name,
            customer_phone=customer_phone,
            pickup_date=pickup_date,
            return_date=return_date,
            Aadhar_number=aadhar,
            license_number=license_no,
            license_image=license_image,
            aadhar_image=aadhar_image,
            total_price=total_price,
            advance_payment=advance_payment,
            booking_status='Pending'
        )

        # ✅ SUCCESS – render template with booking_success=True
        return render(request, 'vehicle_booking.html', {
            'vehicle': vehicle,
            'booking_success': True
        })

    return render(request, 'vehicle_booking.html', {'vehicle': vehicle})

def new_index(request):
    return render(request,'index2.html')



def profile_view(request):

    user = User.objects.get(
        email=request.session.get('u_id')
    )

    vehicles = veh_listing.objects.filter(
        owner=user
    )

    my_bookings = Booking.objects.filter(
        user=user
    )

    booking_requests = Booking.objects.filter(
        vehicle__owner=user,
        booking_status='Pending'
    )

    return_requests = Booking.objects.filter(
        vehicle__owner=user,
        booking_status='Return Requested'
    )
    refund_requests = Booking.objects.filter(
    vehicle__owner=user,
    booking_status='Cancellation Requested'
)
    messages = Contact.objects.filter(
    email=user.email
).exclude(reply="").order_by('-id')

    return render(
        request,
        'profile.html',
        {
            'user': user,
            'vehicles': vehicles,
            'my_bookings': my_bookings,
            'booking_requests': booking_requests,
            'return_requests': return_requests,
            'refund_requests': refund_requests,
            "messages": messages
        }
    )
# vehicle edit page


def vehicle_edit(request,id):
    data=veh_listing.objects.get(id=id)

    return render(
        request,
        'vehicle_edit.html',
        {'data':data}
    )


def vehicle_update(request, id):
    data = veh_listing.objects.get(id=id)

    data.number_plate = request.POST.get('number_plate')
    data.brand = request.POST.get('brand')
    data.year = request.POST.get('year')
    data.type = request.POST.get('type')
    data.reg_no = request.POST.get('reg_no')
    data.location = request.POST.get('location')
    data.pickup_location = request.POST.get('pickup_location')
    data.mileage = request.POST.get('mileage')
    data.price_per_day = request.POST.get('price_per_day')
    data.price_per_week = request.POST.get('price_per_week')
    data.price_per_month = request.POST.get('price_per_month')
    data.fuel = request.POST.get('fuel')
    data.trans = request.POST.get('trans')
    data.description = request.POST.get('description')

    if request.FILES.get('image1'):
        data.image1 = request.FILES['image1']

    if request.FILES.get('image2'):
        data.image2 = request.FILES['image2']

    if request.FILES.get('image3'):
        data.image3 = request.FILES['image3']

    if request.FILES.get('image4'):
        data.image4 = request.FILES['image4']

    data.save()

    return redirect(f'/vehicle-edit/{id}/?updated=1')



    

def accept_booking(request,id):

    booking = Booking.objects.get(id=id)

    booking.booking_status = "Accepted"
    vehicle = booking.vehicle
    vehicle.is_available = False

    booking.save()
    vehicle.save()

    return redirect('/profile') 


def reject_booking(request,id):

    booking = Booking.objects.get(id=id)

    booking.booking_status = "Rejected"


    booking.save()

    return redirect('/profile')

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def after_payment(request, booking_id):

    print("POST DATA =", request.POST)

    booking = Booking.objects.get(id=booking_id)

    payment_id = request.POST.get('razorpay_payment_id')

    print("PAYMENT ID =", payment_id)

    booking.razorpay_payment_id = payment_id
    booking.booking_status = "Paid"

    booking.save()

    return redirect('/profile')



def payment_summary(request, id):
    booking = Booking.objects.get(id=id)
    request.session['booking_id'] = id
    return render(request, 'payment_summary.html', {'booking': booking})


def pay (request,id,booking_id):
    amount = id*100
    print()
    request.session['amount']=id
    
    return render(request, "pay.html",{'b':amount,'booking_id':booking_id})


def payment_details(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    return render(request, 'payment_details.html', {'booking': booking})

def vehicle_delete(request,id):
    vehicle= veh_listing.objects.get(id=id)
    vehicle = get_object_or_404(
        veh_listing,
        id=id
    )

    vehicle.delete()

    return redirect('profile')

def admin_dashboard(request):
    total_users =User.objects.count()
    total_vehicles = veh_listing.objects.count()
    total_bookings = Booking.objects.count()
    
    vehicles = veh_listing.objects.all()
    bookings = Booking.objects.all()
    return render(request,"admin.html",
                  {
                      "total_users":total_users,
                      "total_vehicles":total_vehicles,
                      "total_bookings":total_bookings,
                      
                      "vehicles":vehicles,
                      "bookings":bookings
    
                  }
                  )

def admin_users(request):

    users = User.objects.all()

    return render(
        request,
        'admin_users.html',
        {
            'users': users
        }
    )

def admin_vehicles(request):
    vehicles = veh_listing.objects.all()
    return render(request, 'admin_vehicles.html', {'vehicles': vehicles})

def delete_vehicle_admin(request, id):

    vehicle = veh_listing.objects.get(id=id)

    vehicle.delete()

    return redirect('admin_vehicles')

def admin_bookings(request):

    bookings = Booking.objects.all().order_by('-id')

    return render(
        request,
        "admin_bookings.html",
        {
            "bookings": bookings
        }
    )

def admin_payments(request):

    payments = Booking.objects.filter(
        booking_status="Paid"
    ).order_by('-id')

    total_revenue = sum(
        booking.total_price
        for booking in payments
    )

    return render(
        request,
        "admin_payments.html",
        {
            "payments": payments,
            "total_revenue": total_revenue
        }
    )


def admin_verifications(request):

    vehicles = veh_listing.objects.filter(is_verified=False).order_by('-id')

    return render(
        request,
        "admin_verifications.html",
        {
            "vehicles": vehicles
        }
    )

def approve_vehicle(request, id):
    vehicle = veh_listing.objects.get(id=id)
    vehicle.is_verified = True
    vehicle.save()

    return redirect('admin_verifications')

def reject_vehicle(request, id):
    vehicle = veh_listing.objects.get(id=id)
    vehicle.delete()      # or set a rejected status instead

    return redirect('admin_verifications')


def admin_logout(request):
    request.session.flush()
    return redirect('/')    # or redirect('login_show')# Redirect to the login page   


def return_vehicle(request, id):

    booking = Booking.objects.get(id=id)

    booking.booking_status = "Return Requested"
    booking.save()

    return redirect('profile')


def confirm_return(request, id):
    booking= Booking.objects.get(id=id)
    booking.booking_status = "Completed"
    vehicle = booking.vehicle
    vehicle.is_available=True
    vehicle.save()
    booking.save()
    return redirect('profile')




from datetime import date, timedelta
from django.core.mail import send_mail
from django.http import HttpResponse
from .models import Booking


from datetime import date, timedelta
from django.core.mail import send_mail
from .models import Booking

def send_return_reminders():

    today = date.today()
    tomorrow = today + timedelta(days=1)

    tomorrow_return = Booking.objects.filter(
        return_date=tomorrow,
        booking_status="Paid"
    )

    today_return = Booking.objects.filter(
        return_date=today,
        booking_status="Paid"
    )

    for booking in tomorrow_return:
        send_mail(
            subject="Vehicle Return Reminder",
            message=f"""
Hello {booking.customer_name},

This is a reminder that your vehicle
{booking.vehicle.brand}
must be returned tomorrow ({tomorrow}).

Please return the vehicle on time.

Thank you,
RentalHub Team
            """,
            from_email="nestfinder9@gmail.com",
            recipient_list=[booking.user.email],
            fail_silently=False,
        )

    for booking in today_return:
        send_mail(
            subject="Vehicle Return Due Today",
            message=f"""
Hello {booking.customer_name},

Your vehicle {booking.vehicle.brand}
must be returned today ({today}).

Please return the vehicle on time.

Thank you,
RentalHub Team
            """,
            from_email="nestfinder9@gmail.com",
            recipient_list=[booking.user.email],
            fail_silently=False,
        )

    print("Reminder emails processed successfully")


def cancel_booking(request, id):

    booking = Booking.objects.get(id=id)

    if booking.booking_status == "Paid":

        booking.booking_status = "Cancellation Requested"

    elif booking.booking_status in ["Pending", "Accepted"]:

        booking.booking_status = "Cancelled"

        vehicle = booking.vehicle
        vehicle.is_available = True
        vehicle.save()

    booking.save()

    return redirect('profile')

def delete_booking(request, id):

    booking = Booking.objects.get(id=id)

    booking.delete()

    return redirect('profile')


import razorpay
from django.shortcuts import redirect
from django.http import HttpResponse

def approve_refund(request, id):

    booking = Booking.objects.get(id=id)

    try:

        # Razorpay Client
        client = razorpay.Client(
            auth=(
                "YOUR_KEY_ID",
                "YOUR_KEY_SECRET"
            )
        )

        # Razorpay Refund API
        refund = client.payment.refund(
            booking.razorpay_payment_id,
            {
                "amount": int(booking.total_price * 100)
            }
        )

        booking.booking_status = "Refunded"

        vehicle = booking.vehicle
        vehicle.is_available = True

        vehicle.save()
        booking.save()

        return redirect('admin_dashboard')

    except Exception as e:

        return HttpResponse(
            f"Refund Failed: {str(e)}"
        )
    


def make_vehicle_available(request, id):

    vehicle = veh_listing.objects.get(id=id)

    vehicle.is_available = True
    vehicle.save()

    return redirect('admin_vehicles')


def make_vehicle_unavailable(request, id):

    vehicle = veh_listing.objects.get(id=id)

    vehicle.is_available = False
    vehicle.save()

    return redirect('admin_vehicles')


def refund_pay(request, id, booking_id):

    booking = Booking.objects.get(id=booking_id)

    amount = booking.total_price * 100

    return render(
        request,
        "refund_pay.html",
        {
            'r': amount,
            'booking_id': booking_id,
            'booking': booking,

            
        }
    )



def show_review(request):
    return render(request, 'review.html')

def add_review(request):
    if request.method == "POST":

        user = User.objects.get(
            email=request.session['u_id']
        )

        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        Review.objects.create(
            user=user,
            rating=rating,
            comment=comment
        )

        return redirect('/')# Redirect to the profile page after submitting the review
def contact_show(request):
    return render(request, 'contact.html')
def contact_admin(request):
    if request.method == "POST":

        email = request.session['u_id']

        user = User.objects.get(email=email)

        Contact.objects.create(
            name=user.name,
            email=user.email,
            subject=request.POST.get('subject'),
            message=request.POST.get('message')
        )

        return render(request, 'contact.html', {
            'message_sent': True,
            'user': user
        })

    email = request.session['u_id']
    user = User.objects.get(email=email)

    return render(request, 'contact.html', {
        'user': user
    })


from .models import Contact

def admin_messages(request):

    if 'a_id' not in request.session:
        return render(request, "index.html", {
            "error": "You must be logged in as admin to view this page."
        })

    contacts = Contact.objects.all().order_by('-id')

    return render(request, "admin_messages.html", {
        "contacts": contacts
    })

from django.shortcuts import render, get_object_or_404

def reply_message(request, id):

    contact = Contact.objects.get(id=id)

    if request.method == "POST":

        contact.reply = request.POST['reply']
        contact.save()

        return redirect('admin_messages')

    return render(request, "reply_messages.html", {
        "contact": contact
    })

def view_review(request):
    reviews = Review.objects.all().order_by('-id')
    return render(request, 'view_review.html', {'reviews': reviews})


import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .models import login

def forgot_password(request):

    if request.method == "POST":

        email = request.POST["email"]

        if login.objects.filter(email=email).exists():

            otp = random.randint(100000,999999)

            request.session["otp"] = str(otp)
            request.session["email"] = email

            send_mail(
                "RentalHub Password Reset",
                f"Your OTP is {otp}",
                "yourgmail@gmail.com",
                [email],
                fail_silently=False,
            )

            return redirect("verify_otp")

        else:

            return render(request,"forgot_password.html",{
                "error":"Email not registered"
            })

    return render(request,"forgot_password.html")


def verify_otp(request):

    if request.method=="POST":

        user_otp=request.POST["otp"]

        if user_otp==request.session.get("otp"):

            return redirect("reset_password")

        else:

            return render(request,"verify_otp.html",{
                "error":"Invalid OTP"
            })

    return render(request,"verify_otp.html")


def reset_password(request):

    if request.method=="POST":

        password=request.POST["password"]
        confirm=request.POST["confirm"]

        if password!=confirm:

            return render(request,"reset_password.html",{
                "error":"Passwords do not match"
            })

        email=request.session.get("email")
        print("Email from session:", email)

        user=login.objects.get(email=email)

        user.password=password
        user.save()

        del request.session["otp"]
        del request.session["email"]

        return redirect("/",{
            "success":"Password changed successfully",
            # "reviews": Review.objects.all().order_by('-id')
        })

    return render(request,"reset_password.html")


from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages

from .models import veh_listing


def send_warning(request, vehicle_id):

    vehicle = get_object_or_404(veh_listing, id=vehicle_id)

    if request.method == "POST":

        title = request.POST.get("title")
        complaint = request.POST.get("complaint")

        owner = vehicle.owner

        subject = f"Warning: {title}"

        message = f"""
Dear {owner.name},

A customer has submitted a complaint regarding your vehicle.

Vehicle Details
-------------------------
Brand : {vehicle.brand}
Number Plate : {vehicle.number_plate}
Location : {vehicle.location}

Complaint
-------------------------
{complaint}

Please resolve this issue as soon as possible.

Failure to resolve repeated complaints may result in suspension or permanent removal of your vehicle listing.

If you believe this complaint is incorrect, please contact RentalHub Support.

Regards,

RentalHub Admin Team
"""

        send_mail(
            subject,
            message,
            "yourgmail@gmail.com",
            [owner.email],
            fail_silently=False,
        )

        messages.success(request, "Warning email sent successfully.")

        return redirect("admin_vehicles")

    return render(request, "warning_form.html", {
        "vehicle": vehicle
    })