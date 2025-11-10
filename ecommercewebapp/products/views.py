from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer
from myapp.permission import IsAdmin
from .models import Product
class AdminProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdmin]