from django.shortcuts import render,redirect
from django.views import View
from django.contrib import messages
import requests
from django.conf import settings as config
from django.http import JsonResponse
import simplejson as jsons
from datetime import datetime

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

            Access_Point = config.O_DATA.format("QyRoomBookingSetUp?$filter=Booked%20eq%20false")
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
                typeOfClient = int(request.session['clientType'])
                noOfPeople = int(NumberOfPeople)
                startTime = request.POST.get('startTime')
                endTime = request.POST.get('endTime')

                if not TypeOfAccommodation:
                    TypeOfAccommodation = "None"

                request.session['ServiceRequired'] = ServiceRequired
                request.session['TypeOfRoom'] = TypeOfRoom
                request.session['NumberOfPeople'] = NumberOfPeople
                request.session['startDate'] = startDate

    
                if request.session['typeOfService'] == '1':

                    request.session['startTime'] = startTime
                    request.session['endTime'] = endTime

                    response = config.CLIENT.service.FnMeetingFees(TypeOfRoom,typeOfClient,ServiceRequired,noOfPeople)
                    mp = jsons.dumps(response,use_decimal=True)
                    return JsonResponse(mp,safe=False)

                if request.session['typeOfService'] == '2':

                    request.session['endDate'] = endDate

                    response = config.CLIENT.service.FnAccomodationFees(typeOfClient,ServiceRequired,noOfPeople)
                    print(response)
                    mp = jsons.dumps(response,use_decimal=True)
                    return JsonResponse(mp,safe=False)

                messages.success(request,"Success. Please login or sign up to continue.")
                return redirect('login')
            except Exception as e:
                print (e)
                messages.error(request,e)
                return redirect("ListingDetail",pk=pk)


class availableRoom(UserObjectMixin,View):
    def get(self, request):
        RoomCode = request.GET.get('RoomCode')
        subProduct = config.O_DATA.format(f"QyRoomBookingSetUp?$filter=Code%20eq%20%27{RoomCode}%27")
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

def makeReservation(request,pk):
    if request.method == 'POST':
        try:
            clientType = request.session['clientType']
            typeOfService = request.session['typeOfService']
            if typeOfService == '1':
                TypeOfRoom = request.session['TypeOfRoom'] 
                ServiceRequired = request.session['ServiceRequired']
                startDate = request.session['startDate'] 
                startTime = request.session['startTime']
                endTime = request.session['endTime'] 
                NumberOfPeople = request.session['NumberOfPeople'] 
                messages.success(request,"Success. Please login or sign up to continue.")
                return redirect('login') 
            if typeOfService == '2':
                ServiceRequired = request.session['ServiceRequired']
                NumberOfPeople = request.session['NumberOfPeople']
                startDate = request.session['startDate']
                endDate = request.session['endDate']
                messages.success(request,"Success. Please login or sign up to continue.")
                return redirect('login') 
            if typeOfService == '3':
                messages.error(request, "Setup sessions for meeting room and accomodation")
                return redirect("ListingDetail",pk=pk)
            
        except Exception as e:
            print(e)
            messages.error(request, f"{e} missing, please fill general information form and add a booking line.")
            return redirect("ListingDetail",pk=pk)
    return redirect("ListingDetail",pk=pk)


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

