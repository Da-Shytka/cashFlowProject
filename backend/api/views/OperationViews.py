from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample
from ..models import Operation
from ..serializers import OperationSerializer
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date


class OperationGetView(APIView):
    @extend_schema(
        summary="Получить список операций или одну по ID",
        tags=['Операции'],
        parameters=[
            OpenApiParameter("id", int, required=False, description="ID операции"),
            OpenApiParameter("start_date", str, required=False, description="Дата начала периода (YYYY-MM-DD)"),
            OpenApiParameter("end_date", str, required=False, description="Дата конца периода (YYYY-MM-DD)"),
            OpenApiParameter("status", int, required=False),
            OpenApiParameter("type", int, required=False),
            OpenApiParameter("category", int, required=False),
            OpenApiParameter("subcategory", int, required=False),
        ],
        responses={
            200: OpenApiResponse(response=OperationSerializer(many=True), description="Список операций"),
            404: OpenApiResponse(description="Операция не найдена")
        },
    )
    def get(self, request):
        operation_id = request.query_params.get('id')
        if operation_id:
            instance = get_object_or_404(Operation, id=operation_id)
            serializer = OperationSerializer(instance)
            return Response(serializer.data)

        queryset = Operation.objects.all()

        # фильтрация
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(date__range=(parse_date(start_date), parse_date(end_date)))

        for field in ['status', 'type', 'category', 'subcategory']:
            value = request.query_params.get(field)
            if value:
                queryset = queryset.filter(**{f"{field}_id": value})

        serializer = OperationSerializer(queryset, many=True)
        return Response(serializer.data)


class OperationSaveView(APIView):
    @extend_schema(
        summary="Создать или обновить операцию",
        tags=['Операции'],
        request=OperationSerializer,
        responses={
            200: OpenApiResponse(response=OperationSerializer, description="Операция обновлена"),
            201: OpenApiResponse(response=OperationSerializer, description="Операция создана"),
            400: OpenApiResponse(description="Ошибка валидации")
        },
    )
    def post(self, request):
        operation_id = request.data.get('id')
        if operation_id:
            instance = get_object_or_404(Operation, id=operation_id)
            serializer = OperationSerializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = OperationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OperationDetailView(APIView):
    @extend_schema(
        summary="Получить детальную информацию об операции по ID",
        tags=['Операции'],
        responses={
            200: OpenApiResponse(response=OperationSerializer, description="Детали операции"),
            404: OpenApiResponse(description="Операция не найдена")
        },
        examples=[
            OpenApiExample(
                'Пример запроса',
                value={'id': 1},
                request_only=True,
                response_only=False
            ),
        ]
    )
    def get(self, request, pk):
        instance = get_object_or_404(Operation, id=pk)
        serializer = OperationSerializer(instance)
        return Response(serializer.data)


class OperationDeleteView(APIView):
    @extend_schema(
        summary="Удалить одну или несколько операций",
        tags=['Операции'],
        request=OpenApiParameter(name='ids', description='Список ID для удаления', required=True, type=list),
        responses={
            204: OpenApiResponse(description="Операции успешно удалены"),
            400: OpenApiResponse(description="Неверный формат запроса"),
        },
    )
    def post(self, request):
        ids = request.data.get('ids')

        if not isinstance(ids, list) or not all(isinstance(i, int) for i in ids):
            return Response({"detail": "Ожидается список числовых ID в поле 'ids'"}, status=status.HTTP_400_BAD_REQUEST)

        deleted_count, _ = Operation.objects.filter(id__in=ids).delete()
        return Response({"deleted": deleted_count}, status=status.HTTP_200_OK)