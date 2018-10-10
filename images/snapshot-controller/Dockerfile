#oit## This file is managed by the OpenShift Image Tool: https://github.com/openshift/enterprise-images
#oit## by the OpenShift Continuous Delivery team (#aos-cd-team on IRC).
#oit## 
#oit## Any yum repos listed in this file will effectively be ignored during CD builds.
#oit## Yum repos must be enabled in the oit configuration files.
#oit## Some aspects of this file may be managed programmatically. For example, the image name, labels (version,
#oit## release, and other), and the base FROM. Changes made directly in distgit may be lost during the next
#oit## reconciliation.
#oit## 
FROM rhel7:7-released



RUN yum-config-manager --enable rhel-7-server-ose-3.7-rpms
RUN yum install -y openshift-external-storage-snapshot-controller
RUN yum clean all
USER root

ENTRYPOINT ["/usr/bin/snapshot-controller"]

LABEL \
        io.k8s.description="Controller for VolumeSnapshots." \
        com.redhat.component="snapshot-controller-container" \
        vendor="Red Hat" \
        description="Controller for VolumeSnapshots." \
        License="GPLv2+" \
        url="https://github.com/kubernetes-incubator/external-storage/blob/master/snapshot/README.md" \
        io.k8s.display-name="Volume snapshot controller" \
        summary="Snapshot controller" \
        version="v3.7.65" \
        architecture="x86_64" \
        release="1" \
        io.openshift.tags="dynamic,controller" \
        name="openshift3/snapshot-controller"

