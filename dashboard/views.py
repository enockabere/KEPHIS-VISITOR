from django.shortcuts import render,redirect
from django.views import View
from django.contrib import messages
import requests
from django.conf import settings as config
from django.http import JsonResponse

# Create your views here.
class UserObjectMixin(object):
    model =None
    session = requests.Session()
    session.auth = config.AUTHS
    def get_object(self,endpoint):
        response = self.session.get(endpoint, timeout=10).json()
        return response

class Dashboard(View):
    def get(self,request):
        return render(request,"dashboard.html")
    def post(self,request):
        if request.method == "POST":
            try:
                bookingType = request.POST.get('bookingType')
                clientType = request.POST.get('clientType')
                numberOfPeople = request.POST.get('numberOfPeople')
                typeOfService = request.POST.get('typeOfService')
                serviceRequired = request.POST.get('serviceRequired')
                roomType = request.POST.get('roomType')
                startDate = request.POST.get('startDate')
                endDate = request.POST.get('endDate')
                numberOfAdults = request.POST.get('numberOfAdults')
                numberOfChildren = request.POST.get('numberOfChildren')
                
                try:
                    request.session['endDate'] = endDate
                    request.session['roomType'] = roomType
                    request.session['startDate'] = startDate
                    request.session['clientType'] = clientType
                    request.session['bookingType'] = bookingType
                    request.session['typeOfService'] = typeOfService
                    request.session['numberOfPeople'] = numberOfPeople
                    request.session['numberOfAdults'] = numberOfAdults
                    request.session['serviceRequired'] = serviceRequired
                    request.session['numberOfChildren'] = numberOfChildren
                    messages.success(request,"Success")
                    print("Success")
                    return redirect('ListingDetail')
                except  Exception as e:
                    print (e)
                    messages.error(request,e)
                    return redirect('dashboard')
            except  Exception as e:
                messages.error(request,e)
                return redirect('dashboard')
class ListingDetail(View):
    def get(self,request):
        try:
            endDate = request.session['endDate'] 
            roomType = request.session['roomType'] 
            startDate = request.session['startDate']
            clientType = request.session['clientType']
            typeOfService = request.session['typeOfService']
            numberOfPeople = request.session['numberOfPeople']
            numberOfAdults = request.session['numberOfAdults']
            serviceRequired = request.session['serviceRequired']
            numberOfChildren = request.session['numberOfChildren']
        except ValueError as e:
            print (e)
            messages.error(request,e)
            return redirect('ListingDetail')

        ctx = {
            "endDate":endDate,"roomType":roomType,
            "startDate":startDate,"clientType":clientType,
            "typeOfService":typeOfService,"numberOfPeople":numberOfPeople,
            "numberOfAdults":numberOfAdults,"serviceRequired":serviceRequired,
            "numberOfChildren":numberOfChildren
            }
        return render(request,"listingDetail.html",ctx)
    def post(self, request):
        if request.method == "POST":
            try:
                room = request.POST.get('room')
                try:
                    request.session['room'] = room
                    messages.success(request,"Sign in or Register to Continue.")
                    return redirect('login')
                except Exception as e:
                    print (e)
                    messages.error(request,e)
                    return redirect("ListingDetail")
            except Exception as e:
                print (e)
                messages.error(request,e)
                return redirect("ListingDetail")

class serviceRequired(UserObjectMixin,View):
    def get(self, request):
        Service = config.O_DATA.format("QYServicerequired")
        try:
            serviceResponse = self.get_object(Service)
            return JsonResponse(serviceResponse)

        except  Exception as e:
            print(e)
            return redirect('dashboard')

class CancelReservation(View):
    def post(self,request):
        try:
            del request.session['endDate'] 
            del request.session['roomType'] 
            del request.session['startDate']
            del request.session['clientType']
            del request.session['bookingType']
            del request.session['typeOfService']
            del request.session['numberOfPeople']
            del request.session['numberOfAdults']
            del request.session['serviceRequired']
            del request.session['numberOfChildren']
            messages.info(request,"Reservation Cancelled successfully")
            return redirect('dashboard')
        except Exception as e:
            print (e)
            messages.error(request,e)
            return redirect('ListingDetail')

