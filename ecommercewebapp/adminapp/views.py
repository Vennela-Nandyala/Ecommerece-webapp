from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from shop.models import Product
from shop.serializer import ProductSerializer

def test_view(request):
    return JsonResponse({"message": "Test view is working!"})

class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)