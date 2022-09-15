from django.shortcuts import render,redirect
from django.contrib import messages
from django.views import View

# Create your views here.
class Reservations(View):
    def get(self, request):
        try:
            customerName = request.session['customerName'] 
            customerEmail = request.session['customerEmail']
            idNumber = request.session['customerIDNumber'] 
            phoneNumber = request.session['customerPhone']
        except Exception as e:
            print(e)
            messages.error(request,e)
        ctx = {
            "customerName":customerName,"customerEmail":customerEmail,
            "idNumber":idNumber,"phoneNumber":phoneNumber,
        }
        return render(request,"reserve.html",ctx)
class BookingGateway(View):
    def get(self,request,pk):
        return render(request,"bookingGateway.html")
        
class BookingDetails(View):
    def get(self,request,pk):
        return render(request,"bookingDetails.html")