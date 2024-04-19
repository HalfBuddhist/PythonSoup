from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from kubernetes import client
from kubernetes import config


class K8SException(Exception):
    pass


class K8SClient(object):

    def __init__(self, in_cluster, config_path):
        if in_cluster:
            config.load_incluster_config()
        else:
            if not config_path or not os.path.exists(config_path):
                err_msg = ("init cluster outer client, "
                           "but config path |%s| does not exist" % config_path)
                raise K8SException(err_msg)
            config.load_kube_config(config_path)

        self.__client = client
        self.clients = dict()

    @property
    def client_v1_api(self):
        if "v1" in self.clients:
            return self.clients["v1"]
        self.clients["v1"] = self.__client.AppsV1Api()
        return self.clients["v1"]

    @property
    def client_core_v1_api(self):
        if "corev1" in self.clients:
            return self.clients["corev1"]
        self.clients["corev1"] = self.__client.CoreV1Api()
        return self.clients["corev1"]

    @property
    def client_ext_v1_beta_api(self):
        if "extb1beta" in self.clients:
            return self.clients["extb1beta"]
        self.clients["extb1beta"] = self.__client.ExtensionsV1beta1Api()
        return self.clients["extb1beta"]

    @property
    def client_crd_api(self):
        if "crd" in self.clients:
            return self.clients["crd"]
        self.clients["crd"] = self.__client.CustomObjectsApi(
            self.__client.ApiClient())
        return self.clients["crd"]
