from django.shortcuts import render

from .models import Stock


def home(request):
    if request.user.is_authenticated:
        try:
            Latest_Added_Stock = Stock.objects.order_by('-Recently_Updated')[0]
        except:
            Latest_Added_Stock = None
        if Latest_Added_Stock is None:
            return render(request, 'Inventory_Management_For_Retailers/home.html', dict())
        else:
            return render(request, 'Inventory_Management_For_Retailers/home.html', {'Last_Stock': Latest_Added_Stock})
    return render(request, 'Inventory_Management_For_Retailers/home.html', dict())
