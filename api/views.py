from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProductSerializer
from product.models import Product


class TestView(APIView):
    def get(self, request, *args, **kwargs):
        qs = Product.objects.all()
        serializer = ProductSerializer(qs, many=True)
        return Response(serializer.data)
