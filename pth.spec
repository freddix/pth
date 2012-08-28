Summary:	The GNU portable threads
Name:		pth
Version:	2.0.7
Release:	3
Epoch:		1
License:	LGPL
Group:		Libraries
Source0:	http://ftp.gnu.org/gnu/pth/%{name}-%{version}.tar.gz
# Source0-md5:	9cb4a25331a4c4db866a31cbe507c793
Patch0:		%{name}-nolibs.patch
URL:		http://www.gnu.org/software/pth/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pth is a very portable POSIX/ANSI-C based library for Unix platforms
which provides non-preemptive priority-based scheduling for multiple
threads of execution (aka `multithreading') inside event-driven
applications. All threads run in the same address space of the server
application, but each thread has its own individual program-counter,
run-time stack, signal mask and errno variable.

%package devel
Summary:	Header files and development documentation for pth
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Header files and development documentation for pth.

%prep
%setup -q
%patch0 -p1
# no aclocal call: aclocal.m4 contains only local macros, libtool.m4 is included from configure.in
cp -f /usr/share/automake/config.* /usr/share/aclocal/libtool.m4 .
mv aclocal.m4 local.m4

%build
%{__libtoolize}
%{__aclocal} -I.
%{__autoheader}
%{__autoconf}
%configure \
	--disable-static \
	--enable-optimize
%{__make} pth_p.h
%{__make}
%{__make} test

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
# COPYING contains not only LGPL text
%doc ANNOUNCE AUTHORS COPYING ChangeLog HISTORY NEWS README SUPPORT TESTS THANKS USERS
%attr(755,root,root) %ghost %{_libdir}/libpth.so.??
%attr(755,root,root) %{_libdir}/libpth.so.*.*.*

%files devel
%defattr(644,root,root,755)
%doc HACKING
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libpth.so
%{_libdir}/lib*.la
%{_aclocaldir}/pth.m4
%{_includedir}/*.h
%{_mandir}/man3/*
%{_mandir}/man1/*

