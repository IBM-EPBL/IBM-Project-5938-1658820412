from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Stock


def redirector(request):
    return redirect("/home")


def home(request):
    if request.user.is_authenticated:
        try:
            Latest_Added_Stock = Stock.objects.order_by('-Recently_Updated')[0]
        except:
            Latest_Added_Stock = None
        return render(request, 'Inventory_Management_For_Retailers/home.html', {'Last_Stock': Latest_Added_Stock})
    return render(request, 'Inventory_Management_For_Retailers/home.html', dict())


def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                print('Authenticated')
                return redirect("/")
            else:
                return render(request, 'Inventory_Management_For_Retailers/login.html',
                              {"error_message": "Invalid Credentials"})
        else:
            return render(request, 'Inventory_Management_For_Retailers/login.html', dict())
    # return HttpResponse("This is a Login Page")


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        password1 = request.POST['password']
        password2 = request.POST['password_repeat']
        if User.objects.filter(username=username).exists():
            return render(request, "Inventory_Management_For_Retailers/register.html",
                          {'error_message': "User already Exists"})
        elif password1 != password2:
            return render(request, "Inventory_Management_For_Retailers/register.html",
                          {'error_message': "Password Mismatched"})
        else:
            user = User.objects.create_user(username=username, password=password1, first_name=first_name,
                                            last_name=last_name)
            user.save()
            return redirect("/")
    else:
        return render(request, template_name="Inventory_Management_For_Retailers/register.html")


def logout(request):
    auth.logout(request)
    return redirect('/')


def addStock(request):
    if not request.user.is_authenticated:
        return redirect("/login", error_message="You've not Logged In!")
    if User.is_authenticated:
        if request.method == 'POST':
            product_name = request.POST['product_name']
            No_of_Stocks = request.POST['no_of_stocks']
            Price = request.POST['price']
            Tax = request.POST['tax']
            New_Stock = Stock(Product_Name=product_name, No_of_stocks=No_of_Stocks, Date_Added=timezone.now(),
                              Recently_Updated=timezone.now(), Price=Price, Tax=Tax)
            New_Stock.save()
            # redirect(reverse('Inventory_Management_For_Retailers:home', kwargs={'stock_data':"Stock Added Succesfully"}))
            # return HttpResponseRedirect(reverse('Inventory_Management_For_Retailers:results', args=(question.id,)))
            return redirect("/", {'stock_data': "Stock Added Succesfully"})
            # return render(request,'Inventory_Management_For_Retailers/home.html',{'stock_data':"Stock Added Succesfully"})
        return render(request, 'Inventory_Management_For_Retailers/addStock.html', dict())


def removeStock(request):
    if not request.user.is_authenticated:
        return redirect("/login", error_message="You've not Logged In!")
    if request.method == 'POST':
        try:
            Selected_Stock_id = request.POST['stock']
            Selected_No_Of_Stocks = int(request.POST['Quantity'])
            # selected_stock=Stock.get(Product_Name="stock")
        except:
            Stocks = Stock.objects.all()
            return render(request, "Inventory_Management_For_Retailers/removeStock.html",
                          {'Stocks': Stocks, 'error': "select a Stock"})
        else:
            Stock_To_Be_Removed = Stock.objects.get(id=Selected_Stock_id)
            Stocks = Stock.objects.all()
            if Selected_No_Of_Stocks < 0:
                return render(request, "Inventory_Management_For_Retailers/removeStock.html", {'error_message': "Enter a Positive Value!", 'Stocks': Stocks})
            Available_Stocks = Stock_To_Be_Removed.No_of_stocks
            if Stock_To_Be_Removed.No_of_stocks < Selected_No_Of_Stocks:
                return render(request, "Inventory_Management_For_Retailers/removeStock.html", {
                    'error_message': "The Available No of Stocks for " + Stock_To_Be_Removed.Product_Name + " " + str(
                        Available_Stocks), 'Stocks': Stocks})
            else:
                Stock_To_Be_Removed.No_of_stocks -= Selected_No_Of_Stocks
                Stock_To_Be_Removed.save()
                if Stock_To_Be_Removed.No_of_stocks == 0:
                    Stock_To_Be_Removed.delete()
                return redirect('/')
    Stocks = Stock.objects.all()
    return render(request, "Inventory_Management_For_Retailers/removeStock.html", {'Stocks': Stocks})


def viewstock(request):
    if not request.user.is_authenticated:
        return redirect("/login", error_message="You've not Logged In!")
    else:
        Stocks = Stock.objects.all()
        return render(request, "Inventory_Management_For_Retailers/viewStock.html", {"Stocks": Stocks})


def editStock(request):
    if not request.user.is_authenticated:
        return redirect("/login", error_message="You've not Logged In!")
    else:
        Stocks = Stock.objects.all()
        return render(request, "Inventory_Management_For_Retailers/editStock.html", {"Stocks": Stocks})
