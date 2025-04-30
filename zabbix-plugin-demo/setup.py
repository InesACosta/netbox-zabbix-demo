from setuptools import setup, find_packages

setup(
    name='netbox-zabbix-plugin',
    version='0.1.0',
    description='Adds a Zabbix link tab to NetBox devices',
    author='Inês Costa',
    packages=find_packages(),
    install_requires=[],  # no extra deps
    entry_points={
        'netbox.plugins': [
            'netbox_zabbix_plugin = netbox_zabbix_plugin.config:ZabbixPluginConfig'
        ]
    }
)
