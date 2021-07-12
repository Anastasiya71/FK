from typing import Dict
from django.http.response import JsonResponse
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from catalog_products.serializers import CategorySerializer, ProductSerializer
from catalog_products.models import Category, Product
from rest_framework import viewsets


class CategoryAllViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ProductAllViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class Task1ViewSet(APIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    def get(self, request):
        category_all = Category.objects.all()
        category_without_parent = []
        category_with_parent = []
        for category in category_all:
            if category.parent != None:
                category_with_parent.append(category)
            else:
                category_without_parent.append(category)
        category_name_with_parent = list(map(lambda category: f'Subcategory: {category.name}, parent category: {category.parent.name}',category_with_parent))
        category_name_without_parent = list(map(lambda category: f'Subcategory: {category.name} havent parent category!',category_without_parent))      
        return JsonResponse(category_name_with_parent + category_name_without_parent, safe=False)


class Task2ViewSet(APIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request):
        def get_count_recoursively(category):
            category_all = Category.objects.all()
            subcategory_count = 0
            for cat in category_all:
                if cat.parent == category:
                    subcategory_count += 1
                    subcategory_count += get_count_recoursively(cat)
            return subcategory_count

        category_all = Category.objects.all()
        result = []
        for category in category_all:
            result.append(f'Category: {category.name} - Subcategory: {get_count_recoursively(category)}')
        return JsonResponse(result, safe=False)



class Task3ViewSet(APIView):
    def get(self, request):
        all_categories = Category.objects.all()
        products = Product.objects.all()
        dict_categories = dict((el, 0) for el in all_categories)
        
        def increment_parents_products(cat):
            for category in all_categories:
                if category == cat.parent:
                    dict_categories[cat.parent] += 1
                    return increment_parents_products(cat.parent)

        for cat in all_categories:
            for product in products:
                if product.category == cat:
                    dict_categories[cat] +=1
                    increment_parents_products(cat)

        result = []
        for key, value in dict_categories.items():
            result.append(f'Category: {key}, products: {value}')
        return JsonResponse(result, safe=False)


class Task4ViewSet(APIView):
    def get(self, request):
        all_categories = Category.objects.all()
        products = Product.objects.all()
        dict_categories = dict((el, []) for el in all_categories)
        
        def append_to_parent(cat, value):
            for category in all_categories:
                if category == cat.parent:
                    dict_categories[cat.parent].append(value)
                    return append_to_parent(cat.parent, value)

        for cat in all_categories:
            for product in products:
                if product.category == cat:
                    dict_categories[cat].append(product.name)
                    append_to_parent(cat, product.name)

        result = []
        for key, value in dict_categories.items():
            products_value = ', '.join(value)
            result.append(f'{key} - {products_value}')
        return JsonResponse(result, safe=False)






            


       