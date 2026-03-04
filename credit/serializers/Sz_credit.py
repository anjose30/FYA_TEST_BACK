from rest_framework.serializers import ModelSerializer
from credit.models import M_credit

class Sz_credit(ModelSerializer):
    class Meta:
        model = M_credit.Credit
        fields = ['full_name', 'type_dni', 'dni', 'credit_value', 'interests', 'months']
