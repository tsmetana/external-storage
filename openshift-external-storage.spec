# Build project from bundled dependencies
%global with_bundled 1
# Build with debug info rpm
%global with_debug 1

%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%if ! 0%{?gobuild:1}
%define gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};
%endif

%global provider        github
%global provider_tld    com
%global project         kubernetes-incubator
%global repo            external-storage
# https://github.com/kubernetes-incubator/external-storage
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          1ffdb9d63c8415e752716f67d5bd3ac0f823298f
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           openshift-external-storage
Version:        0.0.3
Release:        2.git%{shortcommit}%{?dist}
Summary:        External storage plugins, provisioners, and helper libraries for OpenShift
License:        ASL 2.0
URL:            https://%{provider_prefix}
Source0:        https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

# tsmetana, hchen: bug 1566194
Patch0: external-storage-ceph-namespaces.patch

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 aarch64 %{arm} ppc64le s390x}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%description
%{summary}

%package efs-provisioner
Summary: AWS EFS dynamic PV provisioner

%description efs-provisioner
AWS EFS dynamic PV provisioner.

%package local-provisioner
Summary: Provisioner for local PersistentVolumes
Requires: e2fsprogs

%description local-provisioner
Provisioner for local PersistentVolumes.

%package snapshot-controller
Summary: External controller for volume snapshots

%description snapshot-controller
External controller for volume snapshots.

%package snapshot-provisioner
Summary: Provisioner for restoring snapshots to PersistentVolumes

%description snapshot-provisioner
Provisioner for restoring snapshots to PersistentVolumes

%package cephfs-provisioner
Summary: Provisioner for CephFS volumes
Requires: ceph-common python-cephfs

%description cephfs-provisioner
Provisioner for CephFS volumes.

%prep
%setup -q -n %{repo}-%{commit}
%patch0 -p1

%build
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s ../../../ src/%{import_path}
export GOPATH=$(pwd):$(pwd)/repo-infra/vendor:%{gopath}

%gobuild -o bin/aws/efs/cmd/efs-provisioner %{import_path}/aws/efs/cmd/efs-provisioner
%gobuild -o bin/local-volume/provisioner/local-provisioner %{import_path}/local-volume/provisioner/cmd
%gobuild -o bin/local-volume/provisioner/snapshot-controller %{import_path}/snapshot/cmd/snapshot-controller
%gobuild -o bin/local-volume/provisioner/snapshot-provisioner %{import_path}/snapshot/cmd/snapshot-pv-provisioner
%gobuild -o bin/cephfs/provisioner/cephfs-provisioner %{import_path}/ceph/cephfs
cp src/%{import_path}/ceph/cephfs/cephfs_provisioner/cephfs_provisioner.py bin/cephfs/provisioner/

%install
install -d -p %{buildroot}%{_bindir}
install -d -p %{buildroot}%{_prefix}/local/bin
install -p -m 0755 bin/aws/efs/cmd/efs-provisioner %{buildroot}%{_bindir}
install -p -m 0755 bin/local-volume/provisioner/local-provisioner %{buildroot}%{_bindir}
install -p -m 0755 bin/local-volume/provisioner/snapshot-controller %{buildroot}%{_bindir}
install -p -m 0755 bin/local-volume/provisioner/snapshot-provisioner %{buildroot}%{_bindir}
install -p -m 0755 bin/cephfs/provisioner/cephfs-provisioner %{buildroot}%{_bindir}
# FIXME: The path to the helper script is hard-coded in the binary
install -p -m 0755 bin/cephfs/provisioner/cephfs_provisioner.py %{buildroot}%{_prefix}/local/bin/
mkdir -p %{buildroot}%{_libexecdir}/%{name}-local-provisioner/scripts
install -p -m 0755 \
	src/%{import_path}/local-volume/provisioner/deployment/docker/scripts/* \
	%{buildroot}%{_libexecdir}/%{name}-local-provisioner/scripts

%files efs-provisioner
%{_bindir}/efs-provisioner
%license LICENSE
%doc CONTRIBUTING.md RELEASE.md README.md

%files local-provisioner
%{_bindir}/local-provisioner
%{_libexecdir}/%{name}-local-provisioner
%license LICENSE
%doc CONTRIBUTING.md RELEASE.md README.md

%files snapshot-controller
%{_bindir}/snapshot-controller
%license LICENSE
%doc CONTRIBUTING.md RELEASE.md README.md

%files snapshot-provisioner
%{_bindir}/snapshot-provisioner
%license LICENSE
%doc CONTRIBUTING.md RELEASE.md README.md

%files cephfs-provisioner
%{_bindir}/cephfs-provisioner
%{_prefix}/local/bin/cephfs_provisioner.py
%license LICENSE
%doc CONTRIBUTING.md RELEASE.md README.md


%changelog
* Fri Oct 12 2018 Tomas Smetana <tsmetana@redhat.com> - 0.0.3-2
* Update for the new CI

* Tue Jul 31 2018 Matthew Wong <mawong@redhat.com> - 0.0.3-1.git1ffdb9d
- Rebase to latest upstream version

* Tue May 29 2018 Tomas Smetana <tsmetana@redhat.com> - 0.0.2-3.gitd3c94f0
- Install local-provisioners helper scripts

* Fri Apr 13 2018 Tomas Smetana <tsmetana@redhat.com> - 0.0.2-2.gitd3c94f0
- Workaround to allow ceph_volume_client to create 'volumes' without namespace isolation
- Resolves: rhbz#1566194

* Tue Apr 03 2018 Tomas Smetana <tsmetana@redhat.com> - 0.0.2-1.gitd3c94f0
- Rebase to latest upstream version; drop upstreamed patches
- Add CephFS and Manila provisioner
- Resolves: rhbz#1547884, rhbz#1548996, rhbz#1490722

* Thu Feb 22 2018 jsafrane <jsafrane@redhat.com> - 0.0.1-9.git78d6339
- Fix local provisioner to discover only mount points and not empty directories
- Resolves: rhbz#1490722

* Fri Feb 16 2018 jsafrane <jsafrane@redhat.com> - 0.0.1-8.git78d6339
- Rebuilt for 3.9

* Mon Feb 12 2018 jsafrane <jsafrane@redhat.com> - 0.0.1-7.git78d6339
- Fix error message when a plain file is discovered
- Resolves: rhbz#1542867

* Thu Nov 16 2017 Yaakov Selkowitz <yselkowi@redhat.com> - 0.0.1-6.git78d6339
- Rebuilt for multi-arch enablement

* Mon Nov 13 2017 Tomas Smetana <tsmetana@redhat.com> - 0.0.1-5.git78d6339
- Rename the snapshot provisioner binary according to upstream one

* Thu Nov 09 2017 Tomas Smetana <tsmetana@redhat.com> - 0.0.1-4.git78d6339
- Rename snapshot API to be consistent with the new upstream APIs

* Thu Oct 19 2017 Tomas Smetana <tsmetana@redhat.com> - 0.0.1-3.git78d6339
- Backport GCE PD code for snapshots
- Resolves: rhbz#1503015, rhbz#1502945

* Tue Sep 26 2017 jsafrane <jsafrane@redhat.com> - 0.0.1-2.git78d6339
- Rename local-storage-provisioner to local-provisioner

* Wed Sep 20 2017 jsafrane <jsafrane@redhat.com> - 0.0.1-1.git78d6339
- First release

