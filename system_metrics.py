import psutil
import json


def unit_conversion(byte):
    if byte/(1024*1024*1024) > 1:
        return {'size': round(byte/(1024*1024*1024), 1), 'unit': 'GiB'}
    if byte/(1024*1024) > 2:
        return {'size': round(byte/(1024*1024), 1), 'unit': 'MiB'}
    if byte/1024 > 2:
        return {'size': round(byte/1024, 1), 'unit': 'KiB'}
    return {'size': byte, 'unit': 'B'}


def get_metrics():
    cpu_usage = round(psutil.cpu_percent(interval=.1), 1)
    ram_data = dict(psutil.virtual_memory()._asdict())
    disk_usage = dict(psutil.disk_usage('/')._asdict())

    ram_total = unit_conversion(int(ram_data.get('total')))
    ram_available = unit_conversion(int(ram_data.get('available')))
    ram_used = unit_conversion(int(ram_data.get('used')))
    ram_wired = unit_conversion(int(ram_data.get('wired')))
    ram_active = unit_conversion(int(ram_data.get('active')))
    ram_inactive = unit_conversion(int(ram_data.get('inactive')))
    ram_free = unit_conversion(int(ram_data.get('free')))
    ram_free_percent = round((ram_data.get('free') / ram_data.get('total')) * 100, 1)

    disk_total = unit_conversion(int(disk_usage.get('total')))
    disk_used = unit_conversion(int(disk_usage.get('used')))
    disk_free = unit_conversion(int(disk_usage.get('free')))
    disk_usage_percent = round(int(disk_usage.get('percent')), 1)

    metric_data = {
        'cpu': cpu_usage,
        'ram': {
            'total': ram_total,
            'available': ram_available,
            'used': ram_used,
            'wired': ram_wired,
            'active': ram_active,
            'inactive': ram_inactive,
            'free': ram_free,
            'free_percent': ram_free_percent
        },
        'disk': {
            'total': disk_total,
            'used': disk_used,
            'free': disk_free,
            'free_percent': 100-disk_usage_percent
        }
    }

    return metric_data


print(json.dumps(get_metrics(), indent=4, sort_keys=True))
