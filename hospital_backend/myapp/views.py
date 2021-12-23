from django.shortcuts import render

# Create your views here.
from . import models
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.forms.models import model_to_dict
import dateutil.parser

@csrf_exempt
def patient_register(request):
    userName = request.POST.get('userName', 'username')
    password = request.POST.get('password', 'xxx')
    email = request.POST.get('email', '未注册')

    realName = request.POST.get('realName','xxx')
    phoneNumber = request.POST.get('phoneNumber','xxx')
    idCardNumber = request.POST.get('idCardNumber','xxx')
    gender = request.POST.get('gender','x')
    birthday = dateutil.parser.parse(request.POST.get('birthday','2000-01-01'))



    res = {'retCode': 0, 'message': ''}

    obj = models.Patient.objects.filter(userName=userName)
    if obj.count() == 0:

        models.Patient.objects.create(
            userName=userName, password=password,email=email,realName=realName,
            gender=gender,birthday=birthday,idCardNumber=idCardNumber,phoneNumber=phoneNumber
        )
        obj = models.Patient.objects.get(userName=userName)
        # obj.collectList.remove('-1')
        obj.save()
        res['retCode'] = 1
        res['message'] = '注册成功'

    else:
        res['retCode'] = 0
        res['message'] = '用户名已注册'

    return JsonResponse(res)

@csrf_exempt
def docter_register(request):
    userName = request.POST.get('userName', 'username')
    password = request.POST.get('password', 'xxx')
    email = request.POST.get('email', '未注册')

    realName = request.POST.get('realName','xxx')
    phoneNumber = request.POST.get('phoneNumber','xxx')
    idCardNumber = request.POST.get('idCardNumber','xxx')
    gender = request.POST.get('gender','x')
    birthday = dateutil.parser.parse(request.POST.get('birthday','2000-01-01'))

    college = request.POST.get('college','Peking')
    degree = request.POST.get('degree','Peking')
    office_name = request.POST.get('office','x')
    is_leader = int(request.POST.get('leader',0))

    res = {'retCode': 0, 'message': ''}

    obj = models.Doctor.objects.filter(userName=userName)
    if obj.count() == 0:
        office = models.Office.objects.filter(name=office_name)
        if office.count() == 0:
            office = None
        else:
            office = office[0]
            if is_leader == True:
                office.leader_username = userName
                office.save()

        models.Doctor.objects.create(
            userName=userName, password=password,email=email,realName=realName,
            gender=gender,birthday=birthday,idCardNumber=idCardNumber,phoneNumber=phoneNumber,
            college=college,degree=degree,office=office,is_leader=is_leader

        )
        obj = models.Doctor.objects.get(userName=userName)
        # obj.collectList.remove('-1')
        obj.save()
        res['retCode'] = 1
        res['message'] = '注册成功'

    else:
        res['retCode'] = 0
        res['message'] = '用户名已注册'

    return JsonResponse(res)

@csrf_exempt
def login(request):
    userName = request.POST.get('userName', 'username')
    password = request.POST.get('password', 'xxx')
    type = request.POST.get('type')
    res = {'retCode': -1, 'message': ''}
    print("userName = {}, password = {}".format(userName,password))

    if type == 'patient':
        obj = models.Patient.objects.filter(userName=userName)
        if obj.count() == 0:
            res['retCode'] = 0
            res['message'] = '用户不存在'
            print('用户不存在')
        else:
            obj = models.Patient.objects.get(userName=userName)
            if obj.password == password:
                res['retCode'] = 1
                res['message'] = '成功登录'
                print("登陆成功")
            else:
                res['retCode'] = 2
                res['message'] = '用户名或密码错误'
                print("密码错误")
    elif type == 'doctor':
        obj = models.Doctor.objects.filter(userName=userName)
        if obj.count() == 0:
            res['retCode'] = 0
            res['message'] = '用户不存在'
            print('用户不存在')
        else:
            obj = models.Doctor.objects.get(userName=userName)
            if obj.password == password:
                res['retCode'] = 1
                res['message'] = '成功登录'
                print("登陆成功")
            else:
                res['retCode'] = 2
                res['message'] = '用户名或密码错误'
                print("密码错误")


    return JsonResponse(res)


@csrf_exempt
def patient_info(request):
    userName = request.POST.get('userName', 'username')
    obj = models.Patient.objects.filter(userName=userName)
    res = {'retCode': -1, 'message': ''}
    if obj.count() == 0:
        res['retCode'] = 0
        res['message'] = '用户不存在'
        print('用户不存在')
    else:
        obj = models.Patient.objects.get(userName=userName)

        res['retCode'] = 1
        res['message'] = '查询成功'
        res['userName'] = obj.userName
        res['realName'] = obj.realName
        res['gender'] = obj.gender
        res['birthday'] = obj.birthday
        res['phoneNumber'] = obj.phoneNumber
        print('查询成功')

    return JsonResponse(res)

@csrf_exempt
def doctor_info(request):
    userName = request.POST.get('userName', 'username')
    doctor = models.Doctor.objects.filter(userName=userName)
    res = {'retCode': -1, 'message': ''}
    if doctor.count() == 0:
        res['retCode'] = 0
        res['message'] = '用户不存在'
        print('用户不存在')
    else:
        doctor = doctor[0]

        res['retCode'] = 1
        res['message'] = '查询成功'
        res['userName'] = doctor.userName
        res['realName'] = doctor.realName
        res['gender'] = doctor.gender
        res['birthday'] = doctor.birthday
        res['phoneNumber'] = doctor.phoneNumber
        res['college'] = doctor.college
        res['degree'] = doctor.degree
        res['is_leader'] = doctor.is_leader
        res['office'] = doctor.office.name
        print('查询成功')

    return JsonResponse(res)


@csrf_exempt
def modify_patient(request):
    userName = request.POST.get('userName')
    password = request.POST.get('password')
    email = request.POST.get('email')
    phoneNumber = request.POST.get('phoneNumber')

    obj = models.Patient.objects.get(userName=userName)
    if password is not None:
        obj.password = password
    if email is not None:
        obj.email = email
    if phoneNumber is not None:
        obj.phoneNumber = phoneNumber

    obj.save()

    res = {'retCode': 1, 'message': '修改成功'}
    return JsonResponse(res)

@csrf_exempt
def modify_doctor(request):
    userName = request.POST.get('userName')
    password = request.POST.get('password')
    email = request.POST.get('email')
    phoneNumber = request.POST.get('phoneNumber')

    obj = models.Doctor.objects.get(userName=userName)
    if password is not None:
        obj.password = password
    if email is not None:
        obj.email = email
    if phoneNumber is not None:
        obj.phoneNumber = phoneNumber

    obj.save()

    res = {'retCode': 1, 'message': '修改成功'}
    return JsonResponse(res)

@csrf_exempt
def make_appointment(request):
    patient_name = request.POST.get('pName')
    doctor_name = request.POST.get('dName')
    date = dateutil.parser.parse(request.POST.get('date'))

    res = {'retCode': -1, 'message': ''}
    #这里不知道写timezone.now()行不行，有问题之后再改
    doc_today_apps = models.Appointment.objects.filter(dName=doctor_name,date=timezone.now())
    if doc_today_apps.count()>30:
        res = {'retCode': 0, 'message': '预约失败'}
        return JsonResponse(res)
    else:
        obj = models.Appointment.objects.create(pName=patient_name,dName=doctor_name,date=date)
        obj.save()
        res = {'retCode': 1, 'message': '预约成功'}
        return JsonResponse(res)

@csrf_exempt
def doctor_appointments(request):
    userName = request.POST.get('userName')
    app_list = models.Appointment.objects.filter(dName=userName)
    res_list = []
    for app in app_list:
        app_dict = model_to_dict(app)
        dName = app.dName
        pName = app.pName
        app_dict['dRealName'] = models.Doctor.objects.get(userName=dName).realName
        app_dict['pRealName'] = models.Patient.objects.get(userName=pName).realName
        res_list.append(app_dict)
    res = {'retCode': 1}
    res['appList'] = res_list
    return JsonResponse(res)

@csrf_exempt
def doctor_appointments_by_date(request):
    userName = request.POST.get('userName')
    date = request.POST.get('date')
    app_list = models.Appointment.objects.filter(dName=userName,date=date)
    res_list = []
    for app in app_list:
        app_dict = model_to_dict(app)
        dName = app.dName
        pName = app.pName
        app_dict['dRealName'] = models.Doctor.objects.get(userName=dName).realName
        app_dict['pRealName'] = models.Patient.objects.get(userName=pName).realName
        res_list.append(app_dict)
    res = {'retCode': 1}
    res['appList'] = res_list
    return JsonResponse(res)

@csrf_exempt
def patient_appointments(request):
    userName = request.POST.get('userName')
    app_list = models.Appointment.objects.filter(pName=userName)
    res_list = []
    for app in app_list:
        app_dict = model_to_dict(app)
        dName = app.dName
        pName = app.pName
        app_dict['dRealName'] = models.Doctor.objects.get(userName=dName).realName
        app_dict['pRealName'] = models.Patient.objects.get(userName=pName).realName
        res_list.append(app_dict)
    res = {'retCode': 1}
    res['appList'] = res_list
    return JsonResponse(res)

@csrf_exempt
def patient_appointments_by_date(request):
    userName = request.POST.get('userName')
    date = request.POST.get('date')
    app_list = models.Appointment.objects.filter(pName=userName,date=date)
    res_list = []
    for app in app_list:
        app_dict = model_to_dict(app)
        dName = app.dName
        pName = app.pName
        app_dict['dRealName'] = models.Doctor.objects.get(userName=dName).realName
        app_dict['pRealName'] = models.Patient.objects.get(userName=pName).realName
        res_list.append(app_dict)
    res = {'retCode': 1}
    res['appList'] = res_list
    return JsonResponse(res)


@csrf_exempt
def make_mr(request):
    pName = request.POST.get('pName')
    dName = request.POST.get('dName')
    date = dateutil.parser.parse(request.POST.get('date'))
    medical = request.POST.get('medical')

    prescription = models.Prescription.objects.create(pName=pName,dName=dName,date=date,medical=medical)
    prescription.save()
    mr = models.MedicalRecord.objects.create(pName=pName,dName=dName,date=date,prescription=prescription)
    mr.save()
    res = {'retCode': 1, 'message': '预约成功'}
    return JsonResponse(res)

@csrf_exempt
def patient_mrs(request):
    userName = request.POST.get('userName')
    mr_list = models.MedicalRecord.objects.filter(pName=userName)
    res_list = []
    for mr in mr_list:
        mr_dict = model_to_dict(mr)
        dName = mr.dName
        pName = mr.pName
        mr_dict['dRealName'] = models.Doctor.objects.get(userName=dName).realName
        mr_dict['pRealName'] = models.Patient.objects.get(userName=pName).realName
        res_list.append(mr_dict)
    res = {'retCode': 1}
    res['mrList'] = res_list
    return JsonResponse(res)

@csrf_exempt
def patient_mrs_by_date(request):
    userName = request.POST.get('userName')
    date = request.POST.get('date')
    mr_list = models.MedicalRecord.objects.filter(pName=userName,date=date)
    res_list = []
    for mr in mr_list:
        mr_dict = model_to_dict(mr)
        dName = mr.dName
        pName = mr.pName
        mr_dict['dRealName'] = models.Doctor.objects.get(userName=dName).realName
        mr_dict['pRealName'] = models.Patient.objects.get(userName=pName).realName
        res_list.append(mr_dict)
    res = {'retCode': 1}
    res['mrList'] = res_list
    return JsonResponse(res)

@csrf_exempt
def office_register(request):
    name = request.POST.get('name')
    leader_username = request.POST.get('leader_username')
    description = request.POST.get('description')
    res = {'retCode': -1}
    office = models.Office.objects.create(name=name,leader_username=leader_username,description=description)
    office.save()
    if leader_username is not None:
        doctor = models.Doctor.objects.filter(userName=leader_username)
        if doctor.count() == 0:
            res['retCode'] = 2
        else:
            #把科长信息修改了
            doctor = doctor[0]
            doctor.is_leader = True
            doctor.office = office
            doctor.save()
            res['retCode'] = 1

    return JsonResponse(res)








