from rest_framework import routers

from products.views import (
    ProductsView,
    CartView,
    CustomerOrderView,
    OrderView,
    ScoreView,
    OrderPaymentsView
)

router = routers.SimpleRouter()
router.register('products', ProductsView, basename='products')
router.register('order', CustomerOrderView, basename='order')
router.register('cart', CartView, basename='cart')
router.register('score', ScoreView, basename='score')
router.register('admin/order', OrderView, basename='admin-order')
router.register('payments', OrderPaymentsView, basename='payments')
urlpatterns = router.urls

