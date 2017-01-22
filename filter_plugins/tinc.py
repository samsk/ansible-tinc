from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.utils.listify import listify_lookup_plugin_terms

def to_tinc_host(inString):
 return inString.replace('.', '_').replace('-', '__')

class FilterModule(object):
    def filters(self):
        return {
            'to_tinc_host': to_tinc_host
}
