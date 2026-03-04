from django.urls import path

from credit.views.V_credit import V_credit_create, V_credit_list
from credit.views.V_choice import get_choices_credit

urlpatterns = [
	path('create/', V_credit_create.as_view(), name='credit-create'),
	path('list/', V_credit_list.as_view(), name='credit-list'),
    path('choices/', get_choices_credit, name='credit-choices'),
]
