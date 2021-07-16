from rest_framework.views import APIView
from .serializers import CategorySerializer, ProductSerializer
from .models import Category, Product
from rest_framework import viewsets
from rest_framework.response import Response


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
        category_all = Category.objects.values()
        category_without_parent = []
        category_with_parent = []
        cat_name_with_par = []
        for category in category_all:
            if category.get('parent_id') is not None:
                category_with_parent.append(category)
            else:
                category_without_parent.append(category)
        for cat_wp in category_with_parent:
            category_name = cat_wp.get('name')
            cat_par_name = list(filter
                                (lambda x: x.get('id') ==
                                 cat_wp.get('parent_id'),
                                 category_all))[0].get('name')
            cat_name_with_par.append(
                f'Subcat: {category_name}, parcat: {cat_par_name}'
                )
        name_key = 'name'
        category_name_witt_parent = list(map(
            lambda category:
            f'Subcategory: {category.get(name_key)} hvnt parcat!',
            category_without_parent
            ))
        return Response(cat_name_with_par + category_name_witt_parent)


class Task2ViewSet(APIView):
    serializer_class = CategorySerializer

    def get(self, request):
        category_all = Category.objects.values()

        def get_recurs(category):
            subcategory_count = 0
            for cat in category_all:
                if cat.get('parent_id') == category.get('id'):
                    subcategory_count += 1
                    subcategory_count += get_recurs(cat)
            return subcategory_count

        result = []
        for cat in category_all:
            category_name = cat.get('name')
            result.append(
                f'Category: {category_name} - Subcat: {get_recurs(cat)}'
                )
        return Response(result)


class Task3ViewSet(APIView):
    def get(self, request):
        all_categories = Category.objects.values()
        products = Product.objects.values()
        dict_categories = dict((el.get('name'), 0) for el in all_categories)

        def increment_parents_products(cat):
            for category in all_categories:
                if category.get('id') == cat.get('parent_id'):
                    target_parent = list(filter(
                        lambda x: x.get('id') == cat.get('parent_id'),
                        all_categories))[0]
                    dict_categories[target_parent.get('name')] += 1
                    return increment_parents_products(target_parent)

        for cat in all_categories:
            for product in products:
                if product.get('category_id') == cat.get('id'):
                    dict_categories[cat.get('name')] += 1
                    increment_parents_products(cat)

        result = []
        for key, value in dict_categories.items():
            result.append(f'Category: {key}, products: {value}')
        return Response(result)


class Task4ViewSet(APIView):
    def get(self, request):
        all_categories = Category.objects.values()
        products = Product.objects.values()
        dict_categories = dict((el.get('name'), []) for el in all_categories)

        def append_to_parent(cat, value):
            for category in all_categories:
                if category.get('id') == cat.get('parent_id'):
                    target_parent = list(filter(
                        lambda x: x.get('id') == cat.get('parent_id'),
                        all_categories))[0]
                    dict_categories[target_parent.get('name')].append(value)
                    return append_to_parent(target_parent, value)

        for cat in all_categories:
            for product in products:
                if product.get('category_id') == cat.get('id'):
                    dict_categories[cat.get('name')].append(
                        product.get('name')
                        )
                    append_to_parent(cat, product.get('name'))

        result = []
        for key, value in dict_categories.items():
            products_value = ', '.join(value)
            result.append(f'{key} - {products_value}')
        return Response(result)
