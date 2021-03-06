# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 11:40:20 2016

@author: Zahari Kassabov
"""

#TODO: Make adding checks easier

from reportengine.resourcebuilder import ResourceError

def add_check(f, check):
    if not hasattr(f, 'checks'):
        f.checks = [check]
    else:
        f.checks.append(check)


def require_one(*args):
    """Ensure that at least one argument is not None."""
    def check(callspec, ns, graph):
        s = set(args)
        in_input_specs = {node.value.resultname for node in graph[callspec].inputs}
        in_ns = {k for k in s if ns.get(k, None) is not None}


        if not (s & (in_ns | in_input_specs)):
            raise ResourceError("You need to supply at least one of: %s" % (args,))

    def decorator(f):
        add_check(f, check)
        return f

    return decorator