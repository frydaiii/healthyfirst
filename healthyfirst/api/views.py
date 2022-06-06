import os.path

from django.http import HttpResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from healthyfirst.api.serializers import PersonSerializer, PremiseSerializer, CertificateSerializer, \
    BusinessTypeSerializer, InspectionPlanSerializer, SampleSerializer, AreaSerializer
from healthyfirst.api.models import Person, Premise, Certificate, BusinessType, InspectionPlan, Sample, Area
from healthyfirst.api.permissions import PersonPermission, PremisePermission, CertificatePermission, \
    BusinessTypePermission, InspectionPlanPermission, SamplePermission, AreaPermission
from healthyfirst.utils.gen_form import GenForm
from healthyfirst.utils.pdf import PDF


class PersonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    serializer_class = PersonSerializer
    authentication_classes = [JWTAuthentication]
    queryset = Person.objects.all()
    lookup_field = 'username'

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        else:
            return [IsAuthenticated(), PersonPermission()]


class PremiseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows action on premises
    """

    serializer_class = PremiseSerializer
    queryset = Premise.objects.all()
    permission_classes = [IsAuthenticated, PremisePermission]


class CertificateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows actions on certificates
    """

    serializer_class = CertificateSerializer
    queryset = Certificate.objects.all()
    permission_classes = [IsAuthenticated, CertificatePermission]


class BusinessTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows actions on business type
    """

    serializer_class = BusinessTypeSerializer
    queryset = BusinessType.objects.all()
    permission_classes = [IsAuthenticated, BusinessTypePermission]


class InspectionPlanViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows actions on inspection plan
    """

    serializer_class = InspectionPlanSerializer
    queryset = InspectionPlan.objects.all()
    permission_classes = [IsAuthenticated, InspectionPlanPermission]


class SampleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows actions on sample
    """

    serializer_class = SampleSerializer
    queryset = Sample.objects.all()
    permission_classes = [IsAuthenticated, SamplePermission]


class AreaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows actions on area
    """

    serializer_class = AreaSerializer
    queryset = Area.objects.all()
    permission_classes = [IsAuthenticated, AreaPermission]


@csrf_exempt
def generate_form(request, cert_id):

    # data = QueryDict(request.body).dict()
    cert_instance = Certificate.objects.get(id=cert_id)
    pdf_path = cert_instance.file_path
    if pdf_path is None or pdf_path == '' or os.path.isfile(pdf_path):
        pdf_path = GenForm(cert_id=cert_id).gen_file()
        cert_instance.file_path = pdf_path
        cert_instance.save()
    with open(pdf_path, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=some_file.pdf'
        return response
    # response = HttpResponse(pdf.output(), content_type='application/pdf')
    # response['Content-Disposition'] = "attachment; filename='file_name.pdf'"
    # return response
