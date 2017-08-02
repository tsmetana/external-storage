# HostPath implementation of snapshots

HostPath snapshots are not suitable for production, they're dedicated only
for development and testing. Volume snapshots are stored in /tmp/ in the
container (or host) that runs `snapshot-controller`!.

#### Start Snapshot Controller

(assuming running Kubernetes local cluster):

```
_output/bin/snapshot-controller  -kubeconfig=${HOME}/.kube/config
```

####  Create a snapshot
 * Create a hostpath PV (leading to `/tmp/test` on the host) and a PVC:
```bash
kubectl create -f examples/hostpath/pv.yaml
kubectl create -f examples/hostpath/pvc.yaml
```

Optionally, you can simulate a pod activity and store something into the PV:
```bash
mkdir -p /tmp/test
echo "hello world" > /tmp/test/data.txt
```

 * Create a Snapshot Third Party Resource

```bash
kubectl create -f examples/hostpath/snapshot.yaml
```

#### Check VolumeSnapshot and VolumeSnapshotData are created

```bash
kubectl get volumesnapshot,volumesnapshotdata -o yaml
```

## Snapshot based PV Provisioner

Unlike existing PV provisioners that provision blank volume, Snapshot based PV provisioners create volumes based on existing snapshots. Thus new provisioners are needed.

There is a special PVCs annotation that requests a PV based on a snapshot. As illustrated in [the example](examples/hostpath/claim.yaml), `snapshot.alpha.kubernetes.io` must point to an existing VolumeSnapshot Object:
```yaml
metadata:
  name:
  namespace:
  annotations:
    snapshot.alpha.kubernetes.io/snapshot: snapshot-demo
```

### HostPath provisioner for snapshot-based claims

#### Start PV Provisioner and Storage Class to restore a snapshot to a PV

Start provisioner (assuming running Kubernetes local cluster):
```bash
_output/bin/snapshot-provisioner  -kubeconfig=${HOME}/.kube/config
```

Create a storage class:
```bash
kubectl create -f examples/hostpath/class.yaml
```

### Create a PVC that claims a PV based on an existing snapshot

```bash
kubectl create -f examples/hostpath/claim.yaml
```

HostPath snapshot provisioner will unpack the snapshot into `/tmp/restore/<random UID>/`.

#### Check PV and PVC are created

```bash
kubectl get pv,pvc
```
