from importlib import import_module


class ServiceDoesNotExist(Exception):
    pass


def get_service_class_by_name(name):
    service_module_path = 'social_content.services.%s_service' % (name)
    service_class_name = 'Service'

    try:
        service_module = import_module(service_module_path)
        return getattr(service_module, service_class_name)
    except (ImportError, AttributeError):
        raise ServiceDoesNotExist('Social content service class not found under: %s' % service_module_path)
