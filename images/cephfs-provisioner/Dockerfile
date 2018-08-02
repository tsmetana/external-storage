FROM rhel7:7-released

RUN yum install -y ceph-common python-cephfs
RUN yum install -y openshift-external-storage-cephfs-provisioner
RUN yum clean all

USER root

ENTRYPOINT ["/usr/bin/cephfs-provisioner"]

LABEL \
        io.k8s.description="CephFS dynamic PV provisioner." \
        com.redhat.component="cephfs-provisioner-container" \
        description="CephFS dynamic PV provisioner" \
        License="GPLv2+" \
        io.k8s.display-name="CephFS Provisioner" \
        summary="CephFS dynamic PV provisioner" \
        version="v3.10.0" \
        io.openshift.tags="ceph,cephfs,dynamic,provisioner" \
        name="openshift3/origin-cephfs-provisioner" \
        io.openshift.expose-services="" \
        maintainer="mawong@redhat.com"
