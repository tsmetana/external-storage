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



RUN yum-config-manager --enable rhel-7-server-ose-3.10-rpms
RUN yum install -y openshift-external-storage-local-provisioner
RUN yum clean all
# Move the helper scripts to the default location so the users don't have to
# configure the provisioner on every run.
RUN mv /usr/libexec/openshift-external-storage-local-provisioner/scripts /

USER root

ENTRYPOINT ["/usr/bin/local-provisioner"]

LABEL \
        io.k8s.description="Provisioner for local PersistentVolumes." \
        com.redhat.component="openshift-local-storage-container" \
        vendor="Red Hat" \
        description="Provisioner for local PersistentVolumes." \
        License="GPLv2+" \
        url="https://github.com/kubernetes-incubator/external-storage/blob/master/local-volume/README.md" \
        io.k8s.display-name="Local storage provisioner" \
        summary="Local storage provisioner" \
        version="v3.10.0" \
        architecture="x86_64" \
        release="0.55.0.0" \
        io.openshift.tags="local,dynamic,provisioner" \
        name="openshift3/local-storage-provisioner"

