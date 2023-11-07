%global debug_package %{nil}
%global gem_name msgpack
Summary:        MessagePack implementation for Ruby
Name:           rubygem-%{gem_name}
Version:        1.7.2
Release:        1%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            http://msgpack.org/
Source0:        https://github.com/msgpack/msgpack-ruby/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-ruby-%{version}.tar.gz
Patch0:         fix-file_list.patch
BuildRequires:  git
BuildRequires:  ruby
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
MessagePack implementation for Ruby

%prep
%autosetup -p1 -n %{gem_name}-ruby-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE
%{gemdir}

%changelog
* Tue Nov 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.7.2-1
- Auto-upgrade to 1.7.2 - Azure Linux 3.0 - package upgrades

* Fri Apr 01 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.4.5-1
- Update to v1.4.5.
- Build from .tar.gz source.

* Mon Jan 04 2021 Henry Li <lihl@microsoft.com> - 1.3.3-1
- License verified
- Original version for CBL-Mariner
