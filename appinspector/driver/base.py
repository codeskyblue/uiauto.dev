#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Created on Fri Mar 01 2024 14:18:30 by codeskyblue
"""
import abc

from PIL import Image

from appinspector.model import Hierarchy, ShellResponse


class BaseDriver(abc.ABC):
    def __init__(self, serial: str):
        self.serial = serial

    @abc.abstractmethod
    def screenshot(self, id: int) -> Image.Image:
        """Take a screenshot of the device
        :param id: physical display ID to capture (normally: 0)
        :return: PIL.Image.Image
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def dump_hierarchy(self) -> Hierarchy:
        """Dump the view hierarchy of the device
        :return: Hierarchy
        """
        raise NotImplementedError()
    
    def shell(self, command: str) -> ShellResponse:
        """Run a shell command on the device
        :param command: shell command
        :return: ShellResponse
        """
        raise NotImplementedError()
    
    