# TODO:
# - kill unaligned accesses (create_db,gpre_current,gbak_static,isql_static) on alpha
# - create classic server/super server subpackages and drop bcond
#   (see firebird2 on debian how to do it)
%bcond_with	ss	# Super Server
Summary:	Firebird SQL Database Server and Client tools
Summary(de):	Firebird - relationalen Open-Source- Datenbankmanagementsystems
Summary(pl):	Firebird - serwer baz danych SQL oraz narzêdzia klienckie
Name:		Firebird
# FirebirdCS/FirebirdSS (Classic Server/Super Server)?
Version:	1.5.3.4870
Release:	2
License:	Interbase Public License 1.0
Group:		Applications/Databases
Source0:	http://dl.sourceforge.net/firebird/firebird-%{version}.tar.bz2
# Source0-md5:	559d005ab6622274f9448687f930393c
Source1:	http://www.ibphoenix.com/downloads/60All.zip
# Source1-md5:	f86a132012361cd4ae88563105741a4c
Source2:	http://www.ibphoenix.com/downloads/ib_4_0_docs.tar.gz
# Source2-md5:	f4176d5dec952ee774bb8ee74c1f715d
Source3:	http://www.ibphoenix.com/downloads/isc_docs.zip
# Source3-md5:	66eef71c188215d10988788282c014a7
Source4:	firebird.init
Source5:	firebird.sysconfig
Source6:	firebird.inetd
Patch0:		%{name}-chmod.patch
Patch1:		%{name}-editline.patch
Patch2:		%{name}-va.patch
Patch3:		%{name}-morearchs.patch
Patch4:		%{name}-gcc4.patch
Patch5:		%{name}-fix-os-detection.dpatch
Patch6:		%{name}-fix-pthreads-detect.dpatch
Patch7:		%{name}-link-with-g++.dpatch
Patch8:		%{name}-no-custom-errno-and-sys_XXerrXX.dpatch
Patch9:		%{name}-opt-bypass-redundant-sort.dpatch
Patch10:	%{name}-security-remote-preauth-crash.dpatch
Patch11:	%{name}-separate-file-and-sem-perms.dpatch
URL:		http://firebird.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	ncurses-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	unzip
Requires:	%{name}-lib = %{version}-%{release}
%if %{with ss}
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
%endif
# official ports are x86, sparc and x86_64
# alpha and ppc added in morearchs patch
# see morearchs patch if you want to add support for more archs
ExclusiveArch:	%{ix86} %{x8664} sparc sparcv9 alpha ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		ibdir	%{_libdir}/interbase
%define		specflags	-fno-strict-aliasing
%define		debugcflags	-O1 -g -Wall -fno-strict-aliasing

%description
Firebird is a powerful, high-performance relational database designed
to be embedded into applications on multiple platforms.

%description -l pl
Firebird jest potê¿nym, wysoko wydajnym systemem relacyjnych baz
danych zaprojektowanym do osadzania w aplikacjach na wielu
platformach.

%description -l de
Firebird ist der Open-Source-Spin-Off des weiterhin kommerziell von
Borland vertriebenen relationalen Datenbankmanagementsystemes
InterBase. Die Abspaltung erfolgte im Jahre 2000 als kurz vor Freigabe
der Version 6 des kommerziellen Vorgängers Interbase bei Borland
ernsthafte Überlegungen im Gange waren, die Weiterentwicklung
einzustellen.

Aus Interbase 6.0 wurde Firebird 1.0, wobei dies als eine
Bugfix-Version mit nur wenigen Erweiterungen angesehen werden kann.
Eine Erweiterung von Firebird 1.0 ist der 64-Bit File I/O, so dass
auch Datenbankdateien über 2GB erzeugt werden können.

%package lib
Summary:	Firebird shared library
Summary(pl):	Biblioteka wspó³dzielona Firebird
Group:		Libraries

%description lib
Firebird shared library (libgds).

%description lib -l pl
Biblioteka wspó³dzielona Firebird (libgds).

%package devel
Summary:	Header files for Firebird library
Summary(pl):	Pliki nag³ówkowe biblioteki Firebird
Group:		Development/Libraries
Requires:	%{name}-lib = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for Firebird library.

%description devel -l pl
Pliki nag³ówkowe biblioteki Firebird.

%package static
Summary:	Static Firebird library
Summary(pl):	Statyczna biblioteka Firebird
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Firebird library (libgds).

%description static -l pl
Statyczna biblioteka Firebird (libgds).

%package doc
Summary:	Extensive InterBase and Firebird documentation
Summary(pl):	Obszerna dokumentacja do baz InterBase i Firebird
Group:		Documentation

%description doc
Extensive InterBase and Firebird documentation.

%description doc -l pl
Obszerna dokumentacja do baz InterBase i Firebird.

%prep
%setup -q -n firebird-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
install -d docs/{IB3.0,IB4.0,IB6.0}
unzip -q %{SOURCE1} -d docs/IB6.0
tar xzf %{SOURCE2} -C docs/IB4.0
unzip -q %{SOURCE3} -d docs/IB3.0
# standardize extension, also avoids gzipping by compress-doc
mv -f docs/IB6.0/LANGREF.{PDF,pdf}

%build
cd src/extern/editline
cp -f /usr/share/automake/config.* .
%{__autoconf}
cd ../../..
%{__libtoolize}
%{__aclocal}
%{__autoconf}

%configure \
	%{?with_ss:--enable-superserver} \
	--prefix=%{ibdir} \
	%{?debug:--enable-debug}

# OPTFLAGS for editline
export OPTFLAGS="%{rpmcflags}"
%ifarch %{x8664}
DARCH="-DAMD64"
%else
%ifarch sparc sparcv9
DARCH="-Dsparc"
%else
DARCH=""
%endif
%endif

%{__make} -j1 \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	PROD_FLAGS="%{rpmcflags} -DNDEBUG -DLINUX -pipe -MMD -fPIC $DARCH" \
	DEV_FLAGS="%{rpmcflags} -DLINUX -DDEBUG_GDS_ALLOC -pipe -MMD -fPIC -Wall -Wno-switch $DARCH" \
	LIB_LINK_RPATH_LINE= \
	LIB_CLIENT_LINK_OPTIONS="-lpthread"

# my name is hack. dirty hack.
# why isn't that build in previous make call?
%{__make} -C src -f ../gen/Makefile.libfbembed libfbembed \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	PROD_FLAGS="%{rpmcflags} -DNDEBUG -DLINUX -pipe -MMD -fPIC $DARCH" \
	DEV_FLAGS="%{rpmcflags} -DLINUX -DDEBUG_GDS_ALLOC -pipe -MMD -fPIC -Wall -Wno-switch $DARCH" \
	LIB_LINK_RPATH_LINE= \
	LIB_CLIENT_LINK_OPTIONS="-lpthread"

# fb_lock_mgr is started during build - try to stop it (if /proc is mounted...)
/sbin/fuser -k gen/firebird/bin/fb_lock_mgr 2>/dev/null || :

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C src -f ../gen/Makefile.install buildImageDir

install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig/rc-inetd}
install -d $RPM_BUILD_ROOT{%{ibdir},%{_libdir},%{_includedir}} \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

install gen/firebird/lib/libfb*.a $RPM_BUILD_ROOT%{_libdir}
install gen/firebird/lib/libfbembed.so* $RPM_BUILD_ROOT%{_libdir}
cd gen/buildroot/%{ibdir}

cp -af UDF bin help intl aliases.conf firebird.conf firebird.msg security.fdb \
	$RPM_BUILD_ROOT%{ibdir}
install include/* $RPM_BUILD_ROOT%{_includedir}
cp -df lib/* $RPM_BUILD_ROOT%{_libdir}
install examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# or libfbembed?
ln -sf libfbclient.so.1 $RPM_BUILD_ROOT%{_libdir}/libgds.so.0
ln -sf libfbclient.so.1 $RPM_BUILD_ROOT%{_libdir}/libgds.so

ln -sf libfbstatic.a $RPM_BUILD_ROOT%{_libdir}/libgds.a

install %{SOURCE4}	$RPM_BUILD_ROOT/etc/rc.d/init.d/firebird
install %{SOURCE5}      $RPM_BUILD_ROOT/etc/sysconfig/firebird
install %{SOURCE6}	$RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/firebird

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 145 firebird
%useradd -u 145 -d %{ibdir} -s /bin/sh -g firebird -c "Firebird Server" firebird

%if %{with ss}
%post
/sbin/chkconfig --add firebird
%service firebird restart

%preun
if [ "$1" = "0" ]; then
	%service firebird stop
	/sbin/chkconfig --del firebird
fi
%endif

%postun
if [ "$1" = "0" ]; then
	%userremove firebird
	%groupremove firebird
fi

%post	lib -p /sbin/ldconfig
%postun	lib -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc doc/{sql.extensions,Firebird_conf.txt,README.user*,WhatsNew,fb2-todo.txt}
%attr(755,root,root) %{_libdir}/libib_util.so
%dir %{ibdir}
%attr(755,root,root) %{ibdir}/UDF
%attr(755,root,root) %{ibdir}/bin
%{ibdir}/help
%dir %{ibdir}/intl
%attr(755,root,root) %{ibdir}/intl/fbintl
%{ibdir}/firebird.msg
# following files should be in /var (*.fdb) and /etc (*.conf)?
%{ibdir}/security.fdb
%{ibdir}/aliases.conf
%{ibdir}/firebird.conf
%if %{with ss}
%attr(754,root,root) /etc/rc.d/init.d/firebird
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/firebird
%else
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/firebird
%endif

%files lib
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfbclient.so.*.*.*
%attr(755,root,root) %{_libdir}/libfbembed.so.*.*.*
# InterBase/old Firebird compatibility symlinks
%attr(755,root,root) %{_libdir}/libgds.so.0
# needed here - original libgds.so.0 didn't have soname, so some old
# (possibly not open-source) apps may be linked with libgds.so
%attr(755,root,root) %{_libdir}/libgds.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfbclient.so
%attr(755,root,root) %{_libdir}/libfbembed.so
%{_includedir}/*.h
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/libfbcommon.a
%{_libdir}/libfbstatic.a
# compat link
%{_libdir}/libgds.a

%files doc
%defattr(644,root,root,755)
%doc docs/*
