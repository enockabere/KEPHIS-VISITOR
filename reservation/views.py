from django.shortcuts import render,redirect
from django.contrib import messages
from django.views import View
from myRequest.views import UserObjectMixin
from django.conf import settings as config
import requests

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

            reservations = self.double_filtered_data(
                'QYvisitors',"User_Code","eq",userID,"and",
                'Booking_Status', "eq", 'Open'
                )

            # open_reservation_count = reservations[0]
            open_reservations = reservations[1]

            open_reservation_count = len(open_reservations)

            ctx = {
                "customerName":customerName,"customerEmail":customerEmail,
                "idNumber":idNumber,"phoneNumber":phoneNumber,
                "open_reservation_count":open_reservation_count,"open_reservations":open_reservations
            }
        except KeyError as e:
            print(e)
            messages.error(request,"Session ended. Login to continue.")
            return redirect("login")
        except Exception as e:
            print(e)
            messages.error(request,e)
        return render(request,"reserve.html",ctx)
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
            "accomodation_lines":accomodation_lines,
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
        
class BookingDetails(View):
    def get(self,request,pk):
        return render(request,"bookingDetails.html")