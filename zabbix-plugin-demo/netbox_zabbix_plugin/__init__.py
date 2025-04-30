from netbox.plugins import PluginConfig
import pkgutil, importlib, logging

logger = logging.getLogger('netbox_zabbix_plugin')


class ZabbixPluginConfig(PluginConfig):
    name = 'netbox_zabbix_plugin'
    verbose_name = 'Zabbix Integration'
    base_url = 'zabbix'
    required_settings = ['zabbix_url', 'zabbix_api_url', 'zabbix_token']
    default_settings = {
        'zabbix_url':     'https://zabbix.e-goi.com',
        'zabbix_api_url': 'https://zabbix.e-goi.com/api_jsonrpc.php',
        'zabbix_token':   '',  # fill this in PLUGINS_CONFIG
    }

config = ZabbixPluginConfig
