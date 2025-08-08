from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from ..models import Category
from ..serializers import CategorySerializer
from django.shortcuts import get_object_or_404


class CategoryGetView(APIView):
    @extend_schema(
        summary="Получить список категорий",
        tags=['Категории'],
        parameters=[
            OpenApiParameter("id", int, required=False, description="ID категории"),
            OpenApiParameter("type", int, required=False, description="Фильтр по ID типа")
        ],
        responses={
            200: OpenApiResponse(response=CategorySerializer(many=True), description="Список категорий"),
            404: OpenApiResponse(description="Категория не найдена")
        },
    )
    def get(self, request):
        category_id = request.query_params.get('id')
        type_id = request.query_params.get('type')

        if category_id:
            instance = get_object_or_404(Category, id=category_id)
            serializer = CategorySerializer(instance)
            return Response(serializer.data)

        queryset = Category.objects.all()
        if type_id:
            queryset = queryset.filter(type_id=type_id)

        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)


class CategorySaveView(APIView):
    @extend_schema(
        summary="Создать или обновить категорию",
        tags=['Категории'],
        request=CategorySerializer,
        responses={
            200: OpenApiResponse(response=CategorySerializer, description="Категория успешно обновлена"),
            201: OpenApiResponse(response=CategorySerializer, description="Категория успешно создана"),
            400: OpenApiResponse(description="Ошибка валидации")
        },
    )
    def post(self, request):
        category_id = request.data.get('id')

        if category_id:
            instance = get_object_or_404(Category, id=category_id)
            serializer = CategorySerializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDeleteView(APIView):
    @extend_schema(
        summary="Удалить категорию",
        tags=['Категории'],
        request=OpenApiParameter(name='ids', description='Список ID для удаления', required=True, type=list),
        responses={
            204: OpenApiResponse(description="Категории успешно удалены"),
            400: OpenApiResponse(description="Неверный формат запроса"),
        },
    )
    def post(self, request):
        ids = request.data.get('ids')
        deleted_count, _ = Category.objects.filter(id__in=ids).delete()
        return Response({"deleted": deleted_count}, status=status.HTTP_200_OK)
