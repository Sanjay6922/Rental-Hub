"""
URL configuration for rental project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user_app import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.profile, name='index'),
    path('home', views.new_index, name='home'),
    path('userreg', views.user_show, name='userreg'),
    path('register_user', views.user_registration),
    # path('login', views.login_show, name='login'),
    path('log', views.login_fun, name='log'),
    path('veh', views.veh_add_show),
    path('listing', views.veh_add, name='listing'),
    path('logout', views.logout, name='logout'),
    path('vehicles', views.vehicle_list, name='vehicle_list'),
    path('vehicle-details/<int:id>/',views.vehicle_details, name='vehicle_details'),
    path('book-vehicle/<int:id>/', views.book_vehicle, name='book_vehicle'),
    path('profile/',views.profile_view,name='profile'),
    path('vehicle-edit/<int:id>/',views.vehicle_edit,name='vehicle-edit'),
    path('vehicle-update/<int:id>/',views.vehicle_update),
    path('accept-booking/<int:id>/',views.accept_booking,name='accept_booking'),
    path('reject-booking/<int:id>/',views.reject_booking,name='reject_booking'),
    path('payment-summary/<int:id>/',views.payment_summary,name='payment_summary'),
    path( 'pay/<int:id>/<int:booking_id>', views.pay, name='pay'),
    path('success/<int:booking_id>', views.after_payment, name='after_payment'),
    path('payment_details/<int:booking_id>', views.payment_details, name='payment_details'),
    path('delete/<int:id>',views.vehicle_delete,name='delete'),
    path('admin-dashboard',views.admin_dashboard,name='admin_dashboard'),
    path( 'admin-dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('admin-users/',views.admin_users,name='admin_users'),
    path('admin-vehicles/',views.admin_vehicles, name='admin_vehicles'),
    path( 'delete-vehicle-admin/<int:id>/', views.delete_vehicle_admin, name='delete_vehicle_admin'),
    path('admin-bookings/',views.admin_bookings,name='admin_bookings'),
    path('admin-payments/',views.admin_payments,name='admin_payments'),
    path('admin-verifications/',views.admin_verifications,name='admin_verifications'),
    path('admin-logout/',views.admin_logout,name='admin_logout'),
    path( 'return-vehicle/<int:id>/', views.return_vehicle,name='return_vehicle'),
    path('confirm-return/<int:id>/',views.confirm_return,name='confirm_return'),
    path('send-return-reminders/', views.send_return_reminders),
    path('cancel-booking/<int:id>/', views.cancel_booking, name='cancel_booking'),
    path('delete-booking/<int:id>/', views.delete_booking, name='delete_booking'),
    path('approve-refund/<int:id>/',views.approve_refund,name='approve_refund'),
    path('vehicle-available/<int:id>/', views.make_vehicle_available, name='vehicle_available'),
    path('vehicle-unavailable/<int:id>/', views.make_vehicle_unavailable, name='vehicle_unavailable'),
    path('refund-pay/<int:id>/<int:booking_id>/', views.refund_pay, name='refund_pay'),
    path('review/', views.show_review),
    path('add_review/', views.add_review, name='add_review'),
    path('contact/', views.contact_admin, ),
    path('contact-show/', views.contact_show, ),
    path('admin-messages/', views.admin_messages, name='admin_messages'),
    path('reply-message/<int:id>/', views.reply_message, name='reply_message'),
    path('approve-vehicle/<int:id>/', views.approve_vehicle, name='approve_vehicle'),
    path('reject-vehicle/<int:id>/', views.reject_vehicle, name='reject_vehicle'),
    path('view-review/', views.view_review, name='view_review'),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),
    path("reset-password/", views.reset_password, name="reset_password"),
    path("admin-dashboard/warning/<int:vehicle_id>/",views.send_warning,name="send_warning",)

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)