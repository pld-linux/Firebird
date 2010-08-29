# TODO:
# - kill unaligned accesses (create_db,gpre_current,gbak_static,isql_static) on alpha
#   - check if it's fixed now (RISC_ALIGNMENT is defined)
# - create classic server/super server subpackages and drop bcond
#   (see firebird2 on debian how to do it)
# - logrotate script
#
# Conditional build:
%bcond_with	ss	# Super Server (standalone daemon instead of inetd service)
#
Summary:	Firebird SQL Database Server and Client tools
Summary(de.UTF-8):	Firebird - relationalen Open-Source- Datenbankmanagementsystems
Summary(pl.UTF-8):	Firebird - serwer baz danych SQL oraz narzędzia klienckie
Name:		Firebird
# FirebirdCS/FirebirdSS (Classic Server/Super Server)?
Version:	2.1.3.18185
Release:	3
License:	Interbase Public License 1.0, Initial Developer's Public License 1.0
Group:		Applications/Databases
Source0:	http://downloads.sourceforge.net/firebird/%{name}-%{version}-0.tar.bz2
# Source0-md5:	ec42bd5c85dc2f65baef185228bcc5ca
Source1:	http://www.firebirdsql.org/pdfmanual/%{name}-2.1-QuickStart.pdf
# Source1-md5:	46bb1af4b94e8c8acee1d6ef2055b2d3
# distfiles refuses this, would require some audit to allow '('/')' chars
#Source2:	http://www.firebirdsql.org/pdfmanual/Using-Firebird_(wip).pdf
## Source2-md5:	9eb90583c200bdd7292a80ecc1df1178
Source3:	http://www.firebirdsql.org/pdfmanual/%{name}-Null-Guide.pdf
# Source3-md5:	d1f8ba75fe3bb9eb9d203ce3f82a1a1a
Source4:	http://www.firebirdsql.org/pdfmanual/%{name}-Generator-Guide.pdf
# Source4-md5:	44e7568ef477072a8ad5f381c3e12a75
Source5:	http://www.firebirdsql.org/pdfmanual/MSSQL-to-%{name}.pdf
# Source5-md5:	1bd4a168e550910fc899e2aa125d83a3
Source6:	http://www.firebirdsql.org/pdfmanual/%{name}-nbackup.pdf
# Source6-md5:	7ef8a8b9a899d06bec2a5da0bb5fea0e
Source7:	http://www.firebirdsql.org/pdfmanual/%{name}-Utils-WIP.pdf
# Source7-md5:	39b9a4f3c9d9e27d985e9277ae163ceb
Source8:	http://www.firebirdnews.org/docs/fb2min.pdf
# Source8-md5:	ebac312c0afbe97b1850bdc74c553c28
Source9:	http://www.firebirdsql.org/doc/contrib/fb_2_1_errorcodes.pdf
# Source9-md5:	9ab392dc349657dbcf9a9c35acd8e8db
Source100:	firebird.init
Source101:	firebird.sysconfig
Source102:	firebird.inetd
Patch0:		%{name}-chmod.patch
Patch1:		%{name}-editline.patch
Patch2:		%{name}-va.patch
Patch3:		%{name}-morearchs.patch
Patch4:		%{name}-FHS.patch
Patch5:		%{name}-64bit.patch
Patch6:		%{name}-gcc-icu.patch
Patch7:		%{name}-btyacc-segv.patch
Patch8:		%{name}-opt.patch
URL:		http://www.firebirdsql.org/
BuildRequires:	autoconf >= 2.56
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	libedit-devel
BuildRequires:	libicu-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	psmisc >= 22.5-2
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
Requires:	%{name}-dirs = %{version}-%{release}
Requires:	%{name}-lib = %{version}-%{release}
%if %{with ss}
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
%endif
# official ports are x86, x86_64, ppc, sparc, arm, mips/mipsel, ia64
# alpha is added in morearchs patch
# see morearchs patch if you want more
ExclusiveArch:	%{ix86} %{x8664} arm ia64 mips mipsel ppc sparc sparcv9 alpha
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		ibdir	%{_libdir}/interbase
%define		specflags	-fno-strict-aliasing
%define		debugcflags	-O1 -g -Wall -fno-strict-aliasing

%description
Firebird is a powerful, high-performance relational database designed
to be embedded into applications on multiple platforms.

%description -l pl.UTF-8
Firebird jest potężnym, wysoko wydajnym systemem relacyjnych baz
danych zaprojektowanym do osadzania w aplikacjach na wielu
platformach.

%description -l de.UTF-8
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

%package dirs
Summary:	Firebird SQL Database common directories
Summary(pl.UTF-8):	Firebird - wspólne katalogi
Group:		Applications/Databases

%description dirs
Firebird SQL Database common directories.

%description dirs -l pl.UTF-8
Firebird - wspólne katalogi.

%package lib
Summary:	Firebird shared library
Summary(pl.UTF-8):	Biblioteka współdzielona Firebird
Group:		Libraries

%description lib
Firebird shared library (libgds).

%description lib -l pl.UTF-8
Biblioteka współdzielona Firebird (libgds).

%package devel
Summary:	Header files for Firebird library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Firebird
Group:		Development/Libraries
Requires:	%{name}-dirs = %{version}-%{release}
Requires:	%{name}-lib = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for Firebird library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Firebird.

%package static
Summary:	Static Firebird library
Summary(pl.UTF-8):	Statyczna biblioteka Firebird
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Firebird library (libgds).

%description static -l pl.UTF-8
Statyczna biblioteka Firebird (libgds).

%package doc
Summary:	Extensive InterBase and Firebird documentation
Summary(pl.UTF-8):	Obszerna dokumentacja do baz InterBase i Firebird
Group:		Documentation

%description doc
Extensive InterBase and Firebird documentation.

%description doc -l pl.UTF-8
Obszerna dokumentacja do baz InterBase i Firebird.

%prep
%setup -q -n %{name}-%{version}-0
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p0
%patch7 -p1
%patch8 -p1

%{__sed} -i 's,@prefix@,%{_prefix},' builds/install/misc/fb_config.in

# force rebuild
rm -f src/dsql/parse.cpp

mkdir docs
cp %{SOURCE1} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7} %{SOURCE8} %{SOURCE9} docs

# not processed by configure
%{__sed} -i -e 's/^CFLAGS.*$/& %{rpmcflags}/' extern/btyacc/Makefile
%{__sed} -i -e 's/^\(CC.*= \)gcc$/\1 %{__cc}/' extern/btyacc/Makefile

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}

%configure \
	--with-editline \
	--with-gnu-ld \
	--with-gpre-pascal \
	--with-system-editline \
	--with-system-icu \
	%{?with_ss:--enable-superserver} \
	--prefix=%{ibdir} \
	%{?debug:--enable-debug}

%{__make} -j1 \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	LIB_LINK_RPATH_LINE= \
	LIB_CLIENT_LINK_OPTIONS="-lpthread"

# fb_lock_mgr is started during build - try to stop it (if /proc is mounted...)
fuser -k gen/firebird/bin/fb_lock_mgr 2>/dev/null || :

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C src -f ../gen/Makefile.install buildImageDir

install -d $RPM_BUILD_ROOT%{_sysconfdir}/{firebird,rc.d/init.d,sysconfig/rc-inetd}
install -d $RPM_BUILD_ROOT{%{_bindir},%{ibdir},%{_libdir},%{_includedir}} \
install -d $RPM_BUILD_ROOT/var/{log,lib/firebird} \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

install gen/firebird/lib/libfb*.a $RPM_BUILD_ROOT%{_libdir}
install gen/firebird/lib/libfbembed.so* $RPM_BUILD_ROOT%{_libdir}
touch $RPM_BUILD_ROOT/var/log/firebird.log

cd gen/buildroot/%{ibdir}
install security2.fdb $RPM_BUILD_ROOT/var/lib/firebird
install *.conf $RPM_BUILD_ROOT%{_sysconfdir}/firebird
install include/* $RPM_BUILD_ROOT%{_includedir}
cp -af UDF bin help intl firebird.msg $RPM_BUILD_ROOT%{ibdir}
cp -df lib/* $RPM_BUILD_ROOT%{_libdir}
cp -rf examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# or libfbembed?
ln -sf libfbclient.so.2 $RPM_BUILD_ROOT%{_libdir}/libgds.so.0
ln -sf libfbclient.so.2 $RPM_BUILD_ROOT%{_libdir}/libgds.so

ln -sf libfbstatic.a $RPM_BUILD_ROOT%{_libdir}/libgds.a

for f in bin/{fb_lock_print,gbak,gdef,gds_drop,gfix,gpre,gsec,gsplit,gstat,nbackup}; do
	ln -sf %{ibdir}/$f $RPM_BUILD_ROOT%{_bindir}/$ff
done

%if %{with ss}
install %{SOURCE100} $RPM_BUILD_ROOT/etc/rc.d/init.d/firebird
install %{SOURCE101} $RPM_BUILD_ROOT/etc/sysconfig/firebird
%else
install %{SOURCE102} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/firebird
%endif

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

%triggerpostun -- %{name} < 2.1.1.17910-2
if [ -f %{ibdir}/aliases.conf.rpmsave ]; then
	mv -f %{ibdir}/aliases.conf.rpmsave %{_sysconfdir}/firebird/aliases.conf
fi
if [ -f %{ibdir}/firebird.conf.rpmsave ]; then
	mv -f %{ibdir}/firebird.conf.rpmsave %{_sysconfdir}/firebird/firebird.conf
fi
if [ -f %{ibdir}/security2.fdb.rpmsave ]; then
	mv -f %{ibdir}/security2.fdb.rpmsave /var/lib/firebird/security2.fdb
fi

%files
%defattr(644,root,root,755)
%doc doc/{license,sql.extensions,Firebird_conf.txt,README.user*,WhatsNew,fb2-todo.txt}
%dir %{_sysconfdir}/firebird
%attr(640,root,firebird) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/firebird/*.conf
%attr(755,root,root) %{_bindir}/fb_lock_print
%attr(755,root,root) %{_bindir}/g*
%attr(755,root,root) %{_bindir}/nbackup
%attr(755,root,root) %{_libdir}/libib_util.so
%attr(755,root,root) %{ibdir}/UDF
%attr(755,root,root) %{ibdir}/bin/*
%exclude %{ibdir}/bin/fb_config
%{ibdir}/help
%dir %attr(770,root,firebird) %{ibdir}/intl
%attr(755,root,root) %{ibdir}/intl/fbintl
# should it be moved to %{_sysconfdir} and marked as config?
%{ibdir}/intl/fbintl.conf
%{ibdir}/firebird.msg
%dir %attr(770,root,firebird) /var/lib/firebird
%attr(660,root,firebird) %config(noreplace) %verify(not md5 mtime size) /var/lib/firebird/security2.fdb
%attr(660,root,firebird) %config(noreplace) %verify(not md5 mtime size) /var/log/firebird.log

%if %{with ss}
%attr(754,root,root) /etc/rc.d/init.d/firebird
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/firebird
%else
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/firebird
%endif

%files dirs
%defattr(644,root,root,755)
%dir %{ibdir}
%dir %{ibdir}/bin

%files lib
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfbclient.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfbclient.so.2
%attr(755,root,root) %{_libdir}/libfbembed.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfbembed.so.2.1

# InterBase/old Firebird compatibility symlinks
%attr(755,root,root) %{_libdir}/libgds.so.0
# needed here - original libgds.so.0 didn't have soname, so some old
# (possibly not open-source) apps may be linked with libgds.so
%attr(755,root,root) %{_libdir}/libgds.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfbclient.so
%attr(755,root,root) %{_libdir}/libfbembed.so
%attr(755,root,root) %{ibdir}/bin/fb_config
%{_includedir}/ib_util.h
%{_includedir}/ibase.h
%{_includedir}/iberror.h
%{_includedir}/perf.h
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/libfbstatic.a
# compat link
%{_libdir}/libgds.a

%files doc
%defattr(644,root,root,755)
%doc docs/*
