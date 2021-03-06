#!/usr/bin/env python
# coding: utf-8

"""
Defines common socketcan functions.
"""

import os
import errno
import struct

from can.interfaces.socketcan.socketcan_constants import CAN_EFF_FLAG


def pack_filters(can_filters=None):
    if can_filters is None:
        # Pass all messages
        can_filters = [{
            'can_id': 0,
            'can_mask': 0
        }]

    can_filter_fmt = "={}I".format(2 * len(can_filters))
    filter_data = []
    for can_filter in can_filters:
        can_id = can_filter['can_id']
        can_mask = can_filter['can_mask']
        if 'extended' in can_filter:
            # Match on either 11-bit OR 29-bit messages instead of both
            can_mask |= CAN_EFF_FLAG
            if can_filter['extended']:
                can_id |= CAN_EFF_FLAG
        filter_data.append(can_id)
        filter_data.append(can_mask)

    return struct.pack(can_filter_fmt, *filter_data)


def error_code_to_str(code):
    """
    Converts a given error code (errno) to a useful and human readable string.

    :param int error_code: a possibly invalid/unknown error code
    :rtype: str
    :returns: a string explaining and containing the given error code, or a string
              explaining that the errorcode is unknown if that is the case
    """

    try:
        name = errno.errorcode[code]
    except KeyError:
        name = "UNKNOWN"

    try:
        description = os.strerror(code)
    except ValueError:
        description = "no description available"

    return "{} (errno {}): {}".format(name, code, description)
