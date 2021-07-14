from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from catalog_products import views
from rest_framework import routers
from django.conf import settings


router = routers.DefaultRouter()
router.register(r'CATEGORIES_FOR_EDIT',
                views.CategoryAllViewSet, 'category_list'),
router.register(r'PRODUCTS_FOR_EDIT', views.ProductAllViewSet, 'product_list')


urlpatterns = [
    path('', include(router.urls)),
    path('TASK_1/', views.Task1ViewSet.as_view()),
    path('TASK_2/', views.Task2ViewSet.as_view()),
    path('TASK_3/', views.Task3ViewSet.as_view()),
    path('TASK_4/', views.Task4ViewSet.as_view()),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
