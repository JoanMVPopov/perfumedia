from django.http import HttpResponse

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .serializer import ProductSerializer

# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

class LatestProductsList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()[0:4]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)