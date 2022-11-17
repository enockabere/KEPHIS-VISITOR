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

# Create your views here.
class UserObjectMixin(object):
    model =None
    session = requests.Session()
    session.auth = config.AUTHS
    def get_object(self,endpoint):
        response = self.session.get(endpoint, timeout=10).json()
        return response

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
def passwordCipher(password):
    Portal_Password = base64.urlsafe_b64decode(password)
    cipher_suite = Fernet(config.ENCRYPT_KEY)
    decoded_text = cipher_suite.decrypt(Portal_Password).decode("ascii")
    return decoded_text

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

                Customer = config.O_DATA.format(f"QyVisitorsLogins?$filter=EmailAddress%20eq%20%27{email}%27")
                CustomerResponse = self.get_object(Customer)

                for applicant in CustomerResponse['value']:
                    if applicant['Verified']==True:
                        decoded_text = passwordCipher(applicant['MyPassword'])
                        if decoded_text == password:
                            request.session['CustomerName'] = applicant['ContactName']
                            request.session['customerEmail'] = applicant['EmailAddress']
                            request.session['customerIDNumber'] = applicant['IdNoKraPin']
                            request.session['customerPhone'] = applicant['BookedByPhoneNo']
                            request.session['UserID'] = applicant['No']

                            try:
                                clientType = request.session['clientType']
                                typeOfService = request.session['typeOfService']

                                print("type of service:",request.session['typeOfService'])

                                if clientType and typeOfService:
                                    bookingNo = ''
                                    myAction = 'insert'
                                    typeOfBooking = int(typeOfService)
                                    typeOfClient = int(clientType)
                                    userCode = request.session['UserID']

                                    BookingHeaderResponse = config.CLIENT.service.FnVisitorsCard(
                                        bookingNo,myAction,typeOfBooking,typeOfClient,userCode)

                                    if BookingHeaderResponse:
                                        bookingNo = BookingHeaderResponse
                                        
                                        if request.session['typeOfService'] == '1':
                                            ServiceRequired = request.session['ServiceRequired']
                                            startDate = datetime.strptime(request.session['startDate'], '%Y-%m-%d').date()
                                            startTime = datetime.strptime(request.session['startTime'], '%H:%M').time()
                                            endTime = datetime.strptime(request.session['endTime'], '%H:%M').time()
                                            TypeOfRoom = request.session['TypeOfRoom']
                                            NumberOfPeople = request.session['NumberOfPeople'] 

                                            BookingLineResponse = config.CLIENT.service.FnRoomBookingLine(
                                                bookingNo,TypeOfRoom,'0',myAction,userCode,ServiceRequired,
                                                startDate,startTime,endTime,NumberOfPeople)

                                            if BookingLineResponse == True:
                                                del request.session['clientType']
                                                del request.session['typeOfService']
                                                del request.session['ServiceRequired']
                                                del request.session['TypeOfRoom']
                                                del request.session['startTime']
                                                del request.session['NumberOfPeople'] 
                                                del request.session['startDate'] 
                                                del request.session['endTime'] 
                                                messages.success(request,f"Welcome, {email}. See Reservations below.")
                                                return redirect('reserve')
                                        if request.session['typeOfService'] == '2':
                                            accom_service = request.session['accom_ServiceRequired']
                                            NumberOfRooms = request.session['NumberOfRooms'] 
                                            accom_startDate = datetime.strptime(request.session['accom_startDate'], '%Y-%m-%d').date()
                                            accom_endDate = datetime.strptime(request.session['accom_endDate'], '%Y-%m-%d').date()
                                            AccomodationLineResponse = config.CLIENT.service.FnAccomodationBookingLine(
                                                bookingNo,myAction,userCode,accom_service,NumberOfRooms,
                                                "0",accom_startDate,accom_endDate)

                                            if AccomodationLineResponse == True:
                                                del request.session['clientType']
                                                del request.session['typeOfService']
                                                del request.session['accom_service']
                                                del request.session['NumberOfRooms'] 
                                                del request.session['accom_startDate'] 
                                                del request.session['accom_endDate'] 
                                                messages.success(request,f"Welcome, {email}. See Reservations below.")
                                                return redirect('reserve')

                                        if request.session['typeOfService'] == '3':
                                            ServiceRequired = request.session['ServiceRequired']
                                            startDate = datetime.strptime(request.session['startDate'], '%Y-%m-%d').date()
                                            startTime = datetime.strptime(request.session['startTime'], '%H:%M').time()
                                            endTime = datetime.strptime(request.session['endTime'], '%H:%M').time()
                                            TypeOfRoom = request.session['TypeOfRoom']
                                            NumberOfPeople = request.session['NumberOfPeople'] 

                                            BookingLineResponse = config.CLIENT.service.FnRoomBookingLine(
                                                bookingNo,TypeOfRoom,'0',myAction,userCode,ServiceRequired,
                                                startDate,startTime,endTime,NumberOfPeople)

                                            if BookingLineResponse == True:
                                                accom_service = request.session['accom_ServiceRequired']
                                                NumberOfRooms = request.session['NumberOfRooms'] 
                                                accom_startDate = datetime.strptime(request.session['accom_startDate'], '%Y-%m-%d').date()
                                                accom_endDate = datetime.strptime(request.session['accom_endDate'], '%Y-%m-%d').date()
                                                AccomodationLineResponse = config.CLIENT.service.FnAccomodationBookingLine(
                                                    bookingNo,myAction,userCode,accom_service,NumberOfRooms,
                                                    "0",accom_startDate,accom_endDate)
                                                if AccomodationLineResponse == True:
                                                    del request.session['clientType']
                                                    del request.session['typeOfService']
                                                    del request.session['ServiceRequired']
                                                    del request.session['TypeOfRoom']
                                                    del request.session['startTime']
                                                    del request.session['NumberOfPeople'] 
                                                    del request.session['startDate'] 
                                                    del request.session['endTime']
                                                    del request.session['accom_service']
                                                    del request.session['NumberOfRooms'] 
                                                    del request.session['accom_startDate'] 
                                                    del request.session['accom_endDate'] 
                                                    messages.success(request,f"Welcome, {email}. See Reservations below.")
                                                    return redirect('reserve')
                                                messages.error(request, "Accomodation Details not added, contact admin.")
                                                return redirect('login')
                                            messages.error(request, "Meeting Room Details not added, contact admin.")
                                            return redirect('login')
                            except KeyError as e:
                                print(e)
                                messages.success(request,f"Welcome, {email}. See Reservations below.")
                                return redirect('reserve')                          
                        messages.error(request, "Invalid Credentials. Please reset your password else create a new account")
                        return redirect('login')
                    messages.error(request, "Your email is not verified.")
                    return redirect('login')
                messages.error(
                request, "Invalid Credentials.")
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
                        print("response:",response)
                        messages.success(request,"Verification Successful")
                        return redirect('login')
            except requests.exceptions.RequestException as e:
                print(e)
                messages.error(request,e)
                return redirect('verifyRequest')
        return redirect('verifyRequest')
