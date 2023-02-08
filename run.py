# try:
#                                 clientType = request.session['clientType']
#                                 typeOfService = request.session['typeOfService']
#                                 if clientType and typeOfService:
                                    
#                                     if BookingHeaderResponse:
#                                         bookingNo = BookingHeaderResponse
#                                         if request.session['typeOfService'] == '1':
#                                             ServiceRequired = request.session['ServiceRequired']
#                                             startDate = datetime.strptime(request.session['startDate'], '%Y-%m-%d').date()
#                                             startTime = datetime.strptime(request.session['startTime'], '%H:%M').time()
#                                             endTime = datetime.strptime(request.session['endTime'], '%H:%M').time()
#                                             TypeOfRoom = request.session['TypeOfRoom']
#                                             NumberOfPeople = request.session['NumberOfPeople'] 
#                                             NumberOfDays = request.session['NumberOfDays']
                                            
#                                             BookingLineResponse = self.zeep_client().service.FnRoomBookingLine(
#                                                 bookingNo,TypeOfRoom,'0',myAction,userCode,ServiceRequired,
#                                                 startDate,startTime,endTime,NumberOfPeople,NumberOfDays)
#                                             if BookingLineResponse == True:
#                                                 request.session.flush()
#                                                 messages.success(request,f"Welcome, {email}. See Reservations below.")
#                                                 return redirect('reserve')
#                                         if request.session['typeOfService'] == '2':
#                                             accom_service = request.session['accom_ServiceRequired']
#                                             NumberOfRooms = request.session['NumberOfRooms'] 
#                                             accom_startDate = datetime.strptime(request.session['accom_startDate'], '%Y-%m-%d').date()
#                                             accom_endDate = datetime.strptime(request.session['accom_endDate'], '%Y-%m-%d').date()
#                                             AccomodationLineResponse = self.zeep_client().service.FnAccomodationBookingLine(
#                                                 bookingNo,myAction,userCode,accom_service,NumberOfRooms,
#                                                 "0",accom_startDate,accom_endDate)
#                                             if AccomodationLineResponse == True:
#                                                 request.session.flush()
#                                                 messages.success(request,f"Welcome, {email}. See Reservations below.")
#                                                 return redirect('reserve')   
#                                         if request.session['typeOfService'] == '3':
#                                             ServiceRequired = request.session['ServiceRequired']
#                                             startDate = datetime.strptime(request.session['startDate'], '%Y-%m-%d').date()
#                                             startTime = datetime.strptime(request.session['startTime'], '%H:%M').time()
#                                             endTime = datetime.strptime(request.session['endTime'], '%H:%M').time()
#                                             TypeOfRoom = request.session['TypeOfRoom']
#                                             NumberOfPeople = request.session['NumberOfPeople']
#                                             NumberOfDays = request.session['NumberOfDays']
#                                             BookingLineResponse = self.zeep_client().service.FnRoomBookingLine(
#                                                 bookingNo,TypeOfRoom,'0',myAction,userCode,ServiceRequired,
#                                                 startDate,startTime,endTime,NumberOfPeople,NumberOfDays)
#                                             if BookingLineResponse == True:
#                                                 accom_service = request.session['accom_ServiceRequired']
#                                                 NumberOfRooms = request.session['NumberOfRooms'] 
#                                                 accom_startDate = datetime.strptime(request.session['accom_startDate'], '%Y-%m-%d').date()
#                                                 accom_endDate = datetime.strptime(request.session['accom_endDate'], '%Y-%m-%d').date()
#                                                 AccomodationLineResponse = self.zeep_client().service.FnAccomodationBookingLine(
#                                                     bookingNo,myAction,userCode,accom_service,NumberOfRooms,
#                                                     "0",accom_startDate,accom_endDate)
#                                                 if AccomodationLineResponse == True:
#                                                     request.session.flush()
#                                                     messages.success(request,f"Welcome, {email}. See Reservations below.")
#                                                     return redirect('reserve')
#                                                 messages.error(request, "Accomodation Details not added, contact admin.")
#                                                 return redirect('login')
#                                             messages.error(request, "Meeting Room Details not added, contact admin.")
#                                             return redirect('login')
#                             except KeyError as e:
#                                 print(e)
                                


