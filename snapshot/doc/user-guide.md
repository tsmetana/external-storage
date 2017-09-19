Persistent Volume Snapshots in Kubernetes
=========================================

This document describes current state of persistent volume snapshot support in Kubernetes provided by external controller and provisioner. Familiarity with [Kubernetes API concepts](https://kubernetes.io/docs/concepts/) is suggested.

## Introduction

Many storage systems provide the ability to create "snapshots" of a persistent volumes to protect against data loss. The external snapshot controller and provisioner provide means to use the feature in Kubernetes cluster and handle the volume snapshots through Kubernetes API.

## Features

* Create snapshot of a `PersistentVolume` bound to a `PersistentVolumeClaim`
* List existing `VolumeSnapshots`
* Delete existing `VolumeSnapshot`
* Create a new `PersistentVolume` from an existing `VolumeSnapshot`
* Supported `PersistentVolume` [types](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#types-of-persistent-volumes):
    * Amazon EBS
    * GCE PD
    * HostPath

## Lifecycle of a Persistent Volume Snapshot

### Creating

User is able to make a snapshot of a `PersistentVolume` bound to a `PersistentVolumeClaim` by creating a new `VolumeSnapshot` object referencing the `PersistentVolumeClaim`. 

Example of the `VolumeSnapshot` object:
```yaml
apiVersion: volume-snapshot-data.external-storage.k8s.io/v1
  kind: VolumeSnapshot
  metadata:
    clusterName: ""
    creationTimestamp: 2017-09-19T13:58:28Z
    generation: 0
    labels:
      Timestamp: "1505829508178510973"
    name: snapshot-demo
    namespace: default
    resourceVersion: "780"
    selfLink: /apis/volume-snapshot-data.external-storage.k8s.io/v1/namespaces/default/volumesnapshots/snapshot-demo
    uid: 9cc5da57-9d42-11e7-9b25-90b11c132b3f
  spec:
    persistentVolumeClaimName: pvc-hostpath
    snapshotDataName: k8s-volume-snapshot-9cc8813e-9d42-11e7-8bed-90b11c132b3f
  status:
    conditions:
    - lastTransitionTime: null
      message: Snapshot created successfully
      reason: ""
      status: "True"
      type: Ready
    creationTimestamp: null
```

The object is then processed by the snapshot controller which instructs the storage system to create snapshot of the volume and creates a representation of the snapshot: `VolumeSnapshotData` API object. Depending on the storage type the operation might go through several phases which are reflected by the `VolumeSnapshot` and `VolumeSnapshotData` status:

1. The `VolumeSnapshot` object is created
2. The controller starts the snapshot operation: the snapshotted volume might need to be frozen and the applications paused.
3. The storage system finishes creating the snapshot (the snapshot is "cut") and the snapshotted volume might return to normal operation. The snapshot itself is not ready yet. The last status condition is of `Created` type with status value "True"
4. The newly created snapshot is completed and ready to use. The last status condition is of `Ready` type with status value "True"

