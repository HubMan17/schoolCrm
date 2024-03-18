import django
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.db.models import Avg, Min, Max, Sum
from .models import *

from .tasks import send_mail_to_enrollee

import secrets
import string

from datetime import timedelta, date
import json

import time

# create history for card
def create_cardHistory(idCard, idUser, changeData, comment, field):
        CardHistory.objects.create(
                idCard=StudentCard.objects.get(id=idCard),
                idUser=User.objects.get(id=idUser),
                comment=comment,
                field=field,
                changeData=changeData
            )

def password_generator():
    return ''.join(secrets.choice(string.ascii_letters + string.digits + '-_') for _ in range(8))


# def send_mail_to_enrollee(lastName, firstName, email, password, enrolleeProfile):
    
#     time.sleep(5)
    
#     # send login and password to email
#     text = f"""Здравствуйте, {lastName} {firstName}, Ваше заявление было успешно принято.

# Для получения дальнейшей информации вы можете обратиться в отдел приёмной комиссии КЭСП или использовать данные для авторизации в вашем профиле на сайте учебной организации:
# Ваш логин: {email}
# Ваш пароль: {password}"""

#     return send_mail('Приёмная комиссия КЭСП', text, 
#                     'notification@dzhanatly.fvds.ru', [enrolleeProfile], fail_silently=False)
            
            

def index(request):
    return HttpResponse("Hello, world!")

@csrf_exempt
def  api_crm_authorization(request):
    
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        post = json.loads(body)
        
        login = post['login']
        password = post['password']
        
        user = User.objects.filter(login=login, password=password).first()
        if user:
            token = django.middleware.csrf.get_token(request)
            
            user.token = token
            user.timeLiveToken = date.today() + timedelta(days=14)
            user.save()
            
            return JsonResponse({
                'status': 'success',
                'code': 200,
                'id': user.id,
                'name': user.name,
                'role': user.role,
                'token': token
            })
        else:
            return JsonResponse({
                'status': 'error',
                'code': 200
            })

@csrf_exempt
def  api_crm_get_token(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        post = json.loads(body)
        
        token = post['token']
        tokenCRM = post['tokenCRM']
        
        if token:
            print(token)
            
        if tokenCRM:
            user = User.objects.filter(token=tokenCRM).first()
            
            if user:
                return JsonResponse({
                    'status': 'success',
                    'code': 200,
                    'id': user.id,
                    'name': user.name,
                    'role': user.role,
                    'token': token
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'code': 200
                })
    else:
        return JsonResponse({
                    'status': 'success',
                    'code': 200
                })

def api_crm(request):
    # send_mail('Приёмная комиссия КЭСП', 'This e-mail was sent with Django.', 
    # 'notification@dzhanatly.fvds.ru', ['dzhanatly@gmail.com'], fail_silently=False)
    
    return JsonResponse({
        'message': 'Something new',
        'status': 200,
    })

def api_crm_get_stages(request):
    data = StudentBoard.objects.exclude(id=0).order_by("position").values('id', 'name', 'position', 'color')
    
    return JsonResponse({
        "data": list(data)
    })
    
def api_crm_get_cards(request):
    countStages = StudentBoard.objects.count()
    data = StudentCard.objects.all().order_by('-id').values(
        'id', 'date', 'idEnrollee__firstName', 'idEnrollee__lastName', 'idStage', 'idStage__name', 'idStage__position',
        'idEnrollee__idSpecialties__name')
    
    cardsToStages = [[] for i in range(countStages)]
    
    for card in data:
        cardsToStages[card['idStage__position']].append(card)
    
    return JsonResponse(cardsToStages, safe=False)
    
def api_crm_update_idStage_card(request):
    idCard = request.GET.get('card')
    idStage = request.GET.get('stage')
    
    StudentCard.objects.filter(id=idCard).update(idStage=idStage)
    
    return JsonResponse({
        'message': 'ok',
        'status': 200
    })
    
def api_crm_get_specialties(request):
    data = Specialties.objects.all().values('name')
    
    return JsonResponse({
        "data": list(data)
    })

@csrf_exempt
def api_crm_create_fast_card(request):
    
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        
        idUser = body["data"]["idUser"]
        
        specialtyName = body["data"]["specialtyName"]
        lastName = body["data"]["lastName"]
        firstName = body["data"]["firstName"]
        email = body["data"]["email"]
        
        try: phone = body["data"]["phone"]
        except: phone = ""
        
        try: middleName = body["data"]["middleName"]
        except: middleName = ""
        
        # check data is not registered
        if Enrollee.objects.filter(lastName=lastName, firstName=firstName).exists() or \
            EnrolleeProfile.objects.filter(email=email).exists() or \
                Student.objects.filter(lastName=lastName, firstName=firstName).exists():
            
            return JsonResponse({
                'statusCreate': 'failed'
            })
        else:
            # create password
            password = password_generator()
            
            document = Document.objects.create()
            enrolleeProfile = EnrolleeProfile.objects.create(
                email=email,
                phone=phone,
                status=1,
                password=password
            )
            
            # create Enrollee
            enrollee = Enrollee.objects.create(
                firstName=firstName,
                middleName=middleName,
                lastName=lastName,
                idSpecialties=Specialties.objects.get(name=specialtyName),
                idDocument=document,
                typeOfEducation=Education.objects.get(id=0),
                idEnrolleeProfile=EnrolleeProfile.objects.get(id=enrolleeProfile.id),
            )
            
            studentCard = StudentCard.objects.create(
                idEnrollee=Enrollee.objects.get(id=enrollee.id),
                idStage=StudentBoard.objects.get(id=0),
                date=date.today()
            )
            
            # creaete rows in CardHistory
            # specialty
            create_cardHistory(
                idCard=studentCard.id,
                idUser=idUser,
                comment=False,
                field='Специальность',
                changeData=specialtyName,
            )
            
            # last name
            create_cardHistory(
                idCard=studentCard.id,
                idUser=idUser,
                comment=False,
                field='Фамилия',
                changeData=lastName,
            )
            
            # first name
            create_cardHistory(
                idCard=studentCard.id,
                idUser=idUser,
                comment=False,
                field='Имя',
                changeData=firstName,
            )
            
            # email
            create_cardHistory(
                idCard=studentCard.id,
                idUser=idUser,
                comment=False,
                field='Электронная почта',
                changeData=email,
            )
            
            # phone
            if phone:
                create_cardHistory(
                idCard=studentCard.id,
                idUser=idUser,
                comment=False,
                field='Телефон',
                changeData=phone,
            )
            
            # middle name
            if middleName:
                create_cardHistory(
                idCard=studentCard.id,
                idUser=idUser,
                comment=False,
                field='Отчество',
                changeData=middleName,
            )
            
            data = StudentCard.objects.filter(id=studentCard.id).values(
                'id', 'date', 'idEnrollee__firstName', 'idEnrollee__lastName', 'idStage', 'idStage__name',
                'idEnrollee__idSpecialties__name')
            
            
            send_mail_to_enrollee.delay(lastName, firstName, email, password, enrolleeProfile.email)

            return JsonResponse(list(data), safe=False)
        
    else:
        print("Not Accepting POST request")    
        return HttpResponse("Hello, world!")
    
def api_crm_delete_card(request):
    idCard = request.GET.get('id')
    
    idEnrollee = StudentCard.objects.get(id=idCard).idEnrollee.id
    idDocument = Enrollee.objects.get(id=idEnrollee).idDocument.id
    
    EnrolleeProfile.objects.get(id=Enrollee.objects.get(id=idEnrollee).idEnrolleeProfile.id).delete()
    document = Document.objects.get(id=idDocument)
    
    document.passport.delete()
    document.copyPassport.delete()
    document.documentOfEducation.delete()
    document.medicalDoc_086_y.delete()
    document.medicalDoc_29_H.delete()
    document.copySNILS.delete()
    document.medicalInsurance.delete()
    document.photo_3_x_4.delete()
    document.save()
    document.delete()
    
    return JsonResponse({
        'message': 'success',
        'status': 200
    })
    
@csrf_exempt
def api_crm_update_stage(request):
    
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        
        stagesRequest = [stage['id'] for stage in body]
        stagesName = [stage['id'] for stage in StudentBoard.objects.all().exclude(id=0).values('id')]
        
        for stage in stagesName:
            if stage not in stagesRequest:
                if StudentCard.objects.filter(idStage__id=stage).count():

                    return JsonResponse({
                        'status': 'failed',
                        'code': 400
                    })
                else:
                    StudentBoard.objects.filter(id=stage).delete()
                    
        
        for stage in body:
            if stage['id'] == False:
                StudentBoard.objects.create(
                    name=stage['name'],
                    position = stage['position'],
                    color = stage['color']
                )
            
            else:
                StudentBoard.objects.filter(id=stage['id']).update(
                name=stage['name'],
                position = stage['position'],
                color = stage['color']
            )
        
        return JsonResponse({
            'status': 'success',
            'code': 200
        })
        
    else:
        return JsonResponse({
            'status': 400,
            'message': 'Not Accepting POST request'
        })

@csrf_exempt
def api_crm_get_file(request):
    if request.method == 'POST':
        body_unicode = request.FILES.get('file')
        doc = Document.objects.get(id=47)
        doc.passport.delete()
        
        doc.passport = body_unicode
        doc.save()
        
    return JsonResponse({
        'status': 200
    })

@csrf_exempt     
def api_crm_get_data_for_form(request):

    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        idCard = json.loads(body_unicode)['id']
        
        historyCard = CardHistory.objects.filter(idCard=idCard).values(
            'id', 'changeData', 'idUser__name',  'comment', 'field', 'changeDate'
        )
        
        # changed time in history
        for item in historyCard:
            item['changeDate'] = item['changeDate'].strftime('%Y-%m-%d %H:%M:%S')
        
        specialties = [name['name'] for name in Specialties.objects.all().values('name')]
        stages = [stage['name'] for stage in StudentBoard.objects.all().exclude(id=0).values('name').order_by('position')]
        educations = [education['name'] for education in Education.objects.all().exclude(id=0).values('name')]
        
        # print()
        # print(Specialties.objects.get(id=Enrollee.objects.get(id=StudentCard.objects.get(id=idCard).idEnrollee).idSpecialties).name)
        # get main data
        main_data = {
            "specialty": StudentCard.objects.filter(id=idCard).values('idEnrollee__idSpecialties__name')[0]['idEnrollee__idSpecialties__name'],
            "stage": StudentCard.objects.filter(id=idCard).values('idStage__name')[0]['idStage__name'],
            "education": StudentCard.objects.filter(id=idCard).values('idEnrollee__typeOfEducation__name')[0]['idEnrollee__typeOfEducation__name'],
            "lastName": StudentCard.objects.filter(id=idCard).values('idEnrollee__lastName')[0]['idEnrollee__lastName'],
            "firstName": StudentCard.objects.filter(id=idCard).values('idEnrollee__firstName')[0]['idEnrollee__firstName'],
            "middleName": StudentCard.objects.filter(id=idCard).values('idEnrollee__middleName')[0]['idEnrollee__middleName'],
            "birthDate": StudentCard.objects.filter(id=idCard).values('idEnrollee__birthDate')[0]['idEnrollee__birthDate'],
            "phone": StudentCard.objects.filter(id=idCard).values('idEnrollee__idEnrolleeProfile__phone')[0]['idEnrollee__idEnrolleeProfile__phone'],
            "email": StudentCard.objects.filter(id=idCard).values('idEnrollee__idEnrolleeProfile__email')[0]['idEnrollee__idEnrolleeProfile__email'],
            "passport": StudentCard.objects.filter(id=idCard).values('idEnrollee__idDocument__passport')[0]['idEnrollee__idDocument__passport'],
            "copyPassport": StudentCard.objects.filter(id=idCard).values('idEnrollee__idDocument__copyPassport')[0]['idEnrollee__idDocument__copyPassport'],
            "documentOfEducation": StudentCard.objects.filter(id=idCard).values('idEnrollee__idDocument__documentOfEducation')[0]['idEnrollee__idDocument__documentOfEducation'],
            "medicalDoc_086_y": StudentCard.objects.filter(id=idCard).values('idEnrollee__idDocument__medicalDoc_086_y')[0]['idEnrollee__idDocument__medicalDoc_086_y'],
            "medicalDoc_29_H": StudentCard.objects.filter(id=idCard).values('idEnrollee__idDocument__medicalDoc_29_H')[0]['idEnrollee__idDocument__medicalDoc_29_H'],
            "copySNILS": StudentCard.objects.filter(id=idCard).values('idEnrollee__idDocument__copySNILS')[0]['idEnrollee__idDocument__copySNILS'],
            "medicalInsurance": StudentCard.objects.filter(id=idCard).values('idEnrollee__idDocument__medicalInsurance')[0]['idEnrollee__idDocument__medicalInsurance'],
            "photo_3_x_4": StudentCard.objects.filter(id=idCard).values('idEnrollee__idDocument__photo_3_x_4')[0]['idEnrollee__idDocument__photo_3_x_4'],
        }

        # print(main_data)
                
        return JsonResponse({
                    "specialties": list(specialties),
                    "stages": list(stages),
                    "educations": list(educations),
                    "history": list(historyCard),
                    "main_data": main_data
                }, safe=False) 
        
    else:

        specialties = [name['name'] for name in Specialties.objects.all().values('name')]
        stages = [stage['name'] for stage in StudentBoard.objects.all().exclude(id=0).values('name').order_by('position')]
        educations = [education['name'] for education in Education.objects.all().exclude(id=0).values('name')]
        
        return JsonResponse({
                    "specialties": list(specialties),
                    "stages": list(stages),
                    "educations": list(educations)
                }, safe=False)    
    
@csrf_exempt
def api_crm_create_card_from_full_form(request):
    if request.method == 'POST':
        body_text = request.POST
        body_file = request.FILES
        
        
        idUser = body_text['idUser']
        # text data
        specialtyName = body_text['specialtyName']
        stageName = body_text['stageName']
        lastName = body_text['lastName']
        firstName = body_text['firstName']
        middleName = body_text['middleName']
        date = body_text['date']
        phone = body_text['phone']
        email = body_text['email']
        education = body_text['education']
        
        # file data
        passport = body_file.get('passport')
        copyPassport = body_file.get('copyPassport')
        documentOfEducation = body_file.get('documentOfEducation')
        medicalDoc_086_y = body_file.get('medicalDoc_086_y')
        medicalDoc_29_H = body_file.get('medicalDoc_29_H')
        copySNILS = body_file.get('copySNILS')
        medicalInsurance = body_file.get('medicalInsurance')
        photo_3_x_4 = body_file.get('photo_3_x_4')
        
        # print(body_text)
        
        # check data is not registered
        if Enrollee.objects.filter(lastName=lastName, firstName=firstName).exists() or \
            EnrolleeProfile.objects.filter(email=email).exists() or \
                Student.objects.filter(lastName=lastName, firstName=firstName).exists():
            
            return JsonResponse({
                'statusCreate': 'failed'
            })
        else:
            document = Document.objects.create(
                passport = passport,
                copyPassport = copyPassport,
                documentOfEducation = documentOfEducation,
                medicalDoc_086_y = medicalDoc_086_y,
                medicalDoc_29_H = medicalDoc_29_H,
                copySNILS = copySNILS,
                medicalInsurance = medicalInsurance,
                photo_3_x_4 = photo_3_x_4,
            )
            
            # generate password
            password = password_generator()
                        
            enrolleeProfile = EnrolleeProfile.objects.create(
                email=email,
                phone=phone,
                status=1,
                password=password
            )
            
            # create Enrollee
            if date == '':
                date = None
                
            enrollee = Enrollee.objects.create(
                firstName=firstName,
                middleName=middleName,
                lastName=lastName,
                birthDate=date,
                idSpecialties=Specialties.objects.get(name=specialtyName),
                idDocument=document,
                typeOfEducation=Education.objects.get(name=education),
                idEnrolleeProfile=EnrolleeProfile.objects.get(id=enrolleeProfile.id),
            )
            
            studentCard = StudentCard.objects.create(
                idEnrollee=Enrollee.objects.get(id=enrollee.id),
                idStage=StudentBoard.objects.get(name=stageName),
                
            )
        

            # send_mail_to_enrollee(lastName, firstName, email, password, enrolleeProfile.email)
            send_mail_to_enrollee.delay(lastName, firstName, email, password, enrolleeProfile.email)
        
            # specialty name 
            if specialtyName != '':
                create_cardHistory(
                    idCard=studentCard.id,
                    idUser=idUser,
                    comment=False,
                    field='Специальность',
                    changeData=specialtyName,
                )
        
            # stage name 
            if stageName != '':
                create_cardHistory(
                    idCard=studentCard.id,
                    idUser=idUser,
                    comment=False,
                    field='Этап',
                    changeData=stageName,
                )
                
            # last name
            if lastName != '':
                create_cardHistory(
                    idCard=studentCard.id,
                    idUser=idUser,
                    comment=False,
                    field='Фамилия',
                    changeData=lastName,
                )
            
            # first name 
            if firstName != '':
                create_cardHistory(
                    idCard=studentCard.id,
                    idUser=idUser,
                    comment=False,
                    field='Имя',
                    changeData=firstName,
                )
                
            # middle name 
            if middleName != '':
                create_cardHistory(
                    idCard=studentCard.id,
                    idUser=idUser,
                    comment=False,
                    field='Отчество',
                    changeData=middleName,
                )
                
            # date of birth 
            if date != None:
                create_cardHistory(
                    idCard=studentCard.id,
                    idUser=idUser,
                    comment=False,
                    field='Дата рождения',
                    changeData=date,
                )
                
            # phone
            if phone != '':
                create_cardHistory(
                    idCard=studentCard.id,
                    idUser=idUser,
                    comment=False,
                    field='Телефон',
                    changeData=phone,
                )
                
            # email 
            if email != '':
                create_cardHistory(
                    idCard=studentCard.id,
                    idUser=idUser,
                    comment=False,
                    field='Электронная почта',
                    changeData=email,
                )
                
            # education 
            if education != '':
                create_cardHistory(
                    idCard=studentCard.id,
                    idUser=idUser,
                    comment=False,
                    field='Образование',
                    changeData=education,
                )
            
            # passport 
            if passport != None:
                create_cardHistory(
                    idCard=studentCard.id,
                    idUser=idUser,
                    comment=False,
                    field='Паспорт',
                    changeData=passport,
                )
                
            # copyPassport
            if copyPassport != None:
                create_cardHistory(
                    idCard=studentCard.id,
                    idUser=idUser,
                    comment=False,
                    field='Копия паспорта',
                    changeData=copyPassport,
                )
                
            # documentOfEducation 
            if documentOfEducation != None:
                create_cardHistory(
                    idCard=studentCard.id,
                    idUser=idUser,
                    comment=False,
                    field='Документ об образовании',
                    changeData=documentOfEducation,
                )
                
            # medicalDoc_086_y 
            if medicalDoc_086_y != None:
                create_cardHistory(
                    idCard=studentCard.id,
                    idUser=idUser,
                    comment=False,
                    field='Мед. справка №086',
                    changeData=medicalDoc_086_y,
                )
                
            # medicalDoc_29_H 
            if medicalDoc_29_H != None:
                create_cardHistory(
                    idCard=studentCard.id,
                    idUser=idUser,
                    comment=False,
                    field='Мед. справка №29-H',
                    changeData=medicalDoc_29_H,
                )
                
            # copySNILS 
            if copySNILS != None:
                create_cardHistory(
                    idCard=studentCard.id,
                    idUser=idUser,
                    comment=False,
                    field='Копия СНИЛС',
                    changeData=copySNILS,
                )
                
            # medicalInsurance
            if medicalInsurance != None:
                create_cardHistory(
                    idCard=studentCard.id,
                    idUser=idUser,
                    comment=False,
                    field='Мед. страхование',
                    changeData=medicalInsurance,
                )
                
            # photo_3_x_4 
            if photo_3_x_4 != None:
                create_cardHistory(
                    idCard=studentCard.id,
                    idUser=idUser,
                    comment=False,
                    field='Фото 3х4',
                    changeData=photo_3_x_4,
                )

        
        # doc = Document.objects.get(id=47)
        # doc.passport.delete()
        # doc.passport = body_unicode
        # doc.save()
            
    return JsonResponse({
        'statusCreate': 'success',
        'idCards': studentCard.id
    })

@csrf_exempt
def api_crm_update_card_from_full_form(request):
    if request.method == 'POST':
        body_text = request.POST
        body_file = request.FILES
        
        # text data
        idBoardCard = body_text['id']
        specialtyName = body_text['specialtyName']
        stageName = body_text['stageName']
        lastName = body_text['lastName']
        firstName = body_text['firstName']
        middleName = body_text['middleName']
        date = body_text['date']
        phone = body_text['phone']
        email = body_text['email']
        education = body_text['education']
        
        # file data
        passport = body_file.get('passport')
        copyPassport = body_file.get('copyPassport')
        documentOfEducation = body_file.get('documentOfEducation')
        medicalDoc_086_y = body_file.get('medicalDoc_086_y')
        medicalDoc_29_H = body_file.get('medicalDoc_29_H')
        copySNILS = body_file.get('copySNILS')
        medicalInsurance = body_file.get('medicalInsurance')
        photo_3_x_4 = body_file.get('photo_3_x_4')
        
        
        # check data is not registered
        if not StudentCard.objects.filter(id=idBoardCard).exists():
            
            return JsonResponse({
                'statusUpdate': 'failed'
            })
        else:
            studentCard = StudentCard.objects.filter(id=idBoardCard).values()
            if stageName != StudentBoard.objects.get(id=studentCard[0]['idStage_id']).name:
                studentCard.update(
                    idStage=StudentBoard.objects.get(name=stageName),
                )
                
                # stage name 
                if stageName != '':
                    create_cardHistory(
                        idCard=idBoardCard,
                        idUser=0,
                        comment=False,
                        field='Этап',
                        changeData=stageName,
                    )
            
            studentCard = studentCard[0]['idEnrollee_id']

            # create Enrollee
            if date == '':
                date = None
            
            enrollee = Enrollee.objects.filter(id=studentCard).values()
            
            if lastName != enrollee[0]['lastName']:
                
                enrollee.update(
                    lastName=lastName
                )
            
                # last name
                if lastName != '':
                    create_cardHistory(
                        idCard=idBoardCard,
                        idUser=0,
                        comment=False,
                        field='Фамилия',
                        changeData=lastName,
                    )
            
            if firstName != enrollee[0]['firstName']:
                enrollee.update(
                    firstName=firstName
                )
                
                # first name 
                if firstName != '':
                    create_cardHistory(
                        idCard=idBoardCard,
                        idUser=0,
                        comment=False,
                        field='Имя',
                        changeData=firstName,
                    )
                
            if middleName != enrollee[0]['middleName']:
                enrollee.update(
                    middleName=middleName
                )
                
                # middle name 
                if middleName != '':
                    create_cardHistory(
                        idCard=idBoardCard,
                        idUser=0,
                        comment=False,
                        field='Отчество',
                        changeData=middleName,
                    )
                
            if date != enrollee[0]['birthDate']:
                enrollee.update(
                    birthDate=date
                )    
            
                # date of birth 
                if date != None:
                    create_cardHistory(
                        idCard=idBoardCard,
                        idUser=0,
                        comment=False,
                        field='Дата рождения',
                        changeData=date,
                    )
                        
                        
            if specialtyName != Specialties.objects.get(id=enrollee[0]['idSpecialties_id']).name:
                enrollee.update(
                    idSpecialties=Specialties.objects.get(name=specialtyName)
                )
                
                #   specialty
                if specialtyName != '':
                    create_cardHistory(
                        idCard=idBoardCard,
                        idUser=0,
                        comment=False,
                        field='Специальность',
                        changeData=specialtyName,
                    )             
                
            if education != Education.objects.get(id=enrollee[0]['typeOfEducation_id']).name:
                enrollee.update(
                    typeOfEducation=Education.objects.get(name=education)
                )    
            
                # education 
                if education != '':
                    create_cardHistory(
                        idCard=idBoardCard,
                        idUser=0,
                        comment=False,
                        field='Образование',
                        changeData=education,
                    )
            
            enrollee = enrollee[0]
            
            enrolleeProfile = EnrolleeProfile.objects.filter(id=enrollee['idEnrolleeProfile_id'])
            if phone != EnrolleeProfile.objects.get(id=enrollee['idEnrolleeProfile_id']).phone:
                
                enrolleeProfile.update(
                    phone=phone
                )
                
                # phone
                if phone != '':
                    create_cardHistory(
                        idCard=idBoardCard,
                        idUser=0,
                        comment=False,
                        field='Телефон',
                        changeData=phone,
                    )
         
            if email != EnrolleeProfile.objects.get(id=enrollee['idEnrolleeProfile_id']).email:
                enrolleeProfile.update(
                    email=email
                )
                
                # email 
                if email != '':
                    create_cardHistory(
                        idCard=idBoardCard,
                        idUser=0,
                        comment=False,
                        field='Электронная почта',
                        changeData=email,
                    )
         
            doc = Document.objects.get(id=enrollee['idDocument_id'])
                    
            doc.passport.delete()
            doc.copyPassport.delete()
            doc.documentOfEducation.delete()
            doc.medicalDoc_086_y.delete()
            doc.medicalDoc_29_H.delete()
            doc.copySNILS.delete()
            doc.medicalInsurance.delete()
            doc.photo_3_x_4.delete()
                        
            if passport != None:
                if doc.passport != "images/" + passport.name:
                    doc.passport.delete()
                    doc.passport = passport
                    
                    # passport 
                    if passport != None:
                        create_cardHistory(
                            idCard=idBoardCard,
                            idUser=0,
                            comment=False,
                            field='Паспорт',
                            changeData=passport,
                        )
            
            if copyPassport != None:
                if doc.copyPassport != "images/" + copyPassport.name:
                    doc.copyPassport.delete()
                    doc.copyPassport = copyPassport
                    
                    # copyPassport
                    if copyPassport != None:
                        create_cardHistory(
                            idCard=idBoardCard,
                            idUser=0,
                            comment=False,
                            field='Копия паспорта',
                            changeData=copyPassport,
                        )
            
            if documentOfEducation != None:
                if doc.documentOfEducation != "images/" + documentOfEducation.name:
                    doc.documentOfEducation.delete()
                    doc.documentOfEducation = documentOfEducation
                    
                    # documentOfEducation 
                    if documentOfEducation != None:
                        create_cardHistory(
                            idCard=idBoardCard,
                            idUser=0,
                            comment=False,
                            field='Документ об образовании',
                            changeData=documentOfEducation,
                        )
            
            if medicalDoc_086_y != None:
                if doc.medicalDoc_086_y != "images/" + medicalDoc_086_y.name:
                    doc.medicalDoc_086_y.delete()
                    doc.medicalDoc_086_y = medicalDoc_086_y
                    
                    # medicalDoc_086_y 
                    if medicalDoc_086_y != None:
                        create_cardHistory(
                            idCard=idBoardCard,
                            idUser=0,
                            comment=False,
                            field='Мед. справка №086',
                            changeData=medicalDoc_086_y,
                        )
            
            if medicalDoc_29_H != None:
                if doc.medicalDoc_29_H != "images/" + medicalDoc_29_H.name:
                    doc.medicalDoc_29_H.delete()
                    doc.medicalDoc_29_H = medicalDoc_29_H
                    
                    # medicalDoc_29_H 
                    if medicalDoc_29_H != None:
                        create_cardHistory(
                            idCard=idBoardCard,
                            idUser=0,
                            comment=False,
                            field='Мед. справка №29-H',
                            changeData=medicalDoc_29_H,
                        )
            
            if copySNILS != None:
                if doc.copySNILS != "images/" + copySNILS.name:
                    doc.copySNILS.delete()
                    doc.copySNILS = copySNILS
                    
                    # copySNILS 
                    if copySNILS != None:
                        create_cardHistory(
                            idCard=idBoardCard,
                            idUser=0,
                            comment=False,
                            field='Копия СНИЛС',
                            changeData=copySNILS,
                        )
            
            if medicalInsurance != None:
                if doc.medicalInsurance != "images/" + medicalInsurance.name:
                    doc.medicalInsurance.delete()
                    doc.medicalInsurance = medicalInsurance
                    
                    # medicalInsurance
                    if medicalInsurance != None:
                        create_cardHistory(
                            idCard=idBoardCard,
                            idUser=0,
                            comment=False,
                            field='Мед. страхование',
                            changeData=medicalInsurance,
                        )
            
            if photo_3_x_4 != None:
                if doc.photo_3_x_4 != "images/" + photo_3_x_4.name:
                    doc.photo_3_x_4.delete()
                    doc.photo_3_x_4 = photo_3_x_4
                    
                    # photo_3_x_4 
                    if photo_3_x_4 != None:
                        create_cardHistory(
                            idCard=idBoardCard,
                            idUser=0,
                            comment=False,
                            field='Фото 3х4',
                            changeData=photo_3_x_4,
                        )
            
            # doc.passport = passport
            # doc.copyPassport = copyPassport
            # doc.documentOfEducation = documentOfEducation
            # doc.medicalDoc_086_y = medicalDoc_086_y
            # doc.medicalDoc_29_H = medicalDoc_29_H
            # doc.copySNILS = copySNILS
            # doc.medicalInsurance = medicalInsurance
            # doc.photo_3_x_4 = photo_3_x_4

            doc.save()

            # send_mail_to_enrollee(lastName, firstName, email, password, enrolleeProfile.email)   
            # send_mail_to_enrollee.delay(lastName, firstName, email, password, enrolleeProfile.email)

            
    return JsonResponse({
        'statusUpdate': 'success'
    })

@csrf_exempt
def api_crm_create_comment(request):
    
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        post = json.loads(body)

        idCard = post['idCard']
        comment = post['comment']
        
        try:
            idUser = post['idUser']
            
            CardHistory.objects.create(
                idCard=StudentCard.objects.get(id=idCard),
                comment=True,
                changeData=comment,
                idUser=User.objects.get(id=idUser)
            )
        except:
            CardHistory.objects.create(
                idCard=StudentCard.objects.get(id=idCard),
                comment=True,
                changeData=comment
            )
        
        return JsonResponse({
                'statusUpdate': 'success'
            })
        
    else:
        return JsonResponse({
                'statusUpdate': 'failed'
            })
    
@csrf_exempt
def api_crm_delete_comment(request):
    
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        post = json.loads(body)
        
        idComment = post['idComment']
        
        CardHistory.objects.filter(id=idComment).delete()
        
        return JsonResponse({
                'statusUpdate': 'success'
            })
        
    else:
        return JsonResponse({
                'statusUpdate': 'failed'
            })

@csrf_exempt
def api_crm_update_comment(request):
    
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        post = json.loads(body)
        
        idComment = post['idComment']
        comment = post['comment']
        
        # print(idComment, comment)
        
        CardHistory.objects.filter(id=idComment).update(changeData=comment)
        
        return JsonResponse({
                'statusUpdate': 'success'
            })
        
    else:
        return JsonResponse({
                'statusUpdate': 'failed'
            })

def api_crm_get_users(request):
    data = User.objects.exclude(id=0).order_by("-role").values('id', 'name', 'login', 'password', 'role')
    
    return JsonResponse({
        "data": list(data)
    })

@csrf_exempt
def api_crm_update_users(request):
    
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        
        usersRequest = [user['id'] for user in body]
        usersName = [user['id'] for user in User.objects.all().exclude(id=0).values('id')]
        
        for user in usersName:
            if user not in usersRequest:
                User.objects.filter(id=user).delete()
                    
        
        for user in body:
            if user['id'] == False:
                User.objects.create(
                    name=user['name'],
                    login = user['login'],
                    password = user['password'],
                    role = user['role']
                )
            
            else:
                User.objects.filter(id=user['id']).update(
                name=user['name'],
                login = user['login'],
                password = user['password'],
                role = user['role']
            )
        
        return JsonResponse({
            'status': 'success',
            'code': 200
        })
        
    else:
        return JsonResponse({
            'status': 400,
            'message': 'Not Accepting POST request'
        })

def test(request):
    
    test_celery_task.delay()
    
    # send_mail('Django mail', 'This e-mail was sent with Django.', 
    #     'notification@dzhanatly.fvds.ru', ['dzhanatly@gmail.com'])

    return JsonResponse({
        'statusUpdate': 'success',
        'code': 200
    })
    
# from datetime import timedelta, date, datetime
# print(datetime.now())
# print(CardHistory.objects.get(id=938).changeDate.strftime('%Y-%m-%d %H:%M:%S'))

# User.objects.create(
#     name = 'test',
#     login = 'test',
#     password = '12345',
#     role = True,
#     token = '12345',
#     timeLiveToken = date.today() + timedelta(days=14)
# )
# from django.contrib.auth.models import User
# user = User.objects.create_user("test", "test@test.com", "12345")
# user.save()

# print(User.objects.filter(id=2).values())
    
# save image from media folder to database
# Document.objects.filter(id=47).update(passport='images/fe93380c-6e89-4142-b6be-d065d3392ba3-original.jpg')

# Specialties.objects.create(
#     name = '09.02.07 Информационные системы и программирование',
#     price = 48000
# )

# Enrollee.objects.filter(id=1).update(idSpecialties=1)

# print(CardHistory.objects.get(id=85).changeDate.strftime('%Y-%m-%d %H:%M:%S'))

# from django.core.mail import send_mail

# send_mail('Django mail', 'This e-mail was sent with Django.', 
# 'notification@dzhanatly.fvds.ru', ['dzhanatly@gmail.com'])