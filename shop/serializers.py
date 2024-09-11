from rest_framework import serializers
from .models import Product, Order, OrderItem, User

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'quantity_in_stock']

class UserDetailSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'full_name']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductDetailSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True,
        source='product'
    )

    class Meta:
        model = OrderItem
        fields = ['product', 'product_id', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    items = OrderItemSerializer(many=True, required=True)

    class Meta:
        model = Order
        fields = ['user', 'items', 'total_amount', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        order = Order.objects.create(user=self.context['request'].user, **validated_data)

        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']

            if product.quantity_in_stock < quantity:
                raise serializers.ValidationError(f"Not enough stock for {product.name}.")

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity
            )

            product.quantity_in_stock -= quantity
            product.save()

        return order


class EnhancedOrderSerializer(serializers.ModelSerializer):
    user_details = UserDetailSerializer(source='user', read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    formatted_total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['user_details', 'items', 'formatted_total_amount', 'created_at']

    def get_formatted_total_amount(self, obj):
        return f"${obj.total_amount:.2f}"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_at'] = instance.created_at.strftime('%B %d, %Y, %I:%M %p')
        return representation
