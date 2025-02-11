from .extension import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'username', 'balance')

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('product_id', 'name', 'price')

class OrderSchema(ma.Schema):
    class Meta:
        fields = ('oder_id', 'user_id', 'total_price', 'status')

class OrderDetailsSchema(ma.Schema):
    class Meta:
        fields = ('oder_id', 'user_id', 'product_id', 'quantity', 'unit_price', 'payment_method')