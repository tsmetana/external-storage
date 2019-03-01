FROM openshift/origin-release:golang-1.10 AS builder
COPY . /go/src/kubernetes-incubator/external-storage
RUN cd /go/src/kubernetes-incubator/external-storage/ceph/cephfs && \
    go build -o cephfs-provisioner cephfs-provisioner.go

FROM openshift/origin-base
COPY --from=builder /go/src/kubernetes-incubator/external-storage/ceph/cephfs/cephfs-provisioner /usr/bin

ENTRYPOINT ["/usr/bin/cephfs-provisioner"]
