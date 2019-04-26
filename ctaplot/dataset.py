import pkg_resources
from os.path import join

__all__ = ['get']


def get(resource_name, data_dir = 'data'):
    """ get the filename for a resource """
    resource_path = join(data_dir, resource_name)
    if not pkg_resources.resource_exists(__name__, resource_path):
        raise FileNotFoundError("Couldn't find resource: '{}'"
                                .format(resource_path))
    return pkg_resources.resource_filename(__name__, resource_path)

