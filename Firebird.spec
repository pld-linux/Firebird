Summary:	Firebird SQL Database Server and Client tools
Summary(pl):	Firebird - serwer baz danych SQL oraz narz�dzia klienckie
Name:		Firebird
# FirebirdCS/FirebirdSS (Classic Server/Super Server)?
Version:	1.0.2.908
Release:	1
License:	Interbase Public License 1.0
Group:		Applications/Databases
Source0:	ftp://ftp.sourceforge.net/pub/sourceforge/firebird/%{name}-%{version}.src.tar.gz
Source1:	ftp://ftp.sourceforge.net/pub/sourceforge/firebird/bootkit-%{version}.tar.gz
Source2:	http://www.ibphoenix.com/downloads/60All.zip
Source3:	http://www.ibphoenix.com/downloads/ib_4_0_docs.tar.gz
Source4:	http://www.ibphoenix.com/downloads/isc_docs.zip
# dirty "fixes" for missing error contants and conflict with isql from unixODBC
# (gds__bad_{limit,skip}_param are defined in supplied codes.h, but removed
#  by codes.h regeneration from messages.gbak(?))
Patch0:		%{name}-fix.patch
URL:		http://firebird.sourceforge.net/
BuildRequires:	unzip
Requires:	%{name}-lib = %{version}
# see firebird-*/jrd/{common.h,gds.h,ibase.h} if you want to add support for more
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		ibdir	%{_libdir}/interbase

%description
Firebird is a powerful, high-performance relational database designed
to be embedded into applications on multiple platforms.

%description -l pl
Firebird jest pot�nym, wysoko wydajnym systemem relacyjnych baz
danych zaprojektowanym do osadzania w aplikacjach na wielu
platformach.

%package lib
Summary:	Firebird shared library
Summary(pl):	Biblioteka wsp�dzielona Firebird
Group:		Libraries

%description lib
Firebird shared library (libgds).

%description lib -l pl
Biblioteka wsp�dzielona Firebird (libgds).

%package devel
Summary:	Header files for Firebird library
Summary(pl):	Pliki nag��wkowe biblioteki Firebird
Group:		Development/Libraries
Requires:	%{name}-lib = %{version}

%description devel
Header files for Firebird library.

%description devel -l pl
Pliki nag��wkowe biblioteki Firebird.

%package static
Summary:	Static Firebird library
Summary(pl):	Statyczna biblioteka Firebird
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

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
%setup -q -n firebird-%{version} -a1
%patch0 -p1

install -d docs/{IB3.0,IB4.0,IB6.0}
unzip -q %{SOURCE2} -d docs/IB6.0
tar xzf %{SOURCE3} -C docs/IB4.0
unzip -q %{SOURCE4} -d docs/IB3.0
# standardize extension, also avoids gzipping by compress-doc
mv -f docs/IB6.0/LANGREF.{PDF,pdf}

%build
INTERBASE=/usr/lib/interbase; export INTERBASE
echo 'y' | ./Configure.sh PROD
. ./Configure_SetupEnv.sh

%{__make} firebird \
	CC="%{__cc}" \
	PROD_CFLAGS="%{rpmcflags} -fpic -DFLINTSTONE"

# classic/super - what's the difference?
#%{__make} super_firebird

#-Isource/interbase/include"

%install
rm -rf $RPM_BUILD_ROOT
INTERBASE=/usr/lib/interbase; export INTERBASE
. ./Configure_SetupEnv.sh

%{__make} buildclassicimage -f firebird/install/linux/Makefile

install -d $RPM_BUILD_ROOT{%{ibdir},%{_libdir},%{_includedir}} \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cd buildroot/opt/interbase
rm -f bin/isc4.gbak
cp -af UDF bin help intl interbase.msg isc4.gdb isc_config \
	$RPM_BUILD_ROOT%{ibdir}
install include/* $RPM_BUILD_ROOT%{_includedir}
install lib/* $RPM_BUILD_ROOT%{_libdir}
install examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc builds_win32/install/{*License,Readme}.txt
%attr(755,root,root) %{_libdir}/libib_util.so
%dir %{ibdir}
%attr(755,root,root) %{ibdir}/UDF
%attr(755,root,root) %{ibdir}/bin
%{ibdir}/help
%{ibdir}/intl
%{ibdir}/interbase.msg
# following two files should be in /var and /etc resp.?
%{ibdir}/isc4.gdb
%{ibdir}/isc_config

%files lib
%defattr(644,root,root,755)
# .so link needed here - library doesn't have SONAME
%attr(755,root,root) %{_libdir}/libgds.so*

%files devel
%defattr(644,root,root,755)
%{_includedir}/*
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/libgds.a

%files doc
%defattr(644,root,root,755)
%doc docs/*
