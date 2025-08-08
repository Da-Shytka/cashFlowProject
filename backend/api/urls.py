from django.urls import path
from api.views.TypeViews import (TypeGetView, TypeSaveView, TypeDeleteView)
from api.views.StatusViews import (StatusGetView, StatusSaveView, StatusDeleteView)
from api.views.CategoryViews import (CategoryGetView, CategorySaveView, CategoryDeleteView)
from api.views.SubcategoryViews import (SubcategoryGetView, SubcategorySaveView, SubcategoryDeleteView)
from api.views.OperationViews import (OperationGetView, OperationSaveView, OperationDetailView, OperationDeleteView)


urlpatterns = [
    path('type/getlist', TypeGetView.as_view(), name='type-get'),
    path('type/save', TypeSaveView.as_view(), name='type-save'),
    path('type/delete', TypeDeleteView.as_view(), name='type-delete'),


    path('status/getlist', StatusGetView.as_view(), name='status-get'),
    path('status/save', StatusSaveView.as_view(), name='status-save'),
    path('status/delete', StatusDeleteView.as_view(), name='status-delete'),

    
    path('category/getlist', CategoryGetView.as_view(), name='category-get'),
    path('category/save', CategorySaveView.as_view(), name='category-save'),
    path('category/delete', CategoryDeleteView.as_view(), name='category-delete'),


    path('subcategory/getlist', SubcategoryGetView.as_view(), name='subcategory-get'),
    path('subcategory/save', SubcategorySaveView.as_view(), name='subcategory-save'),
    path('subcategory/delete', SubcategoryDeleteView.as_view(), name='subcategory-delete'),
    
    
    path('operation/getlist', OperationGetView.as_view(), name='operation-get'),
    path('operation/save', OperationSaveView.as_view(), name='operation-save'),
    path('operations/<int:pk>/', OperationDetailView.as_view(), name='operation-detail'),
    path('operation/delete', OperationDeleteView.as_view(), name='operation-delete'),
]
