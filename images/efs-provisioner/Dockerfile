FROM openshift/origin-release:golang-1.10 AS builder
COPY . /go/src/kubernetes-incubator/external-storage
RUN cd /go/src/kubernetes-incubator/external-storage/aws/efs && \
    go build -o efs-provisioner cmd/efs-provisioner/efs-provisioner.go

FROM openshift/origin-base
COPY --from=builder /go/src/kubernetes-incubator/external-storage/aws/efs/efs-provisioner /usr/bin

ENTRYPOINT ["/usr/bin/efs-provisioner"]
