from django.urls import path
from .views import index, CSVUploadView, QueryDataView

urlpatterns = [
    path('', index, name='index'),
    path('upload/', CSVUploadView.as_view(), name='upload_csv'),
    path('query/', QueryDataView.as_view(), name='query_data'),
]
