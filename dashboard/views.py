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

                clientType = request.POST.get('clientType')
                typeOfService = request.POST.get('typeOfService')
               
                try:
                    request.session['clientType'] = clientType
                    request.session['typeOfService'] = typeOfService

                    messages.success(request,"Success")
                    print("Success")
                    return redirect('ListingDetail',pk=request.session['typeOfService'])
                except  Exception as e:
                    print (e)
                    messages.error(request,e)
                    return redirect('dashboard')
            except  Exception as e:
                messages.error(request,e)
                return redirect('dashboard')
class ListingDetail(UserObjectMixin,View):
    def get(self,request,pk):
        try:

            clientType = request.session['clientType']
            typeOfService = request.session['typeOfService']

            Access_Point = config.O_DATA.format("QYRooms?$filter=Booked%20eq%20false%20and%20Reserved%20eq%20false")
            roomResponse = self.get_object(Access_Point)
            roomOutput = [room for room in roomResponse['value']]

            serviceRequired = config.O_DATA.format(f"QYServicerequired?$filter=Service_Requred_Code%20eq%20%27{pk}%27")
            serviceResponse = self.get_object(serviceRequired)
            serviceOutput = [service for service in serviceResponse['value']]

        except ValueError as e:
            print (e)
            messages.error(request,e)
            return redirect('ListingDetail',pk=pk)

        ctx = {
            "clientType":clientType,"typeOfService":typeOfService
            ,"availableRooms":roomOutput,"serviceOutput":serviceOutput,
            }
        return render(request,"listingDetail.html",ctx)
    def post(self,request,pk):
        if request.method == "POST":
            try:
                ServiceRequired = request.POST.get('ServiceRequired')
                TypeOfRoom = request.POST.get('TypeOfRoom')
                TypeOfAccommodation = request.POST.get('TypeOfAccommodation')
                NumberOfPeople = request.POST.get('NumberOfPeople')
                startDate = request.POST.get('startDate')
                endDate = request.POST.get('endDate')

                request.session['ServiceRequired'] = ServiceRequired
                request.session['TypeOfRoom'] = TypeOfRoom
                request.session['TypeOfAccommodation'] = TypeOfAccommodation
                request.session['NumberOfPeople'] = NumberOfPeople
                request.session['startDate'] = startDate
                request.session['endDate'] = endDate
                messages.success(request,"Added Successfully.")
                return redirect('ListingDetail',pk=pk)

            except Exception as e:
                print (e)
                messages.error(request,e)
                return redirect("ListingDetail",pk=pk)

class submitReservation(UserObjectMixin,View):
    def post(self, request,pk):
        try:
            clientType = request.session['clientType']
            typeOfService = request.session['typeOfService']
            ServiceRequired = request.session['ServiceRequired']
            TypeOfRoom = request.session['TypeOfRoom'] 
            TypeOfAccommodation = request.session['TypeOfAccommodation'] 
            NumberOfPeople = request.session['NumberOfPeople']
            startDate = request.session['startDate']
            endDate = request.session['endDate'] 
            messages.success(request,"Success. Please login or sign up to continue.")
            return redirect('login')
        except Exception as e:
            print (e)
            messages.error(request,"Please add booking line(s)")
            return redirect('ListingDetail',pk=pk)


class availableRoom(UserObjectMixin,View):
    def get(self, request):
        RoomCode = request.GET.get('RoomCode')
        subProduct = config.O_DATA.format(f"QYRooms?$filter=Code%20eq%20%27{RoomCode}%27")
        try:
            roomResponse = self.get_object(subProduct)
            return JsonResponse(roomResponse)
        except  Exception as e:
            print(e)
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

            del request.session['clientType']
            del request.session['typeOfService']
            messages.error(request,"Reservation Cancelled successfully")
            return redirect('dashboard')
        except Exception as e:
            print (e)
            messages.error(request,e)
            return redirect('ListingDetail')

