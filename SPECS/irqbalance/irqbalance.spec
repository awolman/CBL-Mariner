Summary:        Irqbalance daemon
Name:           irqbalance
Version:        1.9.2
Release:        1%{?dist}
License:        GPLv2
URL:            https://github.com/Irqbalance/irqbalance
Group:          System Environment/Services
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://github.com/Irqbalance/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         fix-format-security.patch
BuildRequires:  systemd-devel
BuildRequires:  glib-devel
Requires:       systemd
Requires:       glib

%description
Irqbalance is a daemon to help balance the cpu load generated by
interrupts across all of a systems cpus.

%prep
%autosetup -p1

%build
sed -i 's/libsystemd-journal/libsystemd/' configure.ac
./autogen.sh
./configure \
    --prefix=%{_prefix} \
    --disable-static \
    --with-systemd

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
install -D -m 0644 misc/irqbalance.env %{buildroot}/etc/sysconfig/irqbalance
sed -i 's#/path/to/irqbalance.env#/etc/sysconfig/irqbalance#' misc/irqbalance.service
install -D -m 0644 misc/irqbalance.service %{buildroot}%{_prefix}/lib/systemd/system/irqbalance.service

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post
%systemd_post %{name}.service
%preun
%systemd_preun %{name}.service
%postun
%systemd_postun_with_restart %{name}.service

%files
%defattr(-,root,root)
%license COPYING
%config(noreplace) %{_sysconfdir}/*
%{_sbindir}/*
%exclude %{_libdir}/debug/*
%{_libdir}/systemd/*
%{_datadir}/*

%changelog
* Fri Oct 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.9.2-1
- Auto-upgrade to 1.9.2 - Azure Linux 3.0 - package upgrades

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.8.0-3
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Fri Jun 17 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.8.0-2
- Add upstream patch to fix -Werror=format-security errors after ncurses 6.3 upgrade

* Tue Feb 22 2022 Cameron Baird <cameronbaird@microsoft.com> - 1.8.0-1
- Update source to v1.8.0

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.6.0-3
- Added %%license line automatically

* Thu Apr 09 2020 Joe Schmitt <joschmit@microsoft.com> 1.6.0-2
- Fix Source0 comment.

* Mon Mar 30 2020 Jon Slobodzian <joslobo@microsoft.com> 1.6.0-1
- Updated to latest version to support NUMA. Verified license file.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.4.0-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 1.4.0-2
- Adding BuildArch

* Fri Sep 07 2018 Ankit Jain <ankitja@vmware.com>  1.4.0-1
- Updated the package to version 1.4.0

* Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com>  1.2.0-1
- Updated the package to version 1.2.0

* Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  1.1.0-4
- Change systemd dependency

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.1.0-3
- GA - Bump release of all rpms

* Thu May 05 2016 Kumar Kaushik <kaushikk@vmware.com> 1.1.0-2
- Adding package upgrade support.

* Fri Jan 15 2016 Alexey Makhalov <amakhalov@vmware.com> 1.1.0-1
- Initial version
