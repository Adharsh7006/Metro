import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# Create your views here.
from metro_app.forms import BatchForm, DietplanForm, EquipmentsForm, LoginForm, PhysicianForm, TrainerForm, \
    ComplaintForm, CustomerForm, HealthForm, NotificationForm, PaymentForm
from metro_app.models import Customer, Complaint, Batch, Attendance, Dietplan, Equipments, Physician, Trainer, Login, \
    Health, Notification, Payment


def home(request):
    return render(request, 'home.html')


def admin_home(request):
    return render(request, 'admin_home.html')


def logout_view(request):
    logout(request)
    return redirect('/')


# def login(request):
#     return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def add_attendance(request):
    customer = Customer.objects.all()
    return render(request, 'admintemp/add_attendance.html', {'customer': customer})


def add_batch(request):
    batch_form = BatchForm()
    if request.method == 'POST':
        batch_form = BatchForm(request.POST)
        # print(batch_form)
        if batch_form.is_valid():
            batch_form.save()
            messages.info(request, 'Batch Added Successful')
            return redirect('admin_home')
    return render(request, 'admintemp/add_batch.html', {'batch_form': batch_form})


def add_dietplan(request):
    dietplan_form = DietplanForm()
    if request.method == 'POST':
        dietplan_form = DietplanForm(request.POST, request.FILES)
        if dietplan_form.is_valid():
            dietplan = dietplan_form.save()
            dietplan.save()
            messages.info(request, 'Equipment Added Successful')
            return redirect('dietplan_view')
    return render(request, 'trainertemp/add_dietplan.html', {'dietplan_form': dietplan_form})


def add_equipments(request):
    equipment_form = EquipmentsForm()
    if request.method == 'POST':
        equipment_form = EquipmentsForm(request.POST, request.FILES)
        if equipment_form.is_valid:
            equipment = equipment_form.save()
            equipment.save()
            messages.info(request, 'Equipment Added Successful')
        return redirect('equipments_view')
    return render(request, 'admintemp/add_equipments.html', {'equipment_form': equipment_form})


def add_reply(request, id):
    print("hiii")
    rid = Complaint.objects.get(id=id)
    if request.method == 'POST':
        r = request.POST.get('reply')
        rid.reply = r
        rid.save()
        messages.info(request, 'Reply added Successfuly')
        return redirect('complaint_admview')
    return render(request, 'admintemp/add_reply.html', {'rid': rid})


def admin_home(request):
    return render(request, 'admintemp/admin_home.html')


def batch_update(request, id):
    data = Batch.objects.get(id=id)
    if request.method == 'POST':
        form = BatchForm(request.POST or None, instance=data)
        if form.is_valid():
            form.save()
            messages.info(request, 'Batch update Succesfully')
            return redirect('batch_view')
    else:
        form = BatchForm(instance=data)
    return render(request, 'admintemp/batch_update.html', {'form': form})


def batch_view(request):
    batch = Batch.objects.all()
    return render(request, 'admintemp/batch_view.html', {'batch': batch})


def complaint_admview(request):
    complaint2 = Complaint.objects.all()
    return render(request, 'admintemp/complaint_admview.html', {'complaint2': complaint2})


def customer_view(request):
    customer = Customer.objects.all()
    return render(request, 'admintemp/customer_view.html', {'customer': customer})


def day_attendance(request, date):
    attendance = Attendance.objects.filter(date=date)
    context = {
        'attendances': attendance,
        'date': date
    }
    return render(request, 'admintemp/day_attendance.html', context)


def dietplan_view(request):
    dietplan = Dietplan.objects.all()
    return render(request, 'trainertemp/dietplan_view.html', {'dietplan': dietplan})


def equipments_view(request):
    equipments = Equipments.objects.all()
    return render(request, 'admintemp/equipments_view.html', {'equipments': equipments})


now = datetime.datetime.now()


def mark_attendance(request, id):
    user = Customer.objects.get(user_id=id)
    att = Attendance.objects.filter(name=user, date=datetime.date.today())
    if att.exists():
        messages.info(request, "today's attendance already marked for this student")
        return redirect('add_attendance')
    else:
        if request.method == 'POST':
            attendance = request.POST.get('attendance')
            Attendance(name=user, date=datetime.date.today(), attendance=attendance, time=now.time()).save()
            messages.info(request, "attendance added successfully")
            return redirect('add_attendance')
        return render(request, 'admintemp/mark_attendance.html')


def physician_register(request):
    login_form = LoginForm()
    physician_form = PhysicianForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        physician_form = PhysicianForm(request.POST, request.FILES)
        if login_form.is_valid() and physician_form.is_valid():
            user = login_form.save(commit=False)
            user.is_physician = True
            user.save()
            physician = physician_form.save(commit=False)
            physician.user = user
            physician.save()
            messages.info(request, 'Registration successful')
            return redirect('physician_view')
    return render(request, 'admintemp/physician_register.html',
                  {'login_form': login_form, 'physician_form': physician_form})


def physician_view(request):
    register1 = Physician.objects.all()
    return render(request, 'admintemp/physician_view.html', {'register1': register1})


def trainer_register(request):
    login_form = LoginForm()
    trainer_form = TrainerForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        trainer_form = TrainerForm(request.POST, request.FILES)
        if login_form.is_valid() and trainer_form.is_valid():
            user = login_form.save(commit=False)
            user.is_trainer = True
            user.save()
            trainer = trainer_form.save(commit=False)
            trainer.user = user
            trainer.save()
            messages.info(request, 'Registration successful')
            return redirect('trainer_view')
    return render(request, 'admintemp/trainer_register.html', {'login_form': login_form, 'trainer_form': trainer_form})


def trainer_view(request):
    register = Trainer.objects.all()
    return render(request, 'admintemp/trainer_view.html', {'register': register})


def view_attendance(request):
    value_list = Attendance.objects.values_list('date', flat=True).distinct()
    attendance = {}
    for value in value_list:
        attendance[value] = Attendance.objects.filter(date=value)
    return render(request, 'admintemp/view_attendance.html', {'attendances': attendance})


####################USERTEMP###########

def add_complaint(request):
    complaint_form = ComplaintForm()
    u = request.user
    if request.method == 'POST':
        complaint_form = ComplaintForm(request.POST)
        if complaint_form.is_valid():
            obj = complaint_form.save(commit=False)
            obj.user = u
            obj.save()
            messages.info(request, 'Comlaint Added Successful')
            return redirect('complaint_view')
    return render(request, 'usertemp/add_complaint.html', {'complaint_form': complaint_form})


def complaint_view(request):
    complaint = Complaint.objects.filter(user=request.user)
    return render(request, 'usertemp/complaint_view.html', {'complaint': complaint})


def customer_register(request):
    login_form = LoginForm()
    customer_form = CustomerForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        customer_form = CustomerForm(request.POST, request.FILES)
        if login_form.is_valid() and customer_form.is_valid():
            user = login_form.save(commit=False)
            user.is_customer = True
            user.save()
            customer = customer_form.save(commit=False)
            customer.user = user
            customer.save()
            messages.info(request, 'Registration successfully')
            return redirect('login_view')
    return render(request, 'register.html', {'login_form': login_form, 'customer_form': customer_form})


def dietplanuser_view(request):
    dietplan = Dietplan.objects.all()
    return render(request, 'admintemp/dietplanuser_view.html', {'dietplan': dietplan})


def register(request):
    return render(request, 'usertemp/register.html')


def user_home(request):
    return render(request, 'usertemp/user_home.html')


def userequipments_view(request):
    equipments = Equipments.objects.all()
    return render(request, 'usertemp/userequipments_view.html', {'equipments': equipments})


def userphysician_view(request):
    register1 = Physician.objects.all()
    return render(request, 'usertemp/userphysician_view.html', {'register1': register1})


def usertrainer_view(request):
    register = Trainer.objects.all()
    return render(request, 'usertemp/usertrainer_view.html', {'register': register})


def trainer_home(request):
    return render(request, 'trainertemp/trainer_home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('admin_home')
            elif user.is_trainer:
                return redirect('trainer_home')
            elif user.is_customer:
                return redirect('user_home')
        else:
            messages.info(request, 'invalid credential')
    return render(request, 'login.html')


def trainer_delete(request, id):
    data1 = Trainer.objects.get(id=id)
    data = Login.objects.get(trainer=data1)
    if request.method == "POST":
        data.delete()
        return redirect('trainer_view')
    else:
        return redirect('trainer_view')


def physician_delete(request, id):
    data1 = Physician.objects.get(id=id)
    data = Login.objects.get(physician=data1)
    if request.method == 'POST':
        data.delete()
        return redirect('physician_view')
    else:
        return redirect('physician_view')


def equipments_delete(request, id):
    data = Equipments.objects.get(id=id)
    if request.method == 'POST':
        data.delete()
        return redirect('equipments_view')
    else:
        return redirect('equipments_view')


def batch_delete(request, id):
    data = Batch.objects.get(id=id)
    if request.method == 'POST':
        data.delete()
        return redirect('batch_view')
    else:
        return redirect('batch_view')


def customer_delete(request, id):
    data = Customer.objects.get(id=id)
    if request.method == 'POST':
        data.delete()
        return redirect('customer_view')
    else:
        return redirect('customer_view')


def add_health(request):
    health_form = HealthForm()
    if request.method == 'POST':
        health_form = HealthForm(request.POST)
        if health_form.is_valid():
            health_form.save()
            messages.info(request, 'added successfully')
        return redirect('health_view')
    return render(request, 'trainertemp/add_health.html', {'health_form': health_form})


def health_view(request):
    health = Health.objects.all()
    return render(request, 'trainertemp/health_view.html', {'health': health})


def trainer_custview(request):
    customer = Customer.objects.all()
    return render(request, 'trainertemp/trainer_custview.html', {'customer': customer})


def add_notification(request):
    notification = NotificationForm()
    if request.method == 'POST':
        notification = NotificationForm(request.POST)
        if notification.is_valid():
            notification.save()
            messages.info(request, 'notification added successfully!')
            return redirect('notification_view')
    return render(request, 'admintemp/add_notification.html', {'notification': notification})


def view_notification(request):
    notif = Notification.objects.all()
    return render(request, 'usertemp/view_notification.html', {'notif': notif})


def notifi_update(request, id):
    data = Notification.objects.get(id=id)
    if request.method == 'POST':
        form = NotificationForm(request.POST or None, instance=data)
        if form.is_valid():
            form.save()
            messages.info(request, 'notification Updated')
            return redirect('view_notification')
    else:
        form = NotificationForm(instance=data)
    return render(request, 'admintemp/noti_update.html', {'form': form})


def notification_delete(request, id):
    data = Notification.objects.get(id=id)
    if request.method == 'POST':
        data.delete()
        return redirect('view_notification')
    else:
        return redirect('view_notification')


def add_payment(request):
    payment_form = PaymentForm()
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            payment_form.save()
            messages.info(request, 'added succussfully')
            return redirect('admin_home')
    return render(request, 'admintemp/add_payment.html', {'payment_form': payment_form})


def payment_view(request):
    payment = Payment.objects.all()
    return render(request, 'admintemp/payment_view.html', {'payment': payment})


def userpayment_view(request):
    pay = Payment.objects.filter(name=request.user.customer)
    return render(request, 'usertemp/userpayment_view.html', {'pay': pay})


def notification_view(request):
    notif = Notification.objects.all()
    return render(request, 'admintemp/notification_view.html', {'notif': notif})


def profile_view(request):
    prof = Trainer.objects.all()
    return render(request, 'trainertemp/profile_view.html', {'prof': prof})


def add_card(request, id):
    pay = Payment.objects.get(id=id)
    if request.method == 'POST':
        c = request.POST.get('card_no')
        cn = request.POST.get('card_name')
        cvv = request.POST.get('cvv')
        pay.card_no = c
        pay.card_name = cn
        pay.cvv = cvv
        pay.save()
        messages.info(request, 'Payment Done Successfully!')
        return redirect('cardpay_view')
    return render(request, 'usertemp/add_card.html', {'pay': pay})


def cardpay_view(request):
    return render(request, 'usertemp/cardpay.html')
