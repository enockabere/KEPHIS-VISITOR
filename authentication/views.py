from django.shortcuts import render,redirect
from django.views import View
from django.contrib import messages

# Create your views here.
class Login(View):
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
                messages.success(request,f"Welcome, {email}. See Reservations below.")
                return redirect('reserve')
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
                customerName = request.POST.get('yourName')
                idNumber = request.POST.get('idNumber')
                phoneNumber = request.POST.get('phoneNumber')
                email = request.POST.get('email')
                password = request.POST.get('password')
                password2 = request.POST.get('password2')

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
                
                request.session['customerName'] =customerName
                request.session['customerEmail'] =email
                request.session['customerIDNumber'] =idNumber
                request.session['customerPhone'] =phoneNumber
                messages.success(request,'We sent you an email to verify your account')
                return redirect("login")
            except Exception as e:
                print(e)
                messages.error(request,e)
                return redirect("register")

