from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from ..models import Status
from ..serializers import StatusSerializer
from django.shortcuts import get_object_or_404


class StatusGetView(APIView):
    @extend_schema(
        summary="Получить список статусов или один статус по ID",
        tags=['Статусы'],
        parameters=[OpenApiParameter("id", int, required=False, description="ID статуса")],
        responses={
            200: OpenApiResponse(response=StatusSerializer(many=True), description="Список статусов"),
            404: OpenApiResponse(description="Статус не найден")
        },
    )
    def get(self, request):
        status_id = request.query_params.get('id')

        if status_id:
            instance = get_object_or_404(Status, id=status_id)
            serializer = StatusSerializer(instance)
            return Response(serializer.data)
        else:
            queryset = Status.objects.all()
            serializer = StatusSerializer(queryset, many=True)
            return Response(serializer.data)


class StatusSaveView(APIView):
    @extend_schema(
        summary="Создать или обновить статус",
        tags=['Статусы'],
        request=StatusSerializer,
        responses={
            200: OpenApiResponse(response=StatusSerializer, description="Статус успешно обновлён"),
            201: OpenApiResponse(response=StatusSerializer, description="Статус успешно создан"),
            400: OpenApiResponse(description="Ошибка валидации")
        },
    )
    def post(self, request):
        status_id = request.data.get('id')

        if status_id:
            instance = get_object_or_404(Status, id=status_id)
            serializer = StatusSerializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = StatusSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StatusDeleteView(APIView):
    @extend_schema(
        summary="Удалить один или несколько статусов",
        tags=['Статусы'],
        request=OpenApiParameter(name='ids', description='Список ID для удаления', required=True, type=list),
        responses={
            204: OpenApiResponse(description="Статусы успешно удалены"),
            400: OpenApiResponse(description="Неверный формат запроса"),
        },
    )
    def post(self, request):
        ids = request.data.get('ids')

        if not isinstance(ids, list) or not all(isinstance(i, int) for i in ids):
            return Response({"detail": "Ожидается список числовых ID в поле 'ids'"}, status=status.HTTP_400_BAD_REQUEST)

        deleted_count, _ = Status.objects.filter(id__in=ids).delete()
        return Response({"deleted": deleted_count}, status=status.HTTP_200_OK)