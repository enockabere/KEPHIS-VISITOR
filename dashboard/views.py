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

            serviceRequired = config.O_DATA.format(f"QYServicerequired")
            serviceResponse = self.get_object(serviceRequired)
            
            meeting_services = [service for service in serviceResponse['value'] if service['Service_Requred_Code']=='1']
            accom_services = [service for service in serviceResponse['value'] if service['Service_Requred_Code']=='2']

        except ValueError as e:
            print (e)
            messages.error(request,e)
            return redirect('ListingDetail',pk=pk)

        ctx = {
            "clientType":clientType,"typeOfService":typeOfService
            ,"availableRooms":roomOutput,"meeting_services":meeting_services,
            "accom_services":accom_services,
            }
        return render(request,"listingDetail.html",ctx)
    def post(self,request,pk):
        if request.method == "POST":
            try:
                ServiceRequired = request.POST.get('ServiceRequired')
                TypeOfRoom = request.POST.get('TypeOfRoom')
                NumberOfPeople = request.POST.get('NumberOfPeople')
                startDate = request.POST.get('startDate')
                typeOfClient = int(request.session['clientType'])
                startTime = request.POST.get('startTime')
                endTime = request.POST.get('endTime')


                request.session['ServiceRequired'] = ServiceRequired
                request.session['TypeOfRoom'] = TypeOfRoom
                request.session['NumberOfPeople'] = NumberOfPeople
                request.session['startDate'] = startDate
                request.session['startTime'] = startTime
                request.session['endTime'] = endTime

                noOfRooms = int(NumberOfPeople)
                
                response = config.CLIENT.service.FnMeetingFees(
                    TypeOfRoom,typeOfClient,ServiceRequired,noOfRooms)
                mp = jsons.dumps(response,use_decimal=True)
                return JsonResponse(mp,safe=False)
            except Exception as e:
                print (e)
                messages.error(request,e)
                return redirect("ListingDetail",pk=pk)

class AccomodationForm(UserObjectMixin,View):
    def post(self, request,pk):
        if request.method == 'POST':
            try:
                ServiceRequired = request.POST.get('ServiceRequired')
                numberOfRooms = request.POST.get('NumberOfPeople')
                startDate = request.POST.get('startDate')
                endDate = request.POST.get('endDate')
                typeOfClient = int(request.session['clientType'])


                request.session['accom_ServiceRequired'] = ServiceRequired
                request.session['NumberOfRooms'] = numberOfRooms
                request.session['accom_startDate'] = startDate
                request.session['accom_endDate'] = endDate              

                    
                noOfRooms = int(numberOfRooms)

                response = config.CLIENT.service.FnAccomodationFees(typeOfClient,ServiceRequired,noOfRooms)
                print(response)
                mp = jsons.dumps(response,use_decimal=True)
                return JsonResponse(mp,safe=False)
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

class  MakeReservation(UserObjectMixin,View):
    def post(self, request,pk):
        if request.method == 'POST':
            try:
                clientType = request.session['clientType']

                if pk == '1':
                    TypeOfRoom = request.session['TypeOfRoom'] 
                    ServiceRequired = request.session['ServiceRequired']
                    startDate = request.session['startDate'] 
                    startTime = request.session['startTime']
                    endTime = request.session['endTime'] 
                    NumberOfPeople = request.session['NumberOfPeople'] 
                    messages.success(request,"Success. Please login or sign up to continue.")
                    return redirect('login') 

                if pk == '2':

                    ServiceRequired = request.session['accom_ServiceRequired']
                    NumberOfRooms = request.session['NumberOfRooms'] 
                    startDate = request.session['accom_startDate']
                    endDate = request.session['accom_endDate']
  
                    messages.success(request,"Success. Please login or sign up to continue.")
                    return redirect('login') 

                if pk == '3':
                    TypeOfRoom = request.session['TypeOfRoom'] 
                    ServiceRequired = request.session['ServiceRequired']
                    startDate = request.session['startDate'] 
                    startTime = request.session['startTime']
                    endTime = request.session['endTime'] 
                    NumberOfPeople = request.session['NumberOfPeople'] 
                    ServiceRequired = request.session['accom_ServiceRequired']
                    NumberOfRooms = request.session['NumberOfRooms'] 
                    startDate = request.session['accom_startDate']
                    endDate = request.session['accom_endDate']

                    messages.success(request,"Success. Please login or sign up to continue.")
                    return redirect('login') 
                
            except Exception as e:
                print(e)
                messages.error(request, f"{e} missing, please fill general information form and add a booking line.")
                return redirect("ListingDetail",pk=pk)
        return redirect("ListingDetail",pk=pk)


class CancelReservation(View):
    def post(self,request,pk):
        try:
            del request.session['clientType']
            del request.session['typeOfService']

            if pk == '1':
                del request.session['TypeOfRoom'] 
                del request.session['ServiceRequired']
                del request.session['startDate'] 
                del request.session['startTime']
                del request.session['endTime'] 
                del request.session['NumberOfPeople'] 
                messages.error(request,"Reservation Cancelled successfully")
                return redirect('dashboard') 

            if pk == '2':

                del request.session['accom_ServiceRequired']
                del request.session['NumberOfRooms'] 
                del request.session['accom_startDate']
                del request.session['accom_endDate']
                messages.error(request,"Reservation Cancelled successfully")
                return redirect('dashboard')
            if pk == '3':
                del request.session['TypeOfRoom'] 
                del request.session['ServiceRequired']
                del request.session['startDate'] 
                del request.session['startTime']
                del request.session['endTime'] 
                del request.session['NumberOfPeople'] 
                del request.session['accom_ServiceRequired']
                del request.session['NumberOfRooms'] 
                del request.session['accom_startDate']
                del request.session['accom_endDate']
                messages.error(request,"Reservation Cancelled successfully")
                return redirect('dashboard')
        except Exception as e:
            print (e)
            messages.error(request,e)
            return redirect('ListingDetail',pk=pk)

