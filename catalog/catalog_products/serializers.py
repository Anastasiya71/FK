from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from catalog_products.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent']

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.parent = validated_data.get('parent', instance.parent)
        instance.save()
        return instance


def FilteredCategoriesQuerySet():
    categories_ids_list = []
    category_all = Category.objects.all()

    def fill_with_empty_cat_recoursively(category):
        subcategory_count = 0
        for cat in category_all:
            if cat.parent == category:
                subcategory_count += 1
                subcategory_count += fill_with_empty_cat_recoursively(cat)
        if subcategory_count == 0 and category.id not in categories_ids_list:
            categories_ids_list.append(category.id)
        return subcategory_count

    for cat in category_all:
        fill_with_empty_cat_recoursively(cat)

    return Category.objects.filter(id__in=categories_ids_list)


class ProductSerializer(serializers.ModelSerializer):
    category = PrimaryKeyRelatedField(queryset=FilteredCategoriesQuerySet())

    class Meta:
        model = Product
        fields = ['id', 'name', 'category']
