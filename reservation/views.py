from django.shortcuts import render,redirect
from django.contrib import messages
from django.urls import reverse
from django.views import View
from myRequest.views import UserObjectMixin
from django.conf import settings as config
import requests
from datetime import datetime

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

            reservations = self.one_filter(
                'QYvisitors',"User_Code","eq",userID)

            open_reservations = [x for x in reservations[1] if x['Booking_Status'] == 'Open']
            open_reservation_count = len(open_reservations)

            booked_reservations = [x for x in reservations[1] if x['Booking_Status'] == 'Fully Booked']
            booked_reservation_count = len(booked_reservations)

            Cancel_reservations = [x for x in reservations[1] if x['Booking_Status'] == 'Cancel']
            Cancel_reservation_count = len(Cancel_reservations)

            ctx = {
                "customerName":customerName,"customerEmail":customerEmail,
                "idNumber":idNumber,"phoneNumber":phoneNumber,
                "open_reservation_count":open_reservation_count,"open_reservations":open_reservations,
                "booked_reservation_count":booked_reservation_count,"booked_reservations":booked_reservations,
                "Cancel_reservations":Cancel_reservations,"Cancel_reservation_count":Cancel_reservation_count
            }
        except KeyError as e:
            print(e)
            messages.error(request,"Session ended. Login to continue.")
            return redirect("login")
        except Exception as e:
            print(e)
            messages.error(request,e)
        return render(request,"reserve.html",ctx)
    def post(self, request):
        if request.method == "POST":
            try:
                bookingNo = request.POST.get('bookingNo')
                myAction = request.POST.get('myAction')
                typeOfService = int(request.POST.get('typeOfService'))
                typeOfClient = int(request.POST.get('clientType'))
                userCode = request.session['UserID']

                BookingHeaderResponse = config.CLIENT.service.FnVisitorsCard(
                                        bookingNo,myAction,typeOfService,typeOfClient,userCode)
                if BookingHeaderResponse:
                    messages.success(request,"Success, add booking details")
                    return redirect("BookingGateway",pk=BookingHeaderResponse)
                messages.success(request,"Failed")
                return redirect("reserve")
            except requests.exceptions.HTTPError as err:
                print(err)
                messages.error(request, f"Request Error Code: {err}")
                return redirect('reserve')
            except KeyError as e:
                print(e)
                messages.error(request,"Session ended. Login to continue.")
                return redirect("login")
            except Exception as e:
                print(e)
                messages.info(request, e)
                return redirect('reserve')
        return redirect('reserve')


class BookingGateway(UserObjectMixin,View):
    def get(self,request,pk): 
        try:
            userID =  request.session['UserID']
            response = self.double_filtered_data(
                'QYvisitors',"No_","eq",pk,"and",
                'User_Code', "eq", userID
                )
            for x in response[1]:
                reservation = x
            meeting_room_lines_response = self.double_filtered_data(
                'QyRoomBookingLines',"RoomNo","eq",pk,"and",
                'UserCode', "eq", userID
                )
            meeting_room_lines = meeting_room_lines_response[1]
            accomodation_lines_response = self.double_filtered_data(
                'QyAccommodationBookingLines',"RoomNo","eq",pk,"and",
                'UserCode', "eq", userID
                )
            accomodation_lines = accomodation_lines_response[1]

            Access_Point = config.O_DATA.format("QyRoomBookingSetUp?$filter=Booked%20eq%20false")
            roomResponse = self.get_object(Access_Point)
            roomOutput = [room for room in roomResponse['value']]

            serviceRequired = config.O_DATA.format(f"QYServicerequired")
            serviceResponse = self.get_object(serviceRequired)
            meeting_services = [service for service in serviceResponse['value'] if service['Service_Requred_Code']=='1']
            accom_services = [service for service in serviceResponse['value'] if service['Service_Requred_Code']=='2']

        except requests.exceptions.HTTPError as err:
            print(err)
            messages.error(request, f"Request Error Code: {err}")
            return redirect('reserve')
        except KeyError as e:
            print(e)
            messages.error(request,"Session ended. Login to continue.")
            return redirect("login")
        except Exception as e:
            print(e)
            messages.error(request,e)
            return redirect('reserve')
        ctx = {
            "reservation":reservation,"meeting_room_lines":meeting_room_lines,
            "accomodation_lines":accomodation_lines,"availableRooms":roomOutput,
            "meeting_services":meeting_services,"accom_services":accom_services,
            }
        return render(request,"bookingGateway.html",ctx)
    def post(self,request,pk):
        if request.method == "POST":
            try:
                bookingNo = request.POST.get('bookingNo')
                myAction = request.POST.get('myAction')
                typeOfBooking = int(request.POST.get('typeOfService'))
                typeOfClient = int(request.POST.get('clientType'))
                userCode = request.session['UserID']
                BookingHeaderResponse = config.CLIENT.service.FnVisitorsCard(
                                        bookingNo,myAction,typeOfBooking,typeOfClient,userCode)

                if BookingHeaderResponse:
                    messages.success(request,"Success")
                    return redirect('BookingGateway', pk=bookingNo)
                messages.error(request,f"False.{BookingHeaderResponse}")
                return redirect('BookingGateway', pk=bookingNo)
            except requests.exceptions.HTTPError as err:
                print(err)
                messages.error(request, f"Request Error Code: {err}")
                return redirect('reserve')
            except KeyError as e:
                print(e)
                messages.error(request,"Session ended. Login to continue.")
                return redirect("login")
            except Exception as e:
                print(e)
                messages.info(request, e)
                return redirect('reserve')
        return redirect('BookingGateway',pk=pk)

class MeetingDetails(UserObjectMixin,View):
    def post(self, request,pk):
        if request.method == 'POST':
            try:
                bookingNo = request.POST.get('bookingNo')
                lineNo = request.POST.get('lineNo')
                ServiceRequired = request.POST.get('ServiceRequired')
                TypeOfRoom = request.POST.get('TypeOfRoom')
                NumberOfPeople = int(request.POST.get('NumberOfPeople'))
                startDate = datetime.strptime(request.POST.get('startDate'), '%Y-%m-%d').date()
                startTime = datetime.strptime(request.POST.get('startTime'), '%H:%M').time()
                endTime = datetime.strptime(request.POST.get('endTime'), '%H:%M').time()
                myAction = request.POST.get('myAction')
                userCode = request.session['UserID']

                BookingLineResponse = config.CLIENT.service.FnRoomBookingLine(
                                                bookingNo,TypeOfRoom,lineNo,myAction,userCode,ServiceRequired,
                                                startDate,startTime,endTime,NumberOfPeople)

                if BookingLineResponse == True:
                    messages.success(request,"Success")
                    return redirect('BookingGateway',pk=pk)
                messages.error(request,"Failed")
                return redirect('BookingGateway',pk=pk)

            except requests.exceptions.HTTPError as err:
                print(err)
                messages.error(request, f"Request Error Code: {err}")
                return redirect('BookingGateway',pk=pk)
            except KeyError as e:
                print(e)
                messages.error(request,"Session ended. Login to continue.")
                return redirect("login")
            except Exception as e:
                print(e)
                messages.info(request, e)
                return redirect('BookingGateway',pk=pk)
        return redirect('BookingGateway',pk=pk)

class AccomodationDetails(UserObjectMixin,View):
    def post(self, request,pk):
        if request.method == 'POST':
            try:
                lineNo = request.POST.get('lineNo')
                ServiceRequired = request.POST.get('ServiceRequired')
                NumberOfRooms = int(request.POST.get('NumberOfRooms'))
                startDate = datetime.strptime(request.POST.get('startDate'), '%Y-%m-%d').date()
                endDate = datetime.strptime(request.POST.get('endDate'), '%Y-%m-%d').date()
                myAction = request.POST.get('myAction')
                userCode = request.session['UserID']

                AccomodationLineResponse = config.CLIENT.service.FnAccomodationBookingLine(
                                                pk,myAction,userCode,ServiceRequired,NumberOfRooms,
                                                lineNo,startDate,endDate)

                if AccomodationLineResponse == True:
                    messages.success(request,"Success")
                    return redirect('BookingGateway',pk=pk)
                messages.error(request,"Failed")
                return redirect('BookingGateway',pk=pk)

            except requests.exceptions.HTTPError as err:
                print(err)
                messages.error(request, f"Request Error Code: {err}")
                return redirect('BookingGateway',pk=pk)
            except KeyError as e:
                print(e)
                messages.error(request,"Session ended. Login to continue.")
                return redirect("login")
            except Exception as e:
                print(e)
                messages.info(request, e)
                return redirect('BookingGateway',pk=pk)
        return redirect('BookingGateway',pk=pk)

class Pay(UserObjectMixin,View):
    def post(self,request,pk):
        if request.method == 'POST':
            try:
                phone_number = request.POST.get('phone_number')
                amount = 1
                account_reference = request.POST.get('account_reference')
                transaction_desc = 'Description'

                messages.error(request,"Payment integration to be active once an SSL is installed")
                return redirect('BookingGateway',pk=pk)
                # callback_url = request.build_absolute_uri(reverse('mpesa_stk_push_callback'))
                # response = self.lipa_na_mpesa(amount,phone_number,callback_url,account_reference, transaction_desc)
            except Exception as e:
                print(e)
                messages.info(request, e)
                return redirect('BookingGateway',pk=pk)
        return redirect('BookingGateway',pk=pk)

class Confirm(UserObjectMixin,View):
    def get(self,request,pk):
        return render(request,"confirm.html")

class BookingDetails(View):
    def get(self,request,pk):
        return render(request,"bookingDetails.html")
