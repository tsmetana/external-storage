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



RUN yum install -y openshift-external-storage-snapshot-provisioner
RUN yum clean all
ENTRYPOINT ["/usr/bin/snapshot-provisioner"]

LABEL \
        io.k8s.description="Provisioner for VolumeSnapshots." \
        com.redhat.component="snapshot-provisioner-container" \
        vendor="Red Hat" \
        description="Provisioner for VolumeSnapshots." \
        License="GPLv2+" \
        url="https://github.com/kubernetes-incubator/external-storage/blob/master/snapshot/README.md" \
        io.k8s.display-name="Snapshot volume provisioner" \
        summary="Snapshot volume provisioner" \
        version="v3.9.45" \
        architecture="x86_64" \
        release="1" \
        io.openshift.tags="dynamic,provisioner" \
        name="openshift3/snapshot-provisioner"

