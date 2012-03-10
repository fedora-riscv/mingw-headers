%global snapshot_date 20120224

%global mingw_build_win32 1
%global mingw_build_win64 1

# The mingw-w64-headers provide the headers pthread_time.h
# and pthread_unistd.h by default and are dummy headers.
# The real implementation for these headers is in a separate
# library called winpthreads. As long as winpthreads isn't
# available (and the old pthreads-w32 implementation is used)
# the flag below needs to be set to 1. When winpthreads is
# available then this flag needs to be set to 0 to avoid
# a file conflict with the winpthreads headers
%global bundle_dummy_pthread_headers 1

Name:           mingw-headers
Version:        2.0.999
Release:        0.5.trunk.%{snapshot_date}%{?dist}
Summary:        Win32/Win64 header files

License:        Public Domain and LGPLv2+ and ZPLv2.1
Group:          Development/Libraries

URL:            http://mingw-w64.sourceforge.net/
%if 0%{?snapshot_date}
Source0:        http://downloads.sourceforge.net/mingw-w64/mingw-w64-src_%{snapshot_date}.tar.bz2
%else
Source0:        http://downloads.sourceforge.net/mingw-w64/mingw-w64-v%{version}.tar.gz
%endif

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw64-filesystem >= 95


%description
MinGW Windows cross-compiler Win32 and Win64 header files.


%package -n mingw32-headers
Summary:        MinGW Windows cross-compiler Win32 header files
Requires:       mingw32-filesystem >= 95
%if 0%{bundle_dummy_pthread_headers} == 0
Requires:       mingw32-winpthreads
%endif

Obsoletes:      mingw32-w32api < 3.17-3%{?dist}
Provides:       mingw32-w32api = 3.17-3%{?dist}

%description -n mingw32-headers
MinGW Windows cross-compiler Win32 header files.

%package -n mingw64-headers
Summary:        MinGW Windows cross-compiler Win64 header files
Requires:       mingw64-filesystem >= 95
%if 0%{bundle_dummy_pthread_headers} == 0
Requires:       mingw64-winpthreads
%endif

%description -n mingw64-headers
MinGW Windows cross-compiler Win64 header files.


%prep
%if 0%{?snapshot_date}
rm -rf mingw-w64-v%{version}
mkdir mingw-w64-v%{version}
cd mingw-w64-v%{version}
tar -xf %{S:0}
%setup -q -D -T -n mingw-w64-v%{version}/mingw
%else
%setup -q -n mingw-w64-v%{version}
%endif


%build
pushd mingw-w64-headers
    %mingw_configure --enable-sdk=all --enable-secure-api
popd


%install
pushd mingw-w64-headers
    %mingw_make_install DESTDIR=$RPM_BUILD_ROOT 
popd

# Move the files to a proper location
mkdir -p $RPM_BUILD_ROOT%{mingw32_includedir}
mv $RPM_BUILD_ROOT%{mingw32_prefix}/%{mingw32_target}/include/* $RPM_BUILD_ROOT%{mingw32_includedir}/
rm -rf $RPM_BUILD_ROOT%{mingw32_prefix}/%{mingw32_target}

mkdir -p $RPM_BUILD_ROOT%{mingw64_includedir}
mv $RPM_BUILD_ROOT%{mingw64_prefix}/%{mingw64_target}/include/* $RPM_BUILD_ROOT%{mingw64_includedir}/
rm -rf $RPM_BUILD_ROOT%{mingw32_prefix}/%{mingw64_target}

# Drop the dummy pthread headers if necessary
%if 0%{?bundle_dummy_pthread_headers} == 0
rm -f $RPM_BUILD_ROOT%{mingw32_includedir}/pthread_time.h
rm -f $RPM_BUILD_ROOT%{mingw32_includedir}/pthread_unistd.h
rm -f $RPM_BUILD_ROOT%{mingw64_includedir}/pthread_time.h
rm -f $RPM_BUILD_ROOT%{mingw64_includedir}/pthread_unistd.h
%endif


%files -n mingw32-headers
%doc COPYING DISCLAIMER DISCLAIMER.PD mingw-w64-headers/direct-x/COPYING.LIB
%{mingw32_includedir}/*

%files -n mingw64-headers
%doc COPYING DISCLAIMER DISCLAIMER.PD mingw-w64-headers/direct-x/COPYING.LIB
%{mingw64_includedir}/*


%changelog
* Sat Mar 03 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.5.trunk.20120224
- Bump EVR to fix upgrade path when upgrading from the testing repository

* Fri Feb 24 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.4.trunk.20120224
- Update to 20120224 snapshot
- Eliminated some conditionals related to snapshot builds
- Added DISCLAIMER, DISCLAIMER.PD and COPYING.LIB files
- Added ZPLv2.1 to the license tag
- Added a conditional which is needed to prevent a file conflict with winpthreads
- Bumped BR: mingw{32,64}-filesystem to >= 95

* Fri Feb 24 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.3.trunk.20120120
- Use smaller SourceForge source URLs
- Dropped the mingw_pkg_name global
- Dropped the quotes in the mingw_configure and mingw_make_install calls
- Improved summary of the various packages

* Fri Jan 20 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.2.trunk.20120120
- Update to mingw-w64 trunk 20120120 snapshot (fixes various errno related compile failures)

* Thu Jan 12 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.1.trunk.20120112
- Update to mingw-w64 trunk 20120112 snapshot

* Sat Nov 19 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.1-1
- Update to mingw-w64 v2.0.1

* Sat Oct 22 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0-1
- Update to mingw-w64 v2.0

* Sun Sep 25 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0-0.3.rc1
- Bumped obsoletes for mingw32-w32api
- Dropped unneeded RPM tags

* Sat Aug 13 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0-0.2.rc1
- Rebuild because of broken mingw-find-requires.sh in the mingw-filesystem package

* Mon Aug  8 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0-0.1.rc1
- Update to 2.0-rc1

* Tue Jul 12 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0-0.12.20110711.trunk
- Backported a patch for a regression which causes CLSID_ShellLink to be defined twice
  This fixes compilation of gtk3

* Tue Jul 12 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0-0.11.20110711.trunk
- Update to 20110711 snapshot of the trunk branch

* Sat Jun 25 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0-0.10.20110625.trunk
- Update to 20110625 snapshot of the trunk branch (fixes gstreamer d3d issue)

* Thu Jun  9 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0-0.9.20110609.trunk
- Update to 20110609 snapshot of the trunk branch

* Thu Apr 14 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0-0.8.20110413.trunk
- Update to 20110413 snapshot of the trunk branch
- Made the package compliant with the new packaging guidelines
- Enable the secure API (required for wine-gecko)

* Wed Jan 12 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0-0.7.20101003
- Update to 20101003 snapshot
- Generate per-target RPMs
- Bundle the COPYING file

* Fri Dec 24 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0-0.6.20100914
- Replaced my patch by an upstreamed one

* Fri Oct  8 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0-0.5.20100914
- Bundle the DDK and DirectX headers as well

* Wed Sep 29 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0-0.4.20100914
- Update to 20100914 snapshot
- Renamed the package to mingw-headers
- Obsoletes/provides the mingw32-w32api package

* Sat May 15 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0-0.3.20100513
- The 20100513 snapshot contains a bug where #include <malloc.h>
  doesn't result in declaring the symbols _aligned_malloc and _aligned_free
  Added a patch to fix this

* Fri May 14 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0-0.2.20100513
- Rebuild for new mingw64-filesystem

* Fri May 14 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0-0.1.20100513
- Update to 20100513 snapshot of the 1.0 branch
- Updated Source: URL
- Rewritten the %%build and %%install phases
- Fixed %%defattr tag
- Use the default path which GCC expects for the headers

* Wed Feb 11 2009 Richard W.M. Jones <rjones@redhat.com> - 0.1-0.svn607.10
- Started mingw64 development.

* Mon Dec 15 2008 Richard W.M. Jones <rjones@redhat.com> - 3.13-1
- New upstream version 3.13.

* Tue Dec  9 2008 Richard W.M. Jones <rjones@redhat.com> - 3.12-8
- Force rebuild to get rid of the binary bootstrap package and replace
  with package built from source.

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 3.12-7
- No runtime dependency on binutils or gcc.

* Mon Nov 24 2008 Richard W.M. Jones <rjones@redhat.com> - 3.12-6
- Rebuild against latest filesystem package.
- Rewrite the summary for accuracy and brevity.

* Fri Nov 21 2008 Richard W.M. Jones <rjones@redhat.com> - 3.12-4
- Remove obsoletes for a long dead package.
- Enable _mingw32_configure (Levente Farkas).

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 3.12-3
- Rebuild against mingw32-filesystem 37

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 3.12-2
- Rebuild against mingw32-filesystem 36

* Thu Oct 16 2008 Richard W.M. Jones <rjones@redhat.com> - 3.12-1
- New upstream version 3.12.

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11-7
- Rename mingw -> mingw32.

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11-6
- Moved ole provides to mingw-filesystem package.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11-3
- Use the RPM macros from mingw-filesystem.

* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11-2
- Initial RPM release, largely based on earlier work from several sources.
