	
Summary:        Produces a document with syntax highlighting
Name:           source-highlight
Version:        3.1.9
Release:        1%{?dist}
License:        GPLv3+
Source0:        ftp://ftp.gnu.org/gnu/src-highlite/%{name}-%{version}.tar.gz
Patch0:         remove-throw.patch
URL:            http://www.gnu.org/software/src-highlite/
BuildRequires:  make
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  boost-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  help2man
BuildRequires:  bash-completion

%description
This program, given a source file, produces a document with syntax
highlighting. At the moment this package can handle:
Java, Javascript, C/C++, Prolog, Perl, Php3, Python, Flex, ChangeLog, Ruby,
Lua, Caml, Sml and Log as source languages, and HTML, XHTML and ANSI color
escape sequences as output format.

%package devel
Summary: Development files for source-highlight
Requires: %{name}%{?_isa} = %{version}-%{release}
# For linking against source-higlight using pkgconfig
Requires: boost-devel

%description devel
Development files for source-highlight

%prep
%autosetup -p1

%build
export CXXFLAGS="%{optflags}"
%configure --disable-static \
           --with-boost-regex=boost_regex
%make_build

%install
%make_install

ls -lR %{buildroot}%{_datadir}
mv %{buildroot}%{_datadir}/doc/ docs
%{__sed} -i 's/\r//' docs/source-highlight/*.css
ls -lR %{buildroot}%{_infodir}
rm -f %{buildroot}%{_infodir}/dir
rm -f %{buildroot}%{_libdir}/libsource-highlight.la
#find %{buildroot} -type f -name "*.a" -exec rm -f {} ';'

mkdir -p %{buildroot}%{_datadir}/bash-completion/completions/
mv %{buildroot}%{_sysconfdir}/bash_completion.d/source-highlight %{buildroot}%{_datadir}/bash-completion/completions/
rmdir %{buildroot}%{_sysconfdir}/bash_completion.d/

%files
%doc docs/source-highlight/*
%{_bindir}/cpp2html
%{_bindir}/java2html
%{_bindir}/source-highlight
%{_bindir}/source-highlight-esc.sh
%{_bindir}/check-regexp
%{_bindir}/source-highlight-settings
%{_bindir}/src-hilite-lesspipe.sh
%{_datadir}/bash-completion/
%{_libdir}/libsource-highlight.so.*
%dir %{_datadir}/source-highlight
%{_datadir}/source-highlight/*
%{_mandir}/man1/*
%{_infodir}/source-highlight*.info*

%files devel
%dir %{_includedir}/srchilite
%{_libdir}/libsource-highlight.so
%{_libdir}/pkgconfig/source-highlight.pc
%{_includedir}/srchilite/*.h
