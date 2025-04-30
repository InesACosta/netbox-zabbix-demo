# netbox_zabbix_plugin/urls.py

from django.urls import path
from .views.home           import ZabbixHomeView
from .views.discovered_views import DiscoveredHostView
from netbox.views.generic import ObjectChangeLogView

app_name = 'netbox_zabbix_plugin'

urlpatterns = [
    path('',                   ZabbixHomeView.as_view(),     name='home'),
    path('hosts/<int:pk>/',    DiscoveredHostView.as_view(), name='discoveredhost'),
    path('hosts/',                DiscoveredHostView.as_view(), name='discoveredhost_list'),
    path('hosts/<int:pk>/edit/', DiscoveredHostView.as_view(), name='discoveredhost_edit'),
    path('hosts/add/',           DiscoveredHostView.as_view(), name='discoveredhost_add'),
    path('hosts/<int:pk>/delete/', DiscoveredHostView.as_view(), name='discoveredhost_delete'),
    path('hosts/<int:pk>/update/', DiscoveredHostView.as_view(), name='discoveredhost_update'),
    path('hosts/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='discoveredhost_changelog'),
    # import
    path('hosts/<int:pk>/import/', DiscoveredHostView.as_view(), name='discoveredhost_import'),
]