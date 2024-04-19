#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import pickle
import smtplib
import sys
import time
import traceback
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from email.mime.text import MIMEText

import jinja2


def render_without_request(template_name, **context):
    """ Render template without a http request.

    用法同 flask.render_template:
    render_without_request('template.html', var1='foo', var2='bar')
    """
    env = jinja2.Environment(loader=jinja2.PackageLoader('script'))
    template = env.get_template(template_name)
    return template.render(**context)


def get_time_zone_info():
    """Get time zone info
    :return: time_zone tupple
             ('+08:00', '+0800', timezone)
    """
    time_zone_offset_str = time.strftime('%z', time.localtime())
    time_zone_colon_fmt = (
        time_zone_offset_str[:-2] + ":" + time_zone_offset_str[-2:])
    minutes = int(time_zone_offset_str[-2:]) * (
        1 if time_zone_offset_str[0] == '+' else -1)
    hours = int(time_zone_offset_str[1:-2]) * (
        1 if time_zone_offset_str[0] == '+' else -1)
    time_zone = timezone(timedelta(hours=hours, minutes=minutes))
    return time_zone_colon_fmt, time_zone_offset_str, time_zone