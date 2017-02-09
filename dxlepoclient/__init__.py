# -*- coding: utf-8 -*-
################################################################################
# Copyright (c) 2017 McAfee Inc. - All Rights Reserved.
################################################################################
from __future__ import absolute_import

from .client import EpoClient, OutputFormat

__version__ = "0.0.1"


def get_version():
    """
    Returns the version of the McAfee ePolicy Orchestrator (ePO) Client Library

    :return: The version of the McAfee ePolicy Orchestrator (ePO) Client Library
    """
    return __version__
