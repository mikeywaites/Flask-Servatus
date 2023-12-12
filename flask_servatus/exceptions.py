#!/usr/bin/python
# -*- coding: utf-8 -*-


class ServatusError(Exception):
    pass


class SuspiciousFileOperation(ServatusError):
    pass


class ConfigurationError(ServatusError):
    pass
