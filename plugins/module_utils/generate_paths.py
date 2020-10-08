# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


"""
flatten a complex object to dot bracket notation
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re
from ansible.module_utils.common._collections_compat import (
    Mapping,
    MutableMapping,
)


def generate_paths(nested_json, prepend):
    out = {}

    def flatten(data, name=""):
        if isinstance(data, (dict, Mapping, MutableMapping)):
            for key, val in data.items():
                if name:
                    if re.match("^[a-zA-Z_][a-zA-Z0-9_]*$", key):
                        nname = name + ".{key}".format(key=key)
                    else:
                        nname = name + "['{key}']".format(key=key)
                else:
                    nname = key
                flatten(val, nname)
        elif isinstance(data, list):
            for idx, val in enumerate(data):
                flatten(val, "{name}[{idx}]".format(name=name, idx=idx))
        else:
            out[name] = data

    if prepend:
        flatten({prepend: nested_json})
    else:
        flatten(nested_json)
    return out
