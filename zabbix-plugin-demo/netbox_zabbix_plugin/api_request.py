from netbox.plugins import get_plugin_config

import logging, requests

class API_request():
    """
    A class to handle Zabbix API requests.
    """
    def _zabbix_api_request(payload):
        """
        Helper to send a JSON-RPC call to Zabbix using Bearer token auth.
        """
        api_url = get_plugin_config('netbox_zabbix_plugin', 'zabbix_api_url')
        token   = get_plugin_config('netbox_zabbix_plugin', 'zabbix_token')
        headers = {
            'Host': 'zabbix.e-goi.com',
            'Content-Type': 'application/json-rpc',
            'Authorization': f"Bearer {token}",
        }
        resp = requests.post(api_url, json=payload, headers=headers, verify=False)
        resp.raise_for_status()
        data = resp.json()
        if 'error' in data:
            raise RuntimeError(f"Zabbix API error: {data['error']}")
        return data['result']
