from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.db.models import Avg, Min, Max, Sum
from .models import *

from datetime import date
import json



def index(request):
    return HttpResponse("Hello, world!")

def api_crm(request):
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
        'id', 'date', 'idEnrollee__firstName', 'idEnrollee__lastName', 'idStage', 'idStage__name',
        'idEnrollee__idSpecialties__name')
    
    cardsToStages = [[] for i in range(countStages)]
    
    for card in data:
        cardsToStages[card['idStage']].append(card)
    
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
            document = Document.objects.create()
            enrolleeProfile = EnrolleeProfile.objects.create(
                email=email,
                phone=phone,
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
            
            data = StudentCard.objects.filter(id=studentCard.id).values(
                'id', 'date', 'idEnrollee__firstName', 'idEnrollee__lastName', 'idStage', 'idStage__name',
                'idEnrollee__idSpecialties__name')

            return JsonResponse(list(data), safe=False)
        
    else:
        print("Not Accepting POST request")    
        return HttpResponse("Hello, world!")
    
# Specialties.objects.create(
#     name = '09.02.07 Информационные системы и программирование',
#     price = 48000
# )

# Enrollee.objects.filter(id=1).update(idSpecialties=1)