from django.shortcuts import render,redirect
from django.views import View
from django.contrib import messages

# Create your views here.
class Login(View):
    def get(self, request):
        if request.method == 'POST':
            try:
                email = request.POST.get('email')
                password = request.POST.get('password')

                if not email:
                    messages.error(request,"Email Missing")
                    return redirect("Login")
                if not password:
                    messages.error(request,"Password Missing")
                    return redirect("Login")
                messages.success(request,f"Welcome, {email}. See Reservations below.")
                return redirect('reservation')
            except Exception as e:
                print(e)
                messages.error(request,e)
                return redirect("Login")
        return render(request,'login.html')

class Register(View):
    def get(self, request):
        return render(request,"register.html")