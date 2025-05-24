from django.shortcuts import render, redirect
from .forms import ServiceForm
from .models import Service

# def createService(request):
#     form = ServiceForm()

#     if request.method == 'POST':
#         form = ServiceForm(request.POST)
#         if form.is_valid():
#             service.save()
#             return redirect('homepage')

def home_view(request):
    return render(request, 'services/home.html')
    
def displayServices(request):
    services = Service.objects.all()
    context = {"services": services}
    return render(request, "services/services.html", context)


def getService(request, pk):
    service = Service.objects.get(name=pk)
    context = {"service": service}
    return render(request, "services/single-service.html", context)

def locations(request):
    return render(request, 'services/locations.html')

def whowe_view(request):
    return render(request, 'services/whowe.html')

# def updateService(request):
#     form = ServiceForm()

#     if request.method == 'POST':
#         form = ServiceForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('services')

#     context = {'form': form}
#     return render(request, 'services/service-form.html', context)


# def deleteService(request, pk):
#     service = Service.objects.get(id=pk)
#     if request.method == 'POST':
#         service.delete()
#         messages.success(request, 'Service deleted successfully!')
#         return redirect('services')

#     context = {'object': service}
#     return render(request, 'delete_template.html', context)

def calculate_estimate(request):
    services = Service.objects.all()
    estimated_price = 0.0

    if request.method == 'POST':
        selected_ids = request.POST.getlist('services')
        selected_services = Service.objects.filter(id__in=selected_ids)
        estimated_price = sum(service.price for service in selected_services)

    context = {
        'services': services,
        'estimated_price': estimated_price,
    }
    return render(request, 'services/estimate_form.html', context)
