Summary:	Firebird SQL Database Server and Client tools
Summary(pl):	Firebird - serwer baz danych SQL oraz narzêdzia klienckie
Name:		Firebird
# FirebirdCS/FirebirdSS (Classic Server/Super Server)?
Version:	1.5.0.4290
Release:	0.1
License:	Interbase Public License 1.0
Group:		Applications/Databases
Source0:	http://dl.sourceforge.net/firebird/firebird-%{version}.tar.bz2
# Source0-md5:	c088ccf4d149ecc1fa03ee27e9043701
#Source1:	http://dl.sourceforge.net/firebird/bootkit-%{version}.tar.gz
## Source1-md5: 3ce1d058d568242843fa0f92d5ae7018
Source2:	http://www.ibphoenix.com/downloads/60All.zip
# Source2-md5:	f86a132012361cd4ae88563105741a4c
Source3:	http://www.ibphoenix.com/downloads/ib_4_0_docs.tar.gz
# Source3-md5:	f4176d5dec952ee774bb8ee74c1f715d
Source4:	http://www.ibphoenix.com/downloads/isc_docs.zip
# Source4-md5:	66eef71c188215d10988788282c014a7
Patch0:		%{name}-chmod.patch
Patch1:		%{name}-link.patch
Patch2:		%{name}-sparc.patch
Patch3:		%{name}-va.patch
Patch4:		%{name}-types.patch
Patch5:		%{name}-morearchs.patch
#Patch4:		%{name}-env-overflows.patch
URL:		http://firebird.sourceforge.net/
BuildRequires:	libstdc++-devel
BuildRequires:	ncurses-devel
BuildRequires:	unzip
Requires:	%{name}-lib = %{version}-%{release}
# see morearchs patch if you want to add support for more 32-bit archs
ExclusiveArch:	%{ix86} sparc sparcv9
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
# incomplete, 64-bit port is broken
#%patch4 -p1
%patch5 -p1

install -d docs/{IB3.0,IB4.0,IB6.0}
unzip -q %{SOURCE2} -d docs/IB6.0
tar xzf %{SOURCE3} -C docs/IB4.0
unzip -q %{SOURCE4} -d docs/IB3.0
# standardize extension, also avoids gzipping by compress-doc
mv -f docs/IB6.0/LANGREF.{PDF,pdf}

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}

%configure \
	--prefix=%{ibdir} \
	%{?debug:--enable-debug}
# --enable-superserver

%{__make} \
	PROD_FLAGS="%{rpmcflags} -DNDEBUG -DLINUX -pipe -MMD -fPIC" \
	DEV_FLAGS="%{rpmcflags} -DLINUX -DDEBUG_GDS_ALLOC -pipe -MMD -fPIC -Wall -Wno-switch" \
	LIB_LINK_RPATH_LINE= \
	LIB_CLIENT_LINK_OPTIONS="-lpthread"

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
%{ibdir}/intl
%{ibdir}/firebird.msg
# following files should be in /var (*.fdb) and /etc (*.conf)?
%{ibdir}/security.fdb
%{ibdir}/aliases.conf
%{ibdir}/firebird.conf

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
