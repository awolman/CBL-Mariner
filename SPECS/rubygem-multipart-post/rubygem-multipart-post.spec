%global debug_package %{nil}
%global gem_name multipart-post
Summary:        Adds multipart POST capability to net/http
Name:           rubygem-%{gem_name}
Version:        2.3.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages
URL:            https://github.com/socketry/multipart-post
Source0:        https://github.com/socketry/multipart-post/archive/refs/tags/v%{version}.tar.gz#/%{gem_name}-%{version}.tar.gz
Patch0:         fix-file_list.patch
BuildRequires:  git
BuildRequires:  ruby
Provides:       rubygem(%{gem_name}) = %{version}-%{release}

%description
Adds a streamy multipart form post capability to Net::HTTP.
Also supports other methods besides POST.

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build
gem build %{gem_name}

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{gem_name}-%{version}.gem

%files
%defattr(-,root,root,-)
%license %{gemdir}/gems/%{gem_name}-%{version}/LICENSE
%{gemdir}

%changelog
* Thu Oct 19 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.3.0-1
- Auto-upgrade to 2.3.0 - Azure Linux 3.0 - package upgrades

* Wed Jun 22 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 2.1.1-2
- Build from .tar.gz source.

* Wed Jan 06 2021 Henry Li <lihl@microsoft.com> - 2.1.1-1
- License verified
- Original version for CBL-Mariner
