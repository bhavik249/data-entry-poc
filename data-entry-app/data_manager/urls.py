from django.urls import path
from data_manager.views import *

urlpatterns = [
    path("", InventoryListView.as_view(), name="home"),
    path('create/', EventCreate.as_view(), name='event-create'),
    path('<int:pk>/update/', EventUpdate.as_view(), name='event-update'),
    path('<int:pk>/delete/', EventDelete.as_view(), name='event-delete'),
    path('importevent/', BulkEventCreate.as_view(), name='bulk-event-create')
]