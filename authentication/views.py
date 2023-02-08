import logging
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views import View
from django.contrib import messages
import secrets
import string
from cryptography.fernet import Fernet
import base64
from django.conf import settings as config
from django.contrib.sites.shortcuts import get_current_site
from  django.template.loader import render_to_string
from django.core.mail import EmailMessage
import threading
import requests
from datetime import  datetime
from myRequest.views import UserObjectMixin,one_filter_method



class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

def send_mail(emailAddress,verificationToken,request):
    current_site = get_current_site(request)
    email_subject = 'Activate Your Account'
    email_body = render_to_string('activate.html',{
        'domain': current_site,
        'Secret': verificationToken,
    })

    email = EmailMessage(subject=email_subject,body=email_body,
    from_email=config.EMAIL_HOST_USER,to=[emailAddress])

    EmailThread(email).start()

class Login(UserObjectMixin,View):
    def get(self, request):
        return render(request,'login.html')
    def post(self,request):
        if request.method == 'POST':
            try:
                email = request.POST.get('email')
                password = request.POST.get('password')

                if not email:
                    messages.error(request,"Email Missing")
                    return redirect("login")
                if not password:
                    messages.error(request,"Password Missing")
                    return redirect("login")
                CustomerResponse = self.one_filter("QyVisitorsLogins","EmailAddress","eq",email)
                for applicant in CustomerResponse[1]:
                    if applicant['Verified']==True:
                        if self.pass_decrypt(applicant['MyPassword']) == password:
                            request.session['CustomerName'] = applicant['ContactName']
                            request.session['customerEmail'] = applicant['EmailAddress']
                            request.session['customerIDNumber'] = applicant['IdNoKraPin']
                            request.session['customerPhone'] = applicant['BookedByPhoneNo']
                            request.session['UserID'] = applicant['No'] 
                            header_sessions = [
                                'clientType',
                                'typeOfService',
                                'disabled',
                                'explainDisability',
                                'organization',
                                'payment_method'
                            ]
                            for session in header_sessions:
                                if session not in request.session:
                                    request.session['CustomerName'] = applicant['ContactName']
                                    request.session['customerEmail'] = applicant['EmailAddress']
                                    request.session['customerIDNumber'] = applicant['IdNoKraPin']
                                    request.session['customerPhone'] = applicant['BookedByPhoneNo']
                                    request.session['UserID'] = applicant['No'] 
                                    messages.success(request,f"Welcome, {email}. See Reservations below.")
                                    return redirect('reserve')
                            bookingNo = ''
                            myAction = 'insert'
                            typeOfService = int(request.session['typeOfService'])
                            clientType = int(request.session['clientType'])
                            userCode = applicant['No'] 
                            disabled = request.session['disabled']
                            explainDisability = request.session['explainDisability']
                            organization = request.session['organization']
                            payment_method = int(request.session['payment_method'])
                            try:
                                BookingHeaderResponse = self.zeep_client().service.FnVisitorsCard(
                                        bookingNo,myAction,typeOfService,clientType,userCode,disabled,
                                        explainDisability,organization,payment_method)
                                if BookingHeaderResponse !='0':
                                    del request.session['clientType']
                                    del request.session['disabled']
                                    del request.session['explainDisability']
                                    del request.session['organization']
                                    del request.session['payment_method']
                                    meeting_room_sessions =[
                                            'ServiceRequired',
                                            'startDate',
                                            'startTime',
                                            'endTime',
                                            'TypeOfRoom',
                                            'NumberOfPeople',
                                            'NumberOfDays'
                                        ]
                                    if typeOfService == 1:
                                        for session in meeting_room_sessions:
                                            if session not in request.session:
                                                messages.info(request,f"Welcome, {email}. Meeting room lines not added")
                                                return redirect('reserve')
                                        ServiceRequired = request.session['ServiceRequired']
                                        startDate = datetime.strptime(request.session['startDate'], '%Y-%m-%d').date()
                                        startTime = datetime.strptime(request.session['startTime'], '%H:%M').time()
                                        endTime = datetime.strptime(request.session['endTime'], '%H:%M').time()
                                        TypeOfRoom = request.session['TypeOfRoom']
                                        NumberOfPeople = request.session['NumberOfPeople'] 
                                        NumberOfDays = request.session['NumberOfDays']
                                        BookingLineResponse = self.zeep_client().service.FnRoomBookingLine(
                                                    BookingHeaderResponse,TypeOfRoom,'0',myAction,userCode,
                                                    ServiceRequired,startDate,startTime,endTime,
                                                    NumberOfPeople,NumberOfDays)
                                        del request.session['typeOfService']
                                        del request.session['ServiceRequired']
                                        del request.session['startDate']
                                        del request.session['startTime']
                                        del request.session['endTime']
                                        del request.session['TypeOfRoom']
                                        del request.session['NumberOfPeople']
                                        del request.session['NumberOfDays']
                                        if BookingLineResponse == True:
                                            messages.success(request,f"Welcome, {email}. See Reservations below.")
                                            return redirect('reserve')
                                        messages.info(request,f"Welcome, {email}. Meeting room lines not added")
                                        return redirect('reserve')
                                    elif typeOfService == 2:
                                        accom_sessions = [
                                            'accom_ServiceRequired',
                                            'NumberOfRooms',
                                            'accom_startDate',
                                            'accom_endDate',                                            
                                        ]
                                        for session in accom_sessions:
                                            if session not in request.session:
                                                messages.info(request,f"Welcome, {email}. Accomodation lines not added")
                                                return redirect('reserve')
                                        accom_service = request.session['accom_ServiceRequired']
                                        NumberOfRooms = request.session['NumberOfRooms'] 
                                        accom_startDate = datetime.strptime(request.session['accom_startDate'], '%Y-%m-%d').date()
                                        accom_endDate = datetime.strptime(request.session['accom_endDate'], '%Y-%m-%d').date()
                                        AccomodationLineResponse = self.zeep_client().service.FnAccomodationBookingLine(
                                                bookingNo,myAction,userCode,accom_service,NumberOfRooms,
                                                "0",accom_startDate,accom_endDate)
                                        del request.session['typeOfService']
                                        del request.session['accom_ServiceRequired']
                                        del request.session['NumberOfRooms']
                                        del request.session['accom_startDate']
                                        del request.session['accom_endDate']
                                        if AccomodationLineResponse == True:
                                            messages.success(request,f"Welcome, {email}. See Reservations below.")
                                            return redirect('reserve')
                                        messages.info(request,f"Welcome, {email}. Accomodation lines not added")
                                        return redirect('reserve')    
                                    else:
                                        messages.success(request,f'Welcome, {email}. Add reservation lines to booking{BookingHeaderResponse}')
                                        return redirect('reserve')
                            except Exception as e:
                                logging.exception(e)
                                messages.info('Reservation not created, try to create from your dashboard')
                                return redirect('dashboard')
                            return redirect('login')
                        messages.error(request, "Invalid Password.")
                        return redirect('login')                             
                    messages.error(request, "Your email is not verified.")
                    return redirect('login')
                messages.error(request,"Email not registered, please sign up/user another email to continue")
                return redirect('login')
            except Exception as e:
                print(e)
                messages.error(request,e)
                return redirect("login")
class Register(View):
    def get(self, request):
        return render(request,"register.html")
    def post(self,request):
        if request.method == 'POST':
            try:
                loginNo = ''
                customerName = request.POST.get('yourName')
                idNumber = request.POST.get('idNumber')
                phoneNumber = request.POST.get('phoneNumber')
                email = request.POST.get('email')
                password = request.POST.get('password')
                password2 = request.POST.get('password2')
                myAction = 'insert'

                if not customerName:
                    messages.error(request,"Contact Name Missing")
                    return redirect("register")
                if not email:
                    messages.error(request,"Email Missing")
                    return redirect("register")
                if not idNumber:
                    messages.error(request,"ID Number Missing")
                    return redirect("register")
                if not phoneNumber:
                    messages.error(request,"Phone Number Missing")
                    return redirect("register")
                if not password and password2:
                    messages.error(request,"Password Missing")
                    return redirect("register")
                if password != password2:
                    messages.error(request,"Password Mismatch")
                    return redirect("register")
                
                nameChars = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                        for i in range(5))
                
                verificationToken = str(nameChars)
            
                cipher_suite = Fernet(config.ENCRYPT_KEY)
                
                encrypted_text = cipher_suite.encrypt(password.encode('ascii'))
                myPassword = base64.urlsafe_b64encode(encrypted_text).decode("ascii")

                print(myPassword)

                response = config.CLIENT.service.VisitorSignup(loginNo, customerName, email,idNumber,
                phoneNumber,myPassword,verificationToken, myAction)

                if response == True:
                    send_mail(email,verificationToken,request)
                    messages.success(request, 'We sent you an email to verify your account')
                    return redirect('login')
            except Exception as e:
                print(e)
                messages.error(request,e)
                return redirect("register")

class  verifyRequest(UserObjectMixin,View):
    def get(self,request):
        return render(request,"verify.html")
    def post(self, request):
        if request.method == 'POST':
            try:
                email = request.POST.get('email')
                secret = request.POST.get('secret')
                verified = True
                Access_Point = config.O_DATA.format(f"/QyVisitorsLogins?$filter=EmailAddress%20eq%20%27{email}%27")
                response = self.get_object(Access_Point)
                for res in response['value']:
                    if res['VerificationToken'] == secret:
                        response = config.CLIENT.service.FnVerified(verified,email)
                        messages.success(request,"Verification Successful")
                        return redirect('login')
                    messages.success(request,"Wrong Secret Code")
                    return redirect('verifyRequest')
                messages.success(request,"Email not registered")
                return redirect('register')
            except requests.exceptions.RequestException as e:
                print(e)
                messages.error(request,e)
                return redirect('verifyRequest')
        return redirect('verifyRequest')

def check_id(request):
    idNumber = request.POST.get('idNumber')
    get_user_id =one_filter_method("/QyVisitorsLogins",'IdNoKraPin','eq',idNumber)
    if get_user_id[0]==0:
        return HttpResponse("<span class='error-success'>ID number is available</span>")
    return HttpResponse("<span class='error-error'>ID number already exits</span>")
    
def check_email(request):
    email = request.POST.get('email')
    get_user_email =one_filter_method("/QyVisitorsLogins",'EmailAddress','eq',email)
    if get_user_email[0]==0:
        return HttpResponse("<span class='error-success'>Email is available</span>")
    return HttpResponse("<span class='error-error'>Email already exits</span>")
