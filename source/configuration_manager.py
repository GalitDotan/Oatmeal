from six import with_metaclass, PY3
from singelton import Singleton

import json

from source.errors import ConfigurationManagerError

if PY3:
    UNICODE_TYPE = str
else:
    UNICODE_TYPE = unicode


class ConfigurationManager(with_metaclass(Singleton)):
    def __init__(self, json_string, json_decoder=lambda x: x):
        self.configurations = dict()
        self.derived_configurations = dict()
        self.json_decoder = json_decoder  # see OtmlConfigurationManager.json_decoder
        json_dict = json.loads(json_string)
        self.load_configurations_from_json_dict(json_dict)

        self.validate_configurations()
        self.derive_configurations()

    def load_configurations_from_json_dict(self, json_dict):
        for key, value in json_dict.items():
            if type(value) is UNICODE_TYPE:
                self.configurations[key] = self.json_decoder(value)
            else:
                self.configurations[key] = value

    def update_configurations(self, other_json):
        other = json.loads(other_json)
        if set(self.configurations).issuperset(set(other)):
            self.load_configurations_from_json_dict(other)
        else:
            raise ConfigurationManagerError("configuration update is not a subset of current configurations")

        self.validate_configurations()
        self.derive_configurations()

    def validate_configurations(self):
        pass

    def derive_configurations(self):
        pass

    def __getitem__(self, key):
        if key in self.configurations:
            return self.configurations[key]
        elif key in self.derived_configurations:
            return self.derived_configurations[key]
        else:
            raise ConfigurationManagerError("{} not found".format(key))

    def __setitem__(self, key, value):
        if key in self.configurations:
            self.configurations[key] = value
        elif key in self.derived_configurations:
            raise ConfigurationManagerError("can not change {} directly - it is a derived configuration".format(key))
        else:
            raise ConfigurationManagerError("{} not found".format(key))

        self.validate_configurations()
        self.derive_configurations()
