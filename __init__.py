# -*- coding: utf-8 -*-

def classFactory(iface):
    from .Base import Base
    return Base(iface)
