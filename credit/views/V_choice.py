from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from credit.models.M_credit import Credit

@api_view(['GET'])
def get_choices_credit(request):
    type_dni = [{"value": value, "label": label} for value, label in Credit.TYPE_DNI_CHOICES]
    response = {
        "type_dni": type_dni
    }
    return Response(response, status=status.HTTP_200_OK)