# TODO: kill unaligned accesses (create_db,gpre_current,gbak_static,isql_static) on alpha
Summary:	Firebird SQL Database Server and Client tools
Summary(pl):	Firebird - serwer baz danych SQL oraz narzêdzia klienckie
Name:		Firebird
# FirebirdCS/FirebirdSS (Classic Server/Super Server)?
Version:	1.5.2.4731
Release:	1
License:	Interbase Public License 1.0
Group:		Applications/Databases
Source0:	http://dl.sourceforge.net/firebird/firebird-%{version}.tar.bz2
# Source0-md5:	fea53ed5213cff4bd96513fb1a6c0ca2
Source1:	http://www.ibphoenix.com/downloads/60All.zip
# Source1-md5:	f86a132012361cd4ae88563105741a4c
Source2:	http://www.ibphoenix.com/downloads/ib_4_0_docs.tar.gz
# Source2-md5:	f4176d5dec952ee774bb8ee74c1f715d
Source3:	http://www.ibphoenix.com/downloads/isc_docs.zip
# Source3-md5:	66eef71c188215d10988788282c014a7
Patch0:		%{name}-chmod.patch
Patch1:		%{name}-editline.patch
Patch2:		%{name}-env-overflows.patch
Patch3:		%{name}-va.patch
Patch4:		%{name}-morearchs.patch
URL:		http://firebird.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	libstdc++-devel
BuildRequires:	ncurses-devel
BuildRequires:	unzip
Requires:	%{name}-lib = %{version}-%{release}
# official ports are x86, sparc and amd64
# alpha and ppc added in morearchs patch
# see morearchs patch if you want to add support for more archs
ExclusiveArch:	%{ix86} amd64 sparc sparcv9 alpha ppc
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
	--prefix=%{ibdir} \
	%{?debug:--enable-debug}
# --enable-superserver

# OPTFLAGS for editline
export OPTFLAGS="%{rpmcflags}"
%ifarch amd64
DARCH="-DAMD64"
%else
%ifarch sparc sparcv9
DARCH="-Dsparc"
%else
DARCH=""
%endif
%endif
%{__make} -j1 \
	PROD_FLAGS="%{rpmcflags} -DNDEBUG -DLINUX -pipe -MMD -fPIC $DARCH" \
	DEV_FLAGS="%{rpmcflags} -DLINUX -DDEBUG_GDS_ALLOC -pipe -MMD -fPIC -Wall -Wno-switch $DARCH" \
	LIB_LINK_RPATH_LINE= \
	LIB_CLIENT_LINK_OPTIONS="-lpthread"

# fb_lock_mgr is started during build - try to stop it (if /proc is mounted...)
/sbin/fuser -k gen/firebird/bin/fb_lock_mgr 2>/dev/null || :

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C src -f ../gen/Makefile.install buildImageDir

install -d $RPM_BUILD_ROOT{%{ibdir},%{_libdir},%{_includedir}} \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
install gen/firebird/lib/libfb*.a $RPM_BUILD_ROOT%{_libdir}
cd gen/buildroot/%{ibdir}

cp -af UDF bin help intl aliases.conf firebird.conf firebird.msg security.fdb \
	$RPM_BUILD_ROOT%{ibdir}
install include/* $RPM_BUILD_ROOT%{_includedir}
cp -df lib/* $RPM_BUILD_ROOT%{_libdir}
install examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# or libfbembed?
ln -sf libfbclient.so.1.5.0 $RPM_BUILD_ROOT%{_libdir}/libgds.so.0
ln -sf libfbclient.so.1 $RPM_BUILD_ROOT%{_libdir}/libgds.so

ln -sf libfbstatic.a $RPM_BUILD_ROOT%{_libdir}/libgds.a

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`/usr/bin/getgid firebird`" ]; then
        if [ "`/usr/bin/getgid firebird`" != "145" ]; then
                echo "Error: group firebird doesn't have gid=145. Correct this before installing firebird." 1>&2
                exit 1
        fi
else
        /usr/sbin/groupadd -g 145 firebird
fi
if [ -n "`/bin/id -u firebird 2>/dev/null`" ]; then
        if [ "`/bin/id -u firebird`" != "89" ]; then
                echo "Error: user firebird doesn't have uid=145. Correct this before installing firebird." 1>&2
                exit 1
        fi
else
        /usr/sbin/useradd -u 145 \
                        -d %{ibdir} -s /bin/sh -g firebird \
                        -c "Firebird Server" firebird 1>&2
fi

%post
/sbin/chkconfig --add firebird
if [ -f /var/lock/subsys/firebird ]; then
        /etc/rc.d/init.d/firebird restart >&2
else
        echo "Run \"/etc/rc.d/init.d/firebird start\" to start firebird." >&2
fi

%preun
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/firebird ]; then
                /etc/rc.d/init.d/firebird stop
        fi
        /sbin/chkconfig --del firebird
fi

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
%attr(754,root,root) /etc/rc.d/init.d/firebird
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/firebird

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
