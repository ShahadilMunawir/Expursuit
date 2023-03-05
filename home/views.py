from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from .models import Expense
from login_register.models import User
from matplotlib import pyplot as plt

# Create your views here.

def home_view(request: WSGIRequest):
    from login_register.views import login_view
    if "userId" in request.session:
        user = User.objects.filter(id=request.session["userId"]).values()[0]
        expense = Expense.objects.filter(userId=request.session["userId"]).values()
        index = len(Expense.objects.all())
        total_spending = 0
        spending = 0
        for spend in expense:
            spending += int(spend["amount"])
            total_spending += int(spend["amount"])
        budget = int(user["budget"])
        percentage = int((total_spending/budget)*100)

        slices = []
        labels = []
        categories = {}
        for spend in expense:
            if spend["category"] not in categories:
                categories[spend["category"]] = len(spend["category"])
                slices.append((str(categories[spend["category"]])))
                labels.append(spend["category"])
            else:
                categories[spend["category"]] += len(spend["category"])

        plt.style.use("fivethirtyeight")
        plt.rcParams.update({'text.color': "white", 'axes.labelcolor': "white"})
        plt.title("Analytics")
        plt.tight_layout()
        plt.pie(slices, labels=labels, wedgeprops={"edgecolor": "black"}, autopct="%1.1f%%")
        plt.savefig("/home/shahadil/Desktop/Expursuit/static/images/piecharts/fig.png", transparent=True)

        if request.method == "POST":
            filter = request.POST["filter"]
            if filter == "all":
                expense = Expense.objects.filter(userId=request.session["userId"]).values()
            else:
                expense = Expense.objects.filter(userId=request.session["userId"], category=filter).values()
            index = len(expense)
            print(index)
            filter_spend = 0
            for spend in expense:
                filter_spend += int(spend["amount"])
            budget_amount = total_spending
            total_spending = filter_spend
        else:
            budget_amount = total_spending
        context = {
            "name": user["fullname"],
            "spending": total_spending,
            "budget": budget,
            "percentage": percentage,
            "table_data": expense,
            "total_amount": spending,
            "budget_amount": budget_amount
        }
    else:
        return redirect(login_view)
    return render(request, 'home.html', context=context)


def add_expense_view(request: WSGIRequest):
    from login_register.views import login_view

    if "userId" not in request.session:
        return redirect(login_view)

    if request.method == "POST":
        category = request.POST["category"]
        amount = request.POST["amount"]
        paymentMethod = request.POST["payment-method"]
        date = request.POST["date"]
        description = request.POST["description"]

        expense = Expense(userId=request.session["userId"], category=category, amount=amount, paymentType=paymentMethod, date=date, description=description)
        expense.save()
        print("DATA SAVE IS A GO :@)")
        
        print(category, amount, paymentMethod, date, description)
        return redirect(home_view)
    else:
        return render(request, "add_expense.html", {})
    
def profile_view(request: WSGIRequest):
    from login_register.views import login_view
    if "userId" not in request.session:
        return redirect(login_view)
    else:
        user = User.objects.filter(id=request.session["userId"]).values()[0]
        context = {
            "name": user["fullname"],
            "username": user["username"],
            "email": user["email"],
            "budget": user["budget"]
        }
        return render(request, "profile.html", context)
    
def update_profile_view(request: WSGIRequest):
    from login_register.views import login_view
    if "userId" not in request.session:
        return redirect(login_view)
    
    if request.method == "POST":
        fullname = request.POST["fullname"]
        username = request.POST["username"]
        email = request.POST["email"]
        budget = request.POST["budget"]

        user = User.objects.get(id=request.session["userId"])
        user.fullname = fullname
        user.username = username
        user.email = email
        user.budget = budget
        user.save()

    user = User.objects.filter(id=request.session["userId"]).values()[0]
    context = {
        "fullname": user["fullname"],
        "username": user["username"],
        "email": user["email"],
        "budget": user["budget"]
    }
    return render(request, "update.html", context)