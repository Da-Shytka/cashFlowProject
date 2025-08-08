from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from ..models import Type
from ..serializers import TypeSerializer
from django.shortcuts import get_object_or_404


class TypeGetView(APIView):
    @extend_schema(
        summary="Получить список типов или один тип по ID",
        tags=['Типы'],
        parameters=[OpenApiParameter("id", int, required=False, description="ID типа")],
        responses={
            200: OpenApiResponse(response=TypeSerializer(many=True), description="Список типов"),
            404: OpenApiResponse(description="Тип не найден")
        },
    )
    def get(self, request):
        type_id = request.query_params.get('id')

        if type_id:
            instance = get_object_or_404(Type, id=type_id)
            serializer = TypeSerializer(instance)
            return Response(serializer.data)
        else:
            queryset = Type.objects.all()
            serializer = TypeSerializer(queryset, many=True)
            return Response(serializer.data)


class TypeSaveView(APIView):
    @extend_schema(
        summary="Создать или обновить тип",
        tags=['Типы'],
        request=TypeSerializer,
        responses={
            200: OpenApiResponse(response=TypeSerializer, description="Тип успешно обновлён"),
            201: OpenApiResponse(response=TypeSerializer, description="Тип успешно создан"),
            400: OpenApiResponse(description="Ошибка валидации")
        },
    )
    def post(self, request):
        type_id = request.data.get('id')

        if type_id:
            instance = get_object_or_404(Type, id=type_id)
            serializer = TypeSerializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = TypeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TypeDeleteView(APIView):
    @extend_schema(
        summary="Удалить один или несколько типов",
        tags=['Типы'],
        request=OpenApiParameter(name='ids', description='Список ID для удаления', required=True, type=list),
        responses={
            204: OpenApiResponse(description="Типы успешно удалены"),
            400: OpenApiResponse(description="Неверный формат запроса"),
        },
    )
    def post(self, request):
        ids = request.data.get('ids')

        if not isinstance(ids, list) or not all(isinstance(i, int) for i in ids):
            return Response({"detail": "Ожидается список числовых ID в поле 'ids'"}, status=status.HTTP_400_BAD_REQUEST)

        deleted_count, _ = Type.objects.filter(id__in=ids).delete()
        return Response({"deleted": deleted_count}, status=status.HTTP_200_OK)