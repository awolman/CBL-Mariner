Summary:        A user interface to Ftrace
Name:           trace-cmd
Version:        3.2
Release:        1%{?dist}
License:        LGPLv2+ AND GPLv2+
URL:            https://git.kernel.org/pub/scm/utils/trace-cmd/trace-cmd.git
Source0:        https://git.kernel.org/pub/scm/utils/trace-cmd/trace-cmd.git/snapshot/trace-cmd-v%{version}.tar.gz
Source1:        trace-cmd.conf
Source2:        trace-cmd.service
Source3:        98-trace-cmd.rules

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  xmlto
BuildRequires:  asciidoc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  libtraceevent-devel >= 1.6.3
BuildRequires:  libtracefs-devel >= 1.5.0
BuildRequires:  audit-libs-devel
BuildRequires:  chrpath
BuildRequires:  swig
BuildRequires:  systemd-rpm-macros
BuildRequires:  libzstd-devel
BuildRequires:  pkg-config

%description
trace-cmd is a user interface to Ftrace. Instead of needing to use
debugfs directly, trace-cmd will handle the setting of options and
tracers and will record into a data file.

%package python3
Summary: Python plugin support for trace-cmd
Requires: trace-cmd%{_isa} = %{version}-%{release}
BuildRequires: python3-devel

%description  python3
Python plugin support for trace-cmd

%prep
%autosetup -n %{name}-v%{version}
cp %{SOURCE1} .
cp %{SOURCE2} .
cp %{SOURCE3} .

%build
# MANPAGE_DOCBOOK_XSL define is hack to avoid using locate
MANPAGE_DOCBOOK_XSL=`rpm -ql docbook-style-xsl | grep manpages/docbook.xsl`
CFLAGS="%{optflags} -D_GNU_SOURCE" LDFLAGS="%{build_ldflags}" BUILD_TYPE=Release \
  make V=9999999999 MANPAGE_DOCBOOK_XSL=$MANPAGE_DOCBOOK_XSL \
  prefix=%{_prefix} libdir=%{_libdir} \
  PYTHON_VERS=python3 libs doc all_cmd
for i in python/*.py ; do 
    sed -i 's/env python2/python3/g' $i
done
chrpath --delete tracecmd/trace-cmd

%install
make libdir=%{_libdir} prefix=%{_prefix} V=1 PYTHON_VERS=python3 DESTDIR=%{buildroot}/ CFLAGS="%{optflags} -D_GNU_SOURCE" LDFLAGS="%{build_ldflags} -z muldefs " BUILD_TYPE=Release install_libs install_doc install install_python
find %{buildroot}%{_mandir} -type f | xargs chmod u-x,g-x,o-x
find %{buildroot}%{_datadir} -type f | xargs chmod u-x,g-x,o-x
mkdir -p -m755 %{buildroot}/%{_sysconfdir}/sysconfig/
mkdir -p -m755 %{buildroot}/%{_unitdir}/
mkdir -p -m755 %{buildroot}/%{_udevrulesdir}/
install -p -m 644 trace-cmd.conf %{buildroot}/%{_sysconfdir}/sysconfig/
install -p -m 644 trace-cmd.service %{buildroot}/%{_unitdir}/
install -p -m 644 98-trace-cmd.rules %{buildroot}/%{_udevrulesdir}/
chrpath --delete %{buildroot}/%{_libdir}/libtracecmd.so*

%preun
%systemd_preun %{name}.service

%files
%doc COPYING COPYING.LIB README
%{_bindir}/trace-cmd
%{_libdir}/libtracecmd.so
%{_libdir}/libtracecmd.so.1
%{_libdir}/libtracecmd.so.1.4.0
%{_libdir}/pkgconfig/libtracecmd.pc
%{_includedir}/trace-cmd
%{_mandir}/man1/%{name}*
%{_mandir}/man3/tracecmd*
%{_mandir}/man3/libtracecmd*
%{_mandir}/man5/%{name}*
%{_docdir}/trace-cmd/trace-cmd*.html
%{_docdir}/libtracecmd-doc
%{_sysconfdir}/bash_completion.d/trace-cmd.bash
%{_sysconfdir}/sysconfig/trace-cmd.conf
%{_unitdir}/trace-cmd.service
%{_udevrulesdir}/98-trace-cmd.rules

%files python3
%doc Documentation/README.PythonPlugin
%{_libdir}/%{name}/python/
 
%changelog
