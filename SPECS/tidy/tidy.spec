%global __cmake_in_source_build 1
%global libname libtidy
%global upname tidy-html5
%global tidy_compat_headers 1
Summary:        Utility to clean up and pretty print HTML/XHTML/XML
Name:           tidy
Version:        5.9.9
Release:        1%{?dist}
License:        W3C
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.html-tidy.org/
Source0:        https://github.com/htacg/%{upname}/archive/%{version}.tar.gz#/%{upname}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libxslt
## upstream patches
BuildRequires:  make
BuildRequires:  pkg-config
Requires:       %{libname}%{?_isa} = %{version}-%{release}
Provides:       tidy-html5 = %{version}-%{release}

%description
When editing HTML it's easy to make mistakes. Wouldn't it be nice if
there was a simple way to fix these mistakes automatically and tidy up
sloppy editing into nicely laid out markup? Well now there is! Dave
Raggett's HTML TIDY is a free utility for doing just that. It also
works great on the atrociously hard to read markup generated by
specialized HTML editors and conversion tools, and can help you
identify where you need to pay further attention on making your pages
more accessible to people with disabilities.

%package -n %{libname}
Summary:        Runtime library for %{name}

%description -n %{libname}
%{summary}.

%package -n %{libname}-devel
Summary:        Development files for %{name}
Requires:       %{libname}%{?_isa} = %{version}-%{release}
Obsoletes:      tidy-devel < 0.99.0-10
Provides:       tidy-devel = %{version}-%{release}

%description -n %{libname}-devel
%{summary}.

%prep
%autosetup -n %{upname}-%{version} -p1

# docs/test assuming binary named tidy5, let's fake it -- rex
# FIXME: to do properly, s|tidy5|tidy| references everwhere
ln -s tidy build/cmake/tidy5

%build
pushd build/cmake
%cmake ../../ \
  -DCMAKE_BUILD_TYPE:STRING=Release \
  -DTIDY_CONSOLE_SHARED:BOOL=ON \
  %{?tidy_compat_headers:-DTIDY_COMPAT_HEADERS:BOOL=ON}
popd

%make_build -C build/cmake


%install
make install/fast DESTDIR=%{buildroot}  -C build/cmake

## unpackaged files
# omit static lib
rm -fv %{buildroot}%{_libdir}/libtidy.a


%files
%{_bindir}/tidy
%{_mandir}/man1/tidy.1*

%ldconfig_scriptlets -n %{libname}

%files -n %{libname}
%license README/LICENSE.md
%{_libdir}/libtidy.so.5*

%files -n %{libname}-devel
%{_includedir}/tidy*.h
%if 0%{?tidy_compat_headers}
%{_includedir}/buffio.h
%{_includedir}/platform.h
%endif
%{_libdir}/libtidy.so
%{_libdir}/pkgconfig/tidy.pc

%changelog
* Fri Oct 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.9.9-1
- Auto-upgrade to 5.9.9 - Azure Linux 3.0 - package upgrades

* Mon May 01 2023 Sean Dougherty <sdougherty@microsoft.com> - 5.8.0-6
- Backported patch to fix CVE-2021-33391

* Tue Oct 18 2022 Osama Esmail <osamaesmail@microsoft.com> - 5.8.0-5
- Upgraded from 5.7.28 to 5.8.0
- Changed libtidys.a to libtidy.a
- Added make to our upgrade since tidy uses it now.
- Reverted source URL change
- Initial CBL-Mariner import from Fedora 37 (license: MIT)

* Fri Sep 16 2022 Osama Esmail <osamaesmail@microsoft.com> - 5.7.28-5
- Moved from SPECS-EXTENDED to SPECS
- License verified
- Updated source URL

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 12 2021 Gwyn Ciesla <gwync@protonmail.com> - 5.8.0-1
- 5.8.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.28-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.28-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 16 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.7.28-1
- 5.7.28 (#1728023)
- enable -DTIDY_COMPAT_HEADERS
- link console app against shared lib

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-2
- CVE-2017-17497 (#1485859)

* Mon Dec 11 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-1
- 5.6.0, pkgconfig support

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Apr 07 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.4.0-1
- 5.4.0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 26 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.2.0-1
- 5.2.0

* Mon Feb 29 2016 Rex Dieter <rdieter@fedoraproject.org> 5.1.25-1
- 5.1.25

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 18 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.0.0-5
- Provides: tidy-html5

* Wed Nov 18 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.0.0-4
- rebuild

* Sat Nov 14 2015 Rex Dieter <rdieter@fedoraproject.org> 5.0.0-3
- compat header symlinks to preserve old api (for now)

* Fri Nov 13 2015 Rex Dieter <rdieter@fedoraproject.org> 5.0.0-2
- .spec cosmetics/cleanup, upstreamable cmake fixes

* Wed Nov 11 2015 Matěj Cepl <mcepl@redhat.com> - 5.0.0-1
- New upstream.

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.0-34.20091203
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.0-33.20091203
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.0-32.20091203
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Dec 03 2013 Pavel Raiskup <praiskup@redhat.com> - 0.99.0-31.20091203
- silence gcc's warnings for -Werror=format-string (#1037356)

* Thu Oct 10 2013 Pavel Raiskup <praiskup@redhat.com> - 0.99.0-30.20091203
- enable testsuite during package build

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.0-29.20091203
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 28 2013 Pavel Raiskup <praiskup@redhat.com> - 0.99.0-28.20091203
- add manual page for tab2space

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.0-27.20091203
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.0-26.20091203
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 21 2012 Rex Dieter <rdieter@fedoraproject.org> 0.99.0-25.20091203
- rebuild 2, the wrath of doxygen (#831423)

* Thu Jun 14 2012 Rex Dieter <rdieter@fedoraproject.org> 0.99.0-24.20091203
- rebuild fyand (for yet another newer doxygen) (#831423)

* Wed Jun 13 2012 Rex Dieter <rdieter@fedoraproject.org> 0.99.0-23.20091203
- rebuild for newer doxygen, avoid html doc multilib conflict (#831423)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.0-22.20091203
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.0-21.20091203
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 03 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.99.0-20.20091203
- 20091203 snapshot
- spec housecleaning
- Tidy erroniously removes whitespace, causing mangled text (#481350)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.0-19.20070615
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.0-18.20070615
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 11 2008 Rex Dieter <rdieter@fedoraproject.org> 0.99.0-17.20070615
- respin (gcc43)

* Sat Aug 25 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.99.0-16.20070615
- respin (BuildID)

* Sat Aug 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.99.0-15.20070615
- License: W3C

* Tue Jul 31 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.99.0-14.20070615
- BR: libtool (again)

* Mon Jul 09 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.99.0-13.20070615
- 2007-06-15 snapshot

* Wed Feb 28 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.99.0-12.20070228
- 2007-02-28 snapshot

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.99.0-11.20051025
- fc6 respin

* Wed Jul 12 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.99.0-10.20051025
- fc6 respin

* Wed Mar 1 2006 Rex Dieter <rexdieter[AT]users.sf.net>
- fc5: gcc/glibc respin

* Fri Jan 20 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.99.0-9.20051025
- libtidy returns to be multilib friendly

* Wed Oct 26 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.99.0-8.20051025
- Update to 051025 and docs to 051020

* Tue Aug  9 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.99.0-7.20050803
- -devel: Provides: libtidy-devel (#165452)

* Tue Aug  9 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.99.0-6.20050803
- cleanup doc generation
- add/restore missing docs (manpage, quickref.html)

* Mon Aug  8 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.99.0-5.20050803
- Update to 050803 and docs to 050705
- simplify (fedora.us bug #2071)
- drop missing manpage

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 0.99.0-4.20041214
- rebuild on all arches

* Fri Apr  8 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Thu Dec 16 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-2.20041214
- Update to 041214 and docs to 041206.
- Build with dependency tracking disabled.

* Sun Oct  3 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.2.20040916
- Update to 040916 and docs to 040810.

* Fri Aug 13 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.2.20040811
- Update to 040811, patches applied upstream.

* Wed Jul 28 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.2.20040720
- Update to 040720.
- Add partial fix (still incorrect for XHTML 1.1) for usemap handling.

* Mon Jul  5 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.2.20040704
- Update to 040704.

* Fri Jun 25 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.2.20040622
- Update to 040622.

* Sat Jun  5 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.2.20040603
- Update to 040603.

* Sat May 15 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.2.20040514
- Update to 040514.

* Sun May  2 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.2.20040318
- Update docs to 040317, and generate API docs ourselves.

* Fri Mar 19 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20040318
- Update to 040318.

* Tue Mar 16 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20040315
- Update to 040315.

* Mon Mar 15 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20040314
- Update to 040314.

* Sun Mar 14 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20040313
- Update to 040313.

* Sun Feb  8 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20040205
- Update to 040205.

* Wed Feb  4 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20040202
- Update to 040202.

* Sun Feb  1 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20040130
- Update to 040130.

* Sun Jan 25 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20040124
- Update to 040124.
- Honor optflags more closely.

* Sun Jan 11 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20040110
- Update to 040110.

* Thu Jan  8 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20040106
- Update to 040106.

* Tue Jan  6 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20040104
- Update to 040104.

* Sun Nov  2 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20031101
- Update to 031101.

* Thu Oct 30 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20031029
- Update to 031029.

* Fri Oct  3 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20031002
- Update to 031002.

* Sat Sep 27 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20030926
- Update to 030926.

* Wed Sep  3 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20030901
- Update to 030901.

* Sat Aug 16 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20030815
- Update to 030815.

* Sat Aug  2 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20030801
- Update to 030801.

* Mon Jul 21 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.0-0.fdr.1.20030716
- First build.
