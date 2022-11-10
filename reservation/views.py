from django.shortcuts import render,redirect
from django.contrib import messages
from django.views import View
from myRequest.views import UserObjectMixin

# Create your views here.
class Reservations(UserObjectMixin,View):
    def get(self, request):
        try:
            customerName = request.session['CustomerName']
            customerEmail = request.session['customerEmail']
            idNumber = request.session['customerIDNumber'] 
            phoneNumber = request.session['customerPhone']
            userID =  request.session['UserID']

            open_reservation_count = '0'

            reservations = self.double_filtered_data('QYvisitors',"User_Code",userID,'Booking_Status','Open')

            open_reservation_count = reservations[0]
            open_reservations = reservations[1]

        except Exception as e:
            print(e)
            messages.error(request,e)
        ctx = {
            "customerName":customerName,"customerEmail":customerEmail,
            "idNumber":idNumber,"phoneNumber":phoneNumber,
            "open_reservation_count":open_reservation_count,"open_reservations":open_reservations
        }
        return render(request,"reserve.html",ctx)
class BookingGateway(View):
    def get(self,request,pk):
        return render(request,"bookingGateway.html")
        
class BookingDetails(View):
    def get(self,request,pk):
        return render(request,"bookingDetails.html")