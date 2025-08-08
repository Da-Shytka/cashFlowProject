from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from ..models import Subcategory
from ..serializers import SubcategorySerializer
from django.shortcuts import get_object_or_404


class SubcategoryGetView(APIView):
    @extend_schema(
        summary="Получить список подкатегорий или одну подкатегорию по ID",
        tags=['Подкатегории'],
        parameters=[
            OpenApiParameter("id", int, required=False, description="ID подкатегории"),
            OpenApiParameter("category", int, required=False, description="Фильтр по ID категории")
        ],
        responses={
            200: OpenApiResponse(response=SubcategorySerializer(many=True), description="Список подкатегорий"),
            404: OpenApiResponse(description="Подкатегория не найдена")
        },
    )
    def get(self, request):
        subcat_id = request.query_params.get('id')
        category_id = request.query_params.get('category')

        if subcat_id:
            instance = get_object_or_404(Subcategory, id=subcat_id)
            serializer = SubcategorySerializer(instance)
            return Response(serializer.data)

        queryset = Subcategory.objects.all()
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        serializer = SubcategorySerializer(queryset, many=True)
        return Response(serializer.data)


class SubcategorySaveView(APIView):
    @extend_schema(
        summary="Создать или обновить подкатегорию",
        tags=['Подкатегории'],
        request=SubcategorySerializer,
        responses={
            200: OpenApiResponse(response=SubcategorySerializer, description="Подкатегория успешно обновлена"),
            201: OpenApiResponse(response=SubcategorySerializer, description="Подкатегория успешно создана"),
            400: OpenApiResponse(description="Ошибка валидации")
        },
    )
    def post(self, request):
        subcat_id = request.data.get('id')

        if subcat_id:
            instance = get_object_or_404(Subcategory, id=subcat_id)
            serializer = SubcategorySerializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = SubcategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubcategoryDeleteView(APIView):
    @extend_schema(
        summary="Удалить одну или несколько подкатегорий",
        tags=['Подкатегории'],
        request=OpenApiParameter(name='ids', description='Список ID для удаления', required=True, type=list),
        responses={
            204: OpenApiResponse(description="Подкатегории успешно удалены"),
            400: OpenApiResponse(description="Неверный формат запроса"),
        },
    )
    def post(self, request):
        ids = request.data.get('ids')

        if not isinstance(ids, list) or not all(isinstance(i, int) for i in ids):
            return Response({"detail": "Ожидается список числовых ID в поле 'ids'"}, status=status.HTTP_400_BAD_REQUEST)

        deleted_count, _ = Subcategory.objects.filter(id__in=ids).delete()
        return Response({"deleted": deleted_count}, status=status.HTTP_200_OK)