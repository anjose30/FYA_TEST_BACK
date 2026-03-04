from rest_framework import status
from credit.serializers.Sz_credit import Sz_credit
from credit.models.M_credit import Credit
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework import filters
from credit.utils.email_utils import send_async_email  # <-- Importar
from django.conf import settings  # <-- Importar settings

class V_credit_create(CreateAPIView):
    queryset = Credit.objects.all()
    serializer_class = Sz_credit

    def perform_create(self, serializer):
        credit = serializer.save()
        
        # Preparar mensaje
        subject = 'Nuevo crédito registrado'
        message = f"""
        Se ha registrado un nuevo crédito:
        
        Nombre: {credit.full_name}
        Documento: {credit.dni}
        Valor: ${credit.credit_value}
        Intereses: {credit.interests}%
        Plazo: {credit.months} meses
        """
        
        try:
            send_async_email(
                subject,
                message,
                [settings.EMAIL_DESTINATION]
            )
        except Exception as e:
            return Response(
                {"error_email": str(e)},
                status=500
            )
        
        return credit

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            credit = serializer.save()

            subject = 'Nuevo crédito registrado'
            message = f"""
            Se ha registrado un nuevo crédito:
            
            Nombre: {credit.full_name}
            Documento: {credit.dni}
            Valor: ${credit.credit_value}
            Intereses: {credit.interests}%
            Plazo: {credit.months} meses
            """

            try:
                send_async_email(
                    subject,
                    message,
                    [settings.EMAIL_DESTINATION]
                )
            except Exception as e:
                return Response(
                    {"error_email": str(e)},
                    status=500
                )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=400)

class V_credit_list(ListAPIView):
    queryset = Credit.objects.all()
    serializer_class = Sz_credit
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'full_name', 'dni', 'created_at'] 
    ordering = ['-id'] 

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)

        if search:
            queryset = queryset.filter(
                Q(full_name__icontains=search) |
                Q(dni__icontains=search)
            )

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response(
                {'message': 'No se encontraron créditos'},
                status=status.HTTP_404_NOT_FOUND
            )

        return super().get(request, *args, **kwargs)