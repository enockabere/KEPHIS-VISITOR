from django.shortcuts import render

# Create your views here.

def profileRequest(request):
    return render(request,'profile.html')
def contact(request):
    return render(request,'contact.html')

def FAQRequest(request):
    return render(request,'faq.html')