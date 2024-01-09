Summary:        Linux kernel trace file system library
Name:           libtracefs
Version:        1.7.0
Release:        1%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://git.kernel.org/pub/scm/libs/libtrace/libtracefs.git/
Source:         https://git.kernel.org/pub/scm/libs/libtrace/libtracefs.git/snapshot/libtracefs-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(libtraceevent) >= 1.7.0

# LTO causes linking issues randomly like
# lto1: internal compiler error: resolution sub id 0x7136344381f3059f not in object file
# So disabling LTO at this moment.
%global _lto_cflags %nil

%description
libtracefs is a library for accessing the kernel trace file system

%package devel
Summary: Development headers of %{name}
Requires: %{name}%{_isa} = %{version}-%{release}
 
%description devel
Development headers of %{name}

%prep
%setup -q

%build
%set_build_flags
# skip parallel compilation
make -O -j1 V=1 VERBOSE=1 prefix=%{_prefix} libdir=%{_libdir} all
 
%install
%make_install prefix=%{_prefix} libdir=%{_libdir}
rm -rf %{buildroot}/%{_libdir}/libtracefs.a

%files
%license LICENSES/LGPL-2.1
%license LICENSES/GPL-2.0
%{_libdir}/%{name}.so.1
%{_libdir}/%{name}.so.%{version}

%files devel
%{_includedir}/tracefs/tracefs.h
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/%{name}.so

%changelog
