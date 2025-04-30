import django_tables2 as tables
from django_tables2.utils import A
from netbox.tables import NetBoxTable
from .models import DiscoveredHost

class DiscoveredHostTable(NetBoxTable):
    name = tables.LinkColumn(
        'plugins:netbox_zabbix_plugin:discoveredhost',
        args=[A('pk')],
        verbose_name='Name'
    )

    class Meta(NetBoxTable.Meta):
        model = DiscoveredHost
        fields = ('hostid','name','ip_address', 'os')
        default_columns = ('hostid','name','ip_address', 'os')
        order_by = ('hostid',)
        actions         = ()
