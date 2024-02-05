Summary:        Terminal multiplexer
Name:           tmux
Version:        3.2a
Release:        4%{?dist}
License:        ISC and BSD
URL:            https://tmux.github.io/
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://github.com/tmux/tmux/releases/download/%{version}/%{name}-%{version}.tar.gz
Patch0:         CVE-2022-47016.patch
Patch1:         manual-patch-to-fix-crash-due-to-change-to-ncurses.patch
Requires:       libevent
Requires:       ncurses >= 6.4-2
BuildRequires:  libevent-devel
BuildRequires:  ncurses-devel >= 6.4-2

%description
Terminal multiplexer

%prep
%autosetup -p1

%build
./configure \
    --prefix=%{_prefix}
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%check
make  %{?_smp_mflags} check

%files
%defattr(-,root,root)
%license COPYING
/usr/bin/*
%exclude /usr/lib
/usr/share/*
%exclude /usr/src

%changelog
* Thu Nov 16 2023 Tobias Brick <tobiasb@microsoft.com> - 3.2a-4
- Add dependency on ncurses >= 6.4-2
- Patch to fix crash due to kprevious change to ncurses

* Fri Feb 10 2023 Rachel Menge <rachelmenge@microsoft.com> - 3.2a-3
- Patch CVE-2022-47016

* Tue Feb 08 2022 Thomas Crain <thcrain@microsoft.com> - 3.2a-2
- Remove unused `%%define sha1` lines

* Mon Jan 10 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 3.2a-1
- Update to version 3.2a.
- License verified.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.7-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.7-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Sep 10 2018 Michelle Wang <michellew@vmware.com> 2.7-1
- Updated to version 2.7.

* Tue May 02 2017 Xiaolin Li <xiaolinl@vmware.com> 2.4-1
- Updated to version 2.4. Added make check.

* Tue Mar 28 2017 Xiaolin Li <xiaolinl@vmware.com> 2.3-1
- Updated to version 2.3.

* Wed Jul 13 2016 Alexey Makhalov <amakhalov@vmware.com> 2.2-1
- Initial build.  First version
