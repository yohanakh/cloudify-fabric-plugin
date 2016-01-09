"""This implementation of ctx is still lacking and does not contain
all features the actual ctx object provides.
"""

import subprocess
import json


class CtxLogger(object):
    def _logger(self, message, level='info'):
        cmd = ['ctx', 'logger', level, message]
        return subprocess.check_output(cmd)

    def info(self, message):
        return self._logger(level='info', message=message)


# TODO: set immutable properties here.
class CtxNodeProperties(object):
    def __getitem__(self, property_name):
        cmd = ['ctx', '-j', 'node', 'properties', property_name]
        return json.loads(subprocess.check_output(cmd))

    def get(self, property_name, returns=None):
        return self.__getitem__(property_name) or returns


class CtxNode(object):
    @property
    def properties(self):
        return CtxNodeProperties()


class CtxInstanceRuntimeProperties(object):
    def __init__(self, relationship_type=None):
        self.relationship_type = relationship_type

    def __getitem__(self, property_name):
        cmd = ['ctx', '-j', 'instance', 'runtime_properties', property_name]
        if self.relationship_type:
            cmd.insert(2, self.relationship_type)
        return json.loads(subprocess.check_output(cmd))

    def get(self, property_name, returns=None):
        return self.__getitem__(property_name) or returns

    def __setitem__(self, property_name, value):
        cmd = ['ctx', 'instance', 'runtime_properties', property_name,
               '@"{0}"'.format(value)]
        if self.relationship_type:
            cmd.insert(2, self.relationship_type)
        return subprocess.check_output(cmd)


class CtxNodeInstance(object):
    def __init__(self, relationship_type=None):
        self.relationship_type = relationship_type

    @property
    def runtime_properties(self):
        return CtxInstanceRuntimeProperties(self.relationship_type)

    @property
    def host_ip(self):
        cmd = ['ctx', 'instance', 'host_ip']
        return subprocess.check_output(cmd)

    @property
    def id(self):
        cmd = ['ctx', 'instance', 'id']
        return subprocess.check_output(cmd)

    @property
    def relationships(self):
        cmd = ['ctx', 'instance', 'relationships']
        return subprocess.check_output(cmd)


class CtxRelationshipInstance(object):
    def __init__(self, relationship_type):
        self.relationship_type = relationship_type

    @property
    def instance(self):
        return CtxNodeInstance(self.relationship_type)


class Ctx(object):
    def __init__(self):
        self._logger = CtxLogger()
        self._node = CtxNode()
        self._instance = CtxNodeInstance()
        self._target = CtxRelationshipInstance('target')
        self._source = CtxRelationshipInstance('source')

    @property
    def node(self):
        return self._node

    @property
    def instance(self):
        return self._instance

    @property
    def target(self):
        return self._target

    @property
    def source(self):
        return self._source

    @property
    def logger(self):
        return self._logger

    def download_resource(self, source, destination=None):
        cmd = ['ctx', 'download-resource', source]
        if destination:
            cmd.append(destination)
        return subprocess.check_output(cmd)

    def download_resource_and_render(self, source, destination=None,
                                     params=None):
        cmd = ['ctx', 'download-resource-and-render', source]
        if destination:
            cmd.append(destination)
        if params:
            cmd.append(params)
        return subprocess.check_output(cmd)


ctx = Ctx()
