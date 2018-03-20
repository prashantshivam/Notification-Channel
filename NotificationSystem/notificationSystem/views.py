from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, HttpResponseRedirect	
from notificationSystem.models import *
from datetime import date
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils import timezone
from collections import OrderedDict
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout




@login_required(login_url='/login/')
def index(request):
	context={}
	trucks=TruckDetails.objects.all()
	read_message=[]
	message = OrderedDict()
	flag=False
	print("home")
	for truck in trucks:
		certificates=Certificate.objects.filter(truck_name=truck)
		for certificate in certificates:
			days=(certificate.expire_date-datetime.date.today())
			if days <= datetime.timedelta(7):
				notify=Notifications.objects.filter(certificate_name=certificate,notice3=True).first()
				if ( notify is None) :
					print ("yes")
					Notifications.objects.create(certificate_name=certificate,notice3=True)
					flag=True
			elif days <= datetime.timedelta(15):
				notify=Notifications.objects.filter(certificate_name=certificate,notice2=True).first()
				if ( notify is None) :
					Notifications.objects.create(certificate_name=certificate,notice2=True)
					flag=True
			elif days <= datetime.timedelta(30):
				notify=Notifications.objects.filter(certificate_name=certificate,notice1=True).first()
				if ( notify is None) :
					Notifications.objects.create(certificate_name=certificate,notice1=True)
					flag=True



	notifications=Notifications.objects.all().order_by('-pk')

	for notification in notifications:
		if(notification.notice3 == True):
			message[notification.id] = {'truck_name': notification.certificate_name.truck_name,
			'days': 7 ,'certificate_name' : notification.certificate_name,'time' : notification.time3,
			'flag' : flag, 'read' : notification.read3}
		elif(notification.notice2 == True):
			message[notification.id] = {'truck_name': notification.certificate_name.truck_name,
			'days': 15 ,'certificate_name' : notification.certificate_name,'time' : notification.time2,
			'flag' : flag, 'read' : notification.read2}
		elif(notification.notice3 == True):
			message[notification.id] = {'truck_name': notification.certificate_name.truck_name,
			'days': 15 ,'certificate_name' : notification.certificate_name,'time' : notification.time3,
			'flag' : flag, 'read' : notification.read3}



	return render(request, "notification.html",{'message' : message})

@login_required(login_url='/login/')
def read_notification(request):
	if request.method == 'POST':
		id=request.POST.get('id')
		notification=Notifications.objects.get(id=id)
		notify1=notification.notice1
		notify2=notification.notice2
		notify3=notification.notice3
		Notifications.objects.filter(id=id).update(read1=notify1, 
			read2=notify2, read3=notify3)
		return HttpResponseRedirect('/notification/')
	else:
		return HttpResponseRedirect('/notification/')
	#return HttpResponseRedirect('/notificationdd/')

@login_required(login_url='/login/')
def add_vehicle (request):
	if request.method == 'POST':
		user=request.user
		owner=user
		vehicle_name=request.POST.get('vehicle-name')
		registration_number=request.POST.get('registration-number')
		pollution_exp=request.POST.get('pollution-certificate')
		insurance_exp=request.POST.get('insurance-certificate')
		fitness_exp=request.POST.get('fitness-certificate')
		pollution_exp_date = datetime.datetime.strptime(pollution_exp, "%Y-%m-%d").date()
		fitness_exp_date = datetime.datetime.strptime(fitness_exp, "%Y-%m-%d").date()
		insurance_exp_date = datetime.datetime.strptime(insurance_exp, "%Y-%m-%d").date()
		
		truck_detail=TruckDetails.objects.filter(truck_name=vehicle_name,truck_number=registration_number, truck_owner=owner)
		
		if(truck_detail):
			truck_detail=truck_detail[0]
			Certificate.objects.update(certificate_name="Pollution",
				expire_date=pollution_exp_date,truck_name=truck_detail)
			Certificate.objects.update(certificate_name="Insurance",
				expire_date=insurance_exp_date,truck_name=truck_detail)
			Certificate.objects.update(certificate_name="Fitness",
				expire_date=fitness_exp_date,truck_name=truck_detail)
		else :
			truck_detail=TruckDetails.objects.create(truck_name=vehicle_name,
				truck_number=registration_number, truck_owner=owner)
			Certificate.objects.create(certificate_name="Pollution",
				expire_date=pollution_exp_date,truck_name=truck_detail)
			Certificate.objects.create(certificate_name="Insurance",
				expire_date=insurance_exp_date,truck_name=truck_detail)
			Certificate.objects.create(certificate_name="Fitness",
				expire_date=fitness_exp_date,truck_name=truck_detail)
		return HttpResponseRedirect('/notification/')
	else :
		return HttpResponseRedirect('/notification/')


def login1(request):
	if request.method == 'POST':
		username=request.POST.get('username')
		password=request.POST.get('password')
		
		user = authenticate(request, username=username, password=password)
		if(user is not None):
			login(request, user)
			return HttpResponseRedirect('/notification/')
		else:
			message=[]
			return render(request, "login.html",{'message' : message})


def register(request):
	if request.method == 'POST':
		print(request.POST)
		name=request.POST.get('username')
		email=request.POST.get('email')
		password=request.POST.get('password')
		user = User.objects.create_user(username=name, email=email, password=password)
		user.save();
		print(user)
		message=[]
		if(user is not None):
			login(request, user)
			return HttpResponseRedirect('/notification/')
		else:
			print("yes")
			return render(request, "register.html",{'message' : message})

	else :
		message=[]
		return render(request, "register.html",{'message' : message})

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/notification/login1/')
