from netbox.plugins import PluginMenuButton, PluginMenuItem
from netbox.choices import ButtonColorChoices


zabbix_buttons = [
    PluginMenuButton(
        link='plugins:netbox_zabbix_plugin:home',
        title="Zabbix",
        icon_class="mdi mdi-chart-bar",
    ),
]


menu_items = [
    PluginMenuItem(
        link='plugins:netbox_zabbix_plugin:home',
        link_text="Zabbix",
    ),
]