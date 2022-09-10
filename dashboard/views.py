from django.shortcuts import render,redirect
from django.views import View
from django.contrib import messages

# Create your views here.
class Dashboard(View):
    def get(self,request):
        return render(request,"dashboard.html")
    def post(self,request):
        if request.method == "POST":
            try:
                clientType = request.POST.get('clientType')
                contactName = request.POST.get('contactName')
                idNumber = request.POST.get('idNumber')
                phoneNumber = request.POST.get('phoneNumber')
                email = request.POST.get('email')
                numberOfPeople = request.POST.get('numberOfPeople')
                typeOfService = request.POST.get('typeOfService')
                serviceRequired = request.POST.get('serviceRequired')
                roomType = request.POST.get('roomType')
                startDate = request.POST.get('startDate')
                endDate = request.POST.get('endDate')
                numberOfAdults = request.POST.get('numberOfAdults')
                numberOfChildren = request.POST.get('numberOfChildren')
                
                try:
                    request.session['email'] = email
                    request.session['endDate'] = endDate
                    request.session['idNumber'] = idNumber
                    request.session['roomType'] = roomType
                    request.session['startDate'] = startDate
                    request.session['clientType'] = clientType
                    request.session['contactName'] = contactName
                    request.session['phoneNumber'] = phoneNumber
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
            email =  request.session['email'] 
            endDate = request.session['endDate'] 
            idNumber = request.session['idNumber']
            roomType = request.session['roomType'] 
            startDate = request.session['startDate']
            clientType = request.session['clientType']
            contactName = request.session['contactName']
            phoneNumber = request.session['phoneNumber']
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
            "email":email,"endDate":endDate,
            "idNumber":idNumber,"roomType":roomType,
            "startDate":startDate,"clientType":clientType,
            "contactName":contactName,"phoneNumber":phoneNumber,
            "typeOfService":typeOfService,"numberOfPeople":numberOfPeople,
            "numberOfAdults":numberOfAdults,"serviceRequired":serviceRequired,
            "numberOfChildren":numberOfChildren
            }
        return render(request,"listingDetail.html",ctx)

class CancelReservation(View):
    def post(self,request):
        try:
            del request.session['email'] 
            del request.session['endDate'] 
            del request.session['idNumber']
            del request.session['roomType'] 
            del request.session['startDate']
            del request.session['clientType']
            del request.session['contactName']
            del request.session['phoneNumber']
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