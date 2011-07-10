### Abstract ###

Name: rarian
Version: 0.8.1
Release: 5.1%{?dist}
License: LGPLv2+
Group: System Environment/Base
Summary: Documentation meta-data library
URL: http://rarian.freedesktop.org/
Source: http://download.gnome.org/sources/rarian/0.8/rarian-%{version}.tar.bz2
Source1: scrollkeeper-omf.dtd
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

### Patch ###

# RH bug #453342
Patch1: rarian-0.8.1-categories.patch

### Dependencies ###

Requires(post): libxml2
Requires(postun): libxml2
# for /usr/bin/xmlcatalog

Requires: libxslt
# for /usr/bin/xsltproc
Requires: coreutils, util-linux, gawk
# for basename, getopt, awk, etc

### Build Dependencies ###

BuildRequires: libxslt-devel

%description
Rarian is a documentation meta-data library that allows access to documents,
man pages and info pages.  It was designed as a replacement for scrollkeeper.

%package compat
License: GPLv2+
Group: System Environment/Base
Summary: Extra files for compatibility with scrollkeeper
Requires: rarian = %{version}-%{release}
Requires(post): rarian
# The scrollkeeper version is arbitrary.  It just
# needs to be greater than what we're obsoleting.
Provides: scrollkeeper = 0.4
Obsoletes: scrollkeeper <= 0.3.14

%description compat
This package contains files needed to maintain backward-compatibility with
scrollkeeper.

%package devel
Group: Development/Languages
Summary: Development files for Rarian
Requires: rarian = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains files required to develop applications that use the
Rarian library ("librarian").

%prep
%setup -q
%patch1 -p1 -b .categories

%build

%configure --disable-skdb-update
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_datadir}/xml/scrollkeeper/dtds
cp %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/xml/scrollkeeper/dtds

rm -rf $RPM_BUILD_ROOT%{_libdir}/librarian.a
rm -rf $RPM_BUILD_ROOT%{_libdir}/librarian.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%post compat
%{_bindir}/rarian-sk-update

# Add OMF DTD to XML catalog.
CATALOG=/etc/xml/catalog
/usr/bin/xmlcatalog --noout --add "rewriteSystem" \
  "http://scrollkeeper.sourceforge.net/dtds/scrollkeeper-omf-1.0/scrollkeeper-omf.dtd" \
  "/usr/share/xml/scrollkeeper/dtds/scrollkeeper-omf.dtd" $CATALOG >& /dev/null || :
/usr/bin/xmlcatalog --noout --add "rewriteURI" \
  "http://scrollkeeper.sourceforge.net/dtds/scrollkeeper-omf-1.0/scrollkeeper-omf.dtd" \
  "/usr/share/xml/scrollkeeper/dtds/scrollkeeper-omf.dtd" $CATALOG >& /dev/null || :

%postun -p /sbin/ldconfig

%postun compat

# Delete OMF DTD from XML catalog.
if [ $1 = 0 ]; then
  CATALOG=/etc/xml/catalog
  /usr/bin/xmlcatalog --noout --del \
    "/usr/share/xml/scrollkeeper/dtds/scrollkeeper-omf.dtd" $CATALOG >& /dev/null || :
fi

%files
%defattr(-,root,root,-)
%doc README COPYING COPYING.LIB COPYING.UTILS ChangeLog NEWS AUTHORS
%{_bindir}/rarian-example
%{_libdir}/librarian.so.*
%{_datadir}/librarian
%{_datadir}/help

%files compat
%defattr(-,root,root,-)
%{_bindir}/rarian-sk-*
%{_bindir}/scrollkeeper-*
%{_datadir}/xml/scrollkeeper

%files devel
%defattr(644,root,root,755)
%{_includedir}/rarian
%{_libdir}/librarian.so
%{_libdir}/pkgconfig/rarian.pc

%changelog
* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.8.1-5.1
- Rebuilt for RHEL 6

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 22 2008 Matthew Barnes <mbarnes@redhat.com> - 0.8.1-3
- Shorten the summary.

* Mon Nov 10 2008 Matthew Barnes <mbarnes@redhat.com> - 0.8.1-2
- Add patch for RH bug #453342 (OMF category parsing).

* Mon Sep 01 2008 Matthew Barnes <mbarnes@redhat.com> - 0.8.1-1
- Update to 0.8.1

* Sun May  4 2008 Matthias Clasen <mclasen@redhat.com> - 0.8.0-2
- Fix source url

* Mon Feb 18 2008 Matthew Barnes <mbarnes@redhat.com> - 0.8.0-1
- Update to 0.8.0
- Silence xmlcatalog commands (RH bug #433315).

* Mon Feb 18 2008 Matthew Barnes <mbarnes@redhat.com> - 0.7.1-3
- Require libxml2 in %%post and %%postun (RH bug #433268).

* Sat Feb 09 2008 Matthew Barnes <mbarnes@redhat.com> - 0.7.1-2
- Install XML DTD for scrollkeeper OMF files (RH bug #431088).

* Tue Jan 08 2008 - Bastien Nocera <bnocera@redhat.com> - 0.7.1-1
- Update to 0.7.1

* Mon Nov 26 2007 Matthew Barnes <mbarnes@redhat.com> - 0.7.0-1
- Update to 0.7.0

* Tue Nov 06 2007 Matthew Barnes <mbarnes@redhat.com> - 0.6.0-2
- Own /usr/share/help (RH bug #363311).

* Wed Sep 12 2007 Matthew Barnes <mbarnes@redhat.com> - 0.6.0-1
- Update to 0.6.0
- Remove patch for RH bug #254301 (fixed upstream).

* Thu Aug 30 2007 Matthew Barnes <mbarnes@redhat.com> - 0.5.8-3
- Add patch for RH bug #254301 (rarian-sk-config --omfdir).

* Wed Aug 22 2007 Matthew Barnes <mbarnes@redhat.com> - 0.5.8-2
- Mass rebuild

* Mon Aug 13 2007 Matthew Barnes <mbarnes@redhat.com> - 0.5.8-1
- Update to 0.5.8

* Thu Aug  9 2007 Matthias Clasen <mclasen@redhat.com> - 0.5.6-5
- Move Provides and Obsoletes in the same package, to
  avoid unnessary complications

* Sat Aug  4 2007 Matthias Clasen <mclasen@redhat.com> - 0.5.6-4
- Add a few missing Requires

* Thu Aug 02 2007 Matthew Barnes <mbarnes@redhat.com> - 0.5.6-3
- Fix the Obsoletes/Provides relationship.

* Wed Aug 01 2007 Matthew Barnes <mbarnes@redhat.com> - 0.5.6-2
- More package review feedback (#250150).

* Wed Aug 01 2007 Matthew Barnes <mbarnes@redhat.com> - 0.5.6-1
- Update to 0.5.6

* Tue Jul 31 2007 Matthew Barnes <mbarnes@redhat.com> - 0.5.4-2
- Incorporate package review suggestions.

* Mon Jul 30 2007 Matthew Barnes <mbarnes@redhat.com> - 0.5.4-1
- Initial packaging.
