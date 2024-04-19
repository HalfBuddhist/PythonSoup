#!/usr/bin/env python
# coding=utf-8

import os
import sys
from email.mime.text import MIMEText

import gflags
import psycopg2

from base.logger_helper import PhoenixLogAdapter
from base.k8s_client import K8SClient
from models import Notebook
from models import Project, ExperimentCollection


class TestPG(object):
    def __init__(self):

        self._nb_db = psycopg2.connect(
            host=FLAGS.pg_host_tecoai,
            port=FLAGS.pg_port_tecoai,
            database="notebook",
            user=FLAGS.pg_user,
            password=FLAGS.pg_password,
        )
        self._nb_curosr = self._nb_db.cursor()
