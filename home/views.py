import os
import logging
from .models import Expense
from datetime import datetime
from django.db.models import Q
from redmail import EmailSender
from django.contrib import messages
from matplotlib import pyplot as plt
from login_register.models import User
from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename="log.log"
                    )

# Create your views here.
def home_view(request: WSGIRequest):
    from login_register.views import login_view
    if "userId" in request.session:
        dates = Expense.objects.filter(userId=request.session["userId"])
        days = []
        months = []
        years = []
        for date in dates:
            day = date.date.strftime("%d")
            month = date.date.strftime("%m")
            year = date.date.strftime("%Y")
            
            if day not in days:
                days.append(day)

            if month not in months:
                months.append(month)

            if year not in years:
                years.append(year)


        now = datetime.now()
        logging.info(now.month)
        user = User.objects.filter(id=request.session["userId"]).values()[0]
        # expense = Expense.objects.filter(userId=request.session["userId"]).filter(Q(dateTime__month=now.day) & Q(dateTime__year=now.year))
        expense = Expense.objects.filter(userId=request.session["userId"]).filter(Q(dateTime__month=now.month)).values()
        logging.info(Expense.objects.filter(userId=request.session["userId"]).filter(Q(dateTime__day=now.day)).values())

        if request.method == "POST" and "date-filter" in request.POST:
            day = request.POST["day"]
            month = request.POST["month"]
            year = request.POST["year"]

            if day == '':
                expense = Expense.objects.filter(userId=request.session["userId"]).filter(Q(dateTime__month=month) & Q(dateTime__year=year)).values()
            else:
                expense = Expense.objects.filter(userId=request.session["userId"]).filter(Q(dateTime__day=day) & Q(dateTime__month=month) & Q(dateTime__year=year)).values()
            
        index = len(Expense.objects.all())
        total_spending = 0
        spending = 0
        for spend in expense:
            spending += int(spend["amount"])
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
        plt.savefig("../Expursuit/static/images/piecharts/fig.png", transparent=True)

        if request.method == "POST" and "category-filter" in request.POST:
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

        if request.session["showLimitAlert"]:
            if percentage > 90:
                messages.warning(request, f"You have used {percentage}% of your budget")

                email = EmailSender(
                    host="smtp.gmail.com", 
                    port=587,
                    username=os.environ.get("EXPURSUIT_SENDER_EMAIL"),
                    password=os.environ.get("EXPURSUIT_APP_PASSWORD")
                    )
                email.send(
                    subject="Limit Exceeded",
                    sender="shahadilmunawir110@gmail.com",
                    receivers=[user["email"]],
                    html="""
                        <center>
                            <h1>Expurusit</h1>
                            {{ my_image }}
                            <p>You have used """ + str(percentage) + """% of your budget</p>
                        </center>
                    """,
                    body_images={
                        'my_image': '/home/shahadil/Desktop/Expursuit/static/images/piecharts/fig.png',
                    }
                )
                request.session["showLimitAlert"] = False

        context = {
            "name": user["fullName"],
            "spending": total_spending,
            "budget": budget,
            "percentage": percentage,
            "table_data": expense,
            "total_amount": spending,
            "budget_amount": budget_amount,
            "days": days,
            "months": months,
            "years": years,
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

        dateObj = datetime.strptime(date, "%Y-%m-%d").date()
        timeObj = datetime.now().time()
        dateTime = datetime.combine(dateObj, timeObj)

        expense = Expense(userId=request.session["userId"], category=category, amount=amount, paymentType=paymentMethod, date=dateObj, time=timeObj, dateTime=dateTime, description=description)
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
            "name": user["fullName"],
            "username": user["username"],
            "email": user["email"],
            "budget": user["budget"],
            "profilePicture": user["profilePicture"]
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
        user.fullName = fullname
        user.username = username
        user.email = email
        user.budget = budget
        user.save()

    user = User.objects.filter(id=request.session["userId"]).values()[0]
    context = {
        "fullname": user["fullName"],
        "username": user["username"],
        "email": user["email"],
        "budget": user["budget"]
    }
    return render(request, "update.html", context)