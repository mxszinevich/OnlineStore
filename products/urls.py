from rest_framework import routers

from products.views import ProductsView, CartView, CustomerOrderView, OrderView, ScoreView, OrderPaymentsView

router = routers.SimpleRouter()
router.register('products', ProductsView)
router.register('order', CustomerOrderView, basename='order')
router.register('cart', CartView, basename='cart')
router.register('score', ScoreView, basename='score')
router.register('admin/order', OrderView, basename='admin-order')
router.register('payments', OrderPaymentsView, basename='payments')
urlpatterns = router.urls

# urlpatterns = [
#     path('products/', ProductsView.as_view({'get': 'list'})),
#     path('products/<int:pk>', ProductsView.as_view({'get': 'retrieve'})),
#     path('order/', CustomerOrderView.as_view({'post': 'create', 'get': 'list'})),
#     path('order/<int:pk>', CustomerOrderView.as_view({'get': 'retrieve'})),
#     path('cart/', CartView.as_view({'post': 'create', 'get': 'list'})),
#     path('score/', ScoreView.as_view({'post': 'create', 'get': 'list'})),
#     path('score/<int:pk>', ScoreView.as_view({'get': 'retrieve'})),
#     path('admin/order/<int:pk>', OrderView.as_view({'put': 'update'})),
#     path('admin/order/', OrderView.as_view({'get': 'list'})),
# ]
