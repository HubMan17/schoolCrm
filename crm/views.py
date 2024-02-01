from django.http import HttpResponse, JsonResponse
from django.db.models import Avg, Min, Max, Sum
from .models import *


def index(request):
    return HttpResponse("Hello, world!")

def api_crm(request):
    return JsonResponse({
        'message': 'Something new',
        'status': 200,
    })

def api_crm_get_stages(request):
    data = StudentBoard.objects.exclude(id=1).order_by("position").values('id', 'name', 'position', 'color')
    
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
# Specialties.objects.create(
#     name = '09.02.07 Информационные системы и программирование',
#     price = 48000
# )

# Enrollee.objects.filter(id=1).update(idSpecialties=1)