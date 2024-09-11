from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer, ProductDetailSerializer, EnhancedOrderSerializer

class ProductListAPI(generics.ListAPIView):
    queryset = Product.objects.filter(quantity_in_stock__gt=0)
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        products = self.get_queryset()
        return render(request, 'product_list.html', {'products': products})

class ProductDetailAPI(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

class OrderCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        return render(request, 'create_order.html', {'products': products})

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity', 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return render(request, 'create_order.html', {
                'products': Product.objects.all(),
                'error': "The selected product does not exist."
            })

        if product.quantity_in_stock < int(quantity):
            return render(request, 'create_order.html', {
                'products': Product.objects.all(),
                'error': f"Sorry, only {product.quantity_in_stock} units of {product.name} are available in stock."
            })

        total_amount = product.price * int(quantity)
        order_data = {
            'user': request.user.id,
            'items': [{'product_id': product_id, 'quantity': quantity}],
            'total_amount': total_amount
        }

        serializer = OrderSerializer(data=order_data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return render(request, 'create_order.html', {
                'products': Product.objects.all(),
                'success': "Order placed successfully!"
            })
        else:
            return render(request, 'create_order.html', {
                'products': Product.objects.all(),
                'error': "Failed to place the order. Please try again."
            })

class UserOrderListAPI(generics.ListAPIView):
    serializer_class = EnhancedOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return render(request, 'user_orders.html', {'orders': serializer.data})

def home(request):
    return render(request, 'home.html')
