# TODO:
# - check running
# - 2.5 -> 3.0 migration?
# - more docs from http://www.firebirdsql.org/en/reference-manuals/ ?
# - kill unaligned accesses (create_db,gpre_current,gbak_static,isql_static) on alpha
#   - check if it's fixed now (RISC_ALIGNMENT is defined)
# - check classic subpackage pre/post scripts
# - logrotate script
# - create SYSDBA user with initial password before first firebird start
#   eg.:
#     su firebird
#     echo "create user SYSDBA password 'masterkey';"|fb_isql -u SYSDBA /var/lib/firebird/security5.fdb
#
Summary:	Firebird SQL Database Server and Client tools
Summary(de.UTF-8):	Firebird - relationalen Open-Source- Datenbankmanagementsystems
Summary(pl.UTF-8):	Firebird - serwer baz danych SQL oraz narzędzia klienckie
Name:		Firebird
Version:	5.0.0.1306
Release:	1
License:	Interbase Public License 1.0, Initial Developer's Public License 1.0
Group:		Applications/Databases
Source0:	https://github.com/FirebirdSQL/firebird/releases/download/v5.0.0/%{name}-%{version}-0-source.tar.xz
# Source0-md5:	9d8b64e922df57d6a3f3de1acca4f8e3
Source1:	https://firebirdsql.org/file/documentation/pdf/en/firebirddocs/qsg5/firebird-5-quickstartguide.pdf
# Source1-md5:	c02b14827cc050806bf107fd85a18458
# distfiles refuses this, would require some audit to allow '('/')' chars
#Source2:	http://www.firebirdsql.org/pdfmanual/Using-Firebird_(wip).pdf
## Source2-md5:	9eb90583c200bdd7292a80ecc1df1178
Source3:	http://www.firebirdsql.org/pdfmanual/%{name}-Null-Guide.pdf
# Source3-md5:	dc8e5e234b2138af9a472feca6565359
Source4:	http://www.firebirdsql.org/pdfmanual/%{name}-Generator-Guide.pdf
# Source4-md5:	23926037205ab8716cf0a54544585231
Source5:	http://www.firebirdsql.org/pdfmanual/MSSQL-to-%{name}.pdf
# Source5-md5:	230ef237842d255916398f408f459281
Source6:	http://www.firebirdsql.org/pdfmanual/%{name}-nbackup.pdf
# Source6-md5:	98d310a374ecc3f1f241e1feac6e4dca
Source7:	http://www.firebirdsql.org/pdfmanual/%{name}-shell-scripts.pdf
# Source7-md5:	01c5e91de9f1639f62f93b3e486584c8
Source8:	http://www.firebirdnews.org/docs/fb2min.pdf
# Source8-md5:	5e192abaf5db4417b29ad871716522b5
Source9:	https://firebirdsql.org/file/documentation/reference_manuals/reference_material/Firebird-2.1-ErrorCodes.pdf
# Source9-md5:	9ab392dc349657dbcf9a9c35acd8e8db
Source10:	http://www.firebirdsql.org/pdfmanual/%{name}-gsec.pdf
# Source10-md5:	326ef6f7afebf369b534838945ee4f74
Source11:	http://www.firebirdsql.org/pdfmanual/%{name}-gfix.pdf
# Source11-md5:	22e2cdc1058dd4f764728bcb3a8644f0
Source12:	http://www.firebirdsql.org/pdfmanual/%{name}-gsplit.pdf
# Source12-md5:	0147b5d2118e2e80c93762600107a71f
Source13:	https://firebirdsql.org/file/documentation/pdf/en/refdocs/fblangref50/firebird-50-language-reference.pdf
# Source13-md5:	cf095a223a7b7f631e6a4b8a9604b1da
Source100:	firebird.init
Source101:	firebird.sysconfig
Source102:	firebird.inetd
Source103:	firebird.tmpfiles
Source104:	firebird.service
Source105:	firebird-classic.service
Source106:	firebird-classic.socket
Source107:	server_mode-ss.conf
Source108:	server_mode-classic.conf
Source109:	fb_config
Patch0:		%{name}-chmod.patch
Patch1:		%{name}-editline.patch
Patch2:		%{name}-va.patch
Patch3:		%{name}-FHS.patch
Patch4:		%{name}-opt.patch
Patch5:		%{name}-shared-libstdc++.patch
Patch6:		%{name}-libpath.patch
Patch7:		add-pkgconfig-files.patch
Patch10:	no-copy-from-icu.patch
Patch11:	config.patch
Patch12:	chown.patch
Patch13:	cloop-honour-build-flags.patch
Patch14:	mod_loader.patch
Patch15:	x32.patch
URL:		http://www.firebirdsql.org/
BuildRequires:	autoconf >= 2.67
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	libatomic_ops
BuildRequires:	libedit-devel
BuildRequires:	libicu-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtomcrypt-devel
BuildRequires:	libtommath-devel
BuildRequires:	libtool >= 2:2
# for lockfile
BuildRequires:	procmail
BuildRequires:	re2-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
BuildRequires:	zlib-devel
Requires:	%{name}-dirs = %{version}-%{release}
Requires:	%{name}-lib = %{version}-%{release}
# official ports are x86, x86_64, ppc, sparc, arm, mips/mipsel, ia64
# alpha is added in morearchs patch
# see morearchs patch if you want more
ExclusiveArch:	%{ix86} %{x8664} x32 arm ia64 mips mipsel ppc sparc sparcv9 alpha
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		filterout	-flto
%define		ibdir	%{_libdir}/interbase
%define		specflags	-fno-strict-aliasing
%define		debugcflags	-O1 -g -Wall -fno-strict-aliasing
%define		Werror_cflags	''

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
Obsoletes:	Firebird-static < 3

%description devel
Header files for Firebird library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Firebird.

%package doc
Summary:	Extensive InterBase and Firebird documentation
Summary(pl.UTF-8):	Obszerna dokumentacja do baz InterBase i Firebird
Group:		Documentation

%description doc
Extensive InterBase and Firebird documentation.

%description doc -l pl.UTF-8
Obszerna dokumentacja do baz InterBase i Firebird.

%package ss
Summary:	Firebird SuperServer init scripts
Summary(pl.UTF-8):	Skrypty startowe Firebirda jako SuperServera
Group:		Daemons
Requires:	%{name} = %{version}-%{release}
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts

%description ss
Firebird SuperServer init scripts.

%description ss -l pl.UTF-8
Skrypty startowe Firebirda jako SuperServera.

%package classic
Summary:	Firebird Classic init scripts
Summary(pl.UTF-8):	Skrypty startowe Firebirda w wersji Classic
Group:		Daemons
Requires:	%{name} = %{version}-%{release}

%description classic
Firebird Classic (inetd) init scripts.

%description classic -l pl.UTF-8
Skrypty startowe Firebirda w wersji Classic (inetd).

%prep
%setup -q -n %{name}-%{version}-0-source
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1

mkdir docs
cp %{SOURCE1} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7} %{SOURCE8} %{SOURCE9} \
  %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} docs

# not processed by configure
%{__sed} -i -e 's/^CFLAGS.*$/& %{rpmcflags} %{rpmcppflags}/' extern/btyacc/Makefile
%{__sed} -i -e 's;^\(CC\|LINKER\)\(.*= \)gcc$;\1\2 %{__cc};' extern/btyacc/Makefile

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}

%configure \
	CFLAGS="%{rpmcflags} -fno-delete-null-pointer-checks" \
	--prefix=%{ibdir} \
	--with-fbconf=%{_sysconfdir}/firebird \
	--with-fbinclude=%{_includedir} \
	--with-fblib=%{_libdir} \
	--with-fblog=/var/log \
	--with-fbsecure-db=/var/lib/firebird \
	--with-fbglock=/var/lib/firebird \
	--with-gnu-ld \
	--with-gpre-pascal \
	--with-system-editline \
	--with-system-re2 \
	%{?debug:--enable-debug} \
	--disable-rpath \
	--disable-binreloc

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C src -f ../gen/Makefile.install buildRoot

install -d $RPM_BUILD_ROOT%{_sysconfdir}/{firebird{,/conf.d},rc.d/init.d,sysconfig/rc-inetd}
install -d $RPM_BUILD_ROOT{%{_bindir},%{ibdir},%{_libdir},%{_includedir},%{_pkgconfigdir}} \
install -d $RPM_BUILD_ROOT/var/{log,lib/firebird} \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/tmpfiles.d
install -d $RPM_BUILD_ROOT%{systemdunitdir}
cp -p %{SOURCE103} $RPM_BUILD_ROOT%{_sysconfdir}/tmpfiles.d/firebird.conf
touch $RPM_BUILD_ROOT/var/log/firebird.log

cp -p gen/install/misc/fbclient.pc $RPM_BUILD_ROOT%{_pkgconfigdir}

cd gen/buildroot
cp -p var/lib/firebird/security5.fdb $RPM_BUILD_ROOT/var/lib/firebird
cp -p etc/firebird/*.conf $RPM_BUILD_ROOT%{_sysconfdir}/firebird
cp -dp usr/%{_lib}/*.so* $RPM_BUILD_ROOT%{_libdir}
chmod 755 usr/include/firebird/impl
cp -pr usr/include/* $RPM_BUILD_ROOT%{_includedir}
# missing in buildroot
cp -p ../Release/firebird/include/firebird/FirebirdInterface.idl $RPM_BUILD_ROOT%{_includedir}/firebird
cp -p ../Release/firebird/include/firebird/impl/iberror_c.h $RPM_BUILD_ROOT%{_includedir}/firebird/impl

cd .%{ibdir}
cp -a bin intl plugins firebird.msg $RPM_BUILD_ROOT%{ibdir}
ln -s %{ibdir}/intl $RPM_BUILD_ROOT%{_sysconfdir}/firebird
ln -s %{ibdir}/{bin,plugins,firebird.msg} $RPM_BUILD_ROOT%{_sysconfdir}/firebird
chmod u+w -R examples # allow further cleaning
cp -rf examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

ln -sf libfbclient.so.2 $RPM_BUILD_ROOT%{_libdir}/libgds.so.0
ln -sf libfbclient.so.2 $RPM_BUILD_ROOT%{_libdir}/libgds.so

for f in bin/{fb_lock_print,gbak,gfix,gpre,gsec,gsplit,gstat,nbackup}; do
	ln -sf %{ibdir}/$f $RPM_BUILD_ROOT%{_bindir}/${f#bin/}
done
ln -sf %{ibdir}/bin/isql $RPM_BUILD_ROOT%{_bindir}/fb_isql

%{__rm} $RPM_BUILD_ROOT%{ibdir}/bin/{FirebirdUninstall.sh,changeServerMode.sh}

sed -e 's|/usr/lib|%{_libdir}|' %{SOURCE100} >$RPM_BUILD_ROOT/etc/rc.d/init.d/firebird
cp -p %{SOURCE101} $RPM_BUILD_ROOT/etc/sysconfig/firebird
sed -e 's|/usr/lib|%{_libdir}|' %{SOURCE104} >$RPM_BUILD_ROOT%{systemdunitdir}/firebird.service
install -d $RPM_BUILD_ROOT/run/firebird

sed -e 's|/usr/lib|%{_libdir}|' %{SOURCE102} >$RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/firebird
sed -e 's|/usr/lib|%{_libdir}|' %{SOURCE105} >$RPM_BUILD_ROOT%{systemdunitdir}/firebird-classic@.service
cp -p %{SOURCE106} $RPM_BUILD_ROOT%{systemdunitdir}/firebird-classic.socket

cp -p %{SOURCE107} $RPM_BUILD_ROOT%{_sysconfdir}/firebird/conf.d/
cp -p %{SOURCE108} $RPM_BUILD_ROOT%{_sysconfdir}/firebird/conf.d/
install -p %{_sourcedir}/fb_config $RPM_BUILD_ROOT%{_bindir}/fb_config

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 145 firebird
%useradd -u 145 -d %{ibdir} -s /bin/sh -g firebird -c "Firebird Server" firebird

%postun
if [ "$1" = "0" ]; then
	%userremove firebird
	%groupremove firebird
fi

%post	lib -p /sbin/ldconfig
%postun	lib -p /sbin/ldconfig

%post ss
/sbin/chkconfig --add firebird
%service firebird restart
%systemd_post firebird.service

%preun ss
if [ "$1" = "0" ]; then
	%service firebird stop
	/sbin/chkconfig --del firebird
fi
%systemd_preun firebird.service

%postun ss
%systemd_reload

%post classic
%systemd_post firebird-classic@.service firebird-classic.socket

%preun classic
%systemd_preun firebird-classic@.service firebird-classic.socket

%postun classic
%systemd_reload

%triggerpostun -- %{name} < 2.1.1.17910-2
if [ -f %{ibdir}/firebird.conf.rpmsave ]; then
	mv -f %{ibdir}/firebird.conf.rpmsave %{_sysconfdir}/firebird/firebird.conf
fi

%files
%defattr(644,root,root,755)
%doc doc/{license,sql.extensions,Firebird_conf.txt,README.user*}
%dir %{_sysconfdir}/firebird
%dir %{_sysconfdir}/firebird/conf.d
%attr(640,root,firebird) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/firebird/databases.conf
%attr(640,root,firebird) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/firebird/fbtrace.conf
%attr(640,root,firebird) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/firebird/firebird.conf
%attr(640,root,firebird) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/firebird/plugins.conf
%attr(640,root,firebird) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/firebird/replication.conf
%{_sysconfdir}/firebird/intl
%{_sysconfdir}/firebird/bin
%{_sysconfdir}/firebird/firebird.msg
%{_sysconfdir}/firebird/plugins
%attr(755,root,root) %{_bindir}/fb_isql
%attr(755,root,root) %{_bindir}/fb_lock_print
%attr(755,root,root) %{_bindir}/gbak
%attr(755,root,root) %{_bindir}/gfix
%attr(755,root,root) %{_bindir}/gsec
%attr(755,root,root) %{_bindir}/gsplit
%attr(755,root,root) %{_bindir}/gstat
%attr(755,root,root) %{_bindir}/nbackup
%attr(755,root,root) %{_libdir}/libib_util.so
%attr(755,root,root) %{ibdir}/bin/*
%exclude %{ibdir}/bin/fb_config
%exclude %{ibdir}/bin/gpre
%exclude %{ibdir}/bin/fbguard
%dir %{ibdir}/intl
%attr(755,root,root) %{ibdir}/intl/fbintl
# should it be moved to %{_sysconfdir} and marked as config?
%{ibdir}/intl/fbintl.conf
%dir %{ibdir}/plugins
%attr(755,root,root) %{ibdir}/plugins/libChaCha.so
%attr(755,root,root) %{ibdir}/plugins/libDefault_Profiler.so
%attr(755,root,root) %{ibdir}/plugins/libfbtrace.so
%attr(755,root,root) %{ibdir}/plugins/libEngine13.so
%attr(755,root,root) %{ibdir}/plugins/libLegacy_Auth.so
%attr(755,root,root) %{ibdir}/plugins/libLegacy_UserManager.so
%attr(755,root,root) %{ibdir}/plugins/libSrp.so
%attr(755,root,root) %{ibdir}/plugins/libudr_engine.so
%dir %{ibdir}/plugins/udr
%attr(755,root,root) %{ibdir}/plugins/udr/libudf_compat.so
%{ibdir}/plugins/udr/udf_compat.sql
%attr(755,root,root) %{ibdir}/plugins/udr/libudrcpp_example.so
%{ibdir}/plugins/udr_engine.conf

%{ibdir}/firebird.msg
%dir %attr(770,root,firebird) /var/lib/firebird
%attr(660,root,firebird) %config(noreplace) %verify(not md5 mtime size) /var/lib/firebird/security5.fdb
%attr(660,root,firebird) %config(noreplace) %verify(not md5 mtime size) /var/log/firebird.log


%files dirs
%defattr(644,root,root,755)
%dir %{ibdir}
%dir %{ibdir}/bin

%files lib
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfbclient.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfbclient.so.2

# InterBase/old Firebird compatibility symlinks
%attr(755,root,root) %{_libdir}/libgds.so.0
# needed here - original libgds.so.0 didn't have soname, so some old
# (possibly not open-source) apps may be linked with libgds.so
%attr(755,root,root) %{_libdir}/libgds.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/fb_config
%attr(755,root,root) %{_libdir}/libfbclient.so
%attr(755,root,root) %{ibdir}/bin/fb_config
%attr(755,root,root) %{ibdir}/bin/gpre
%attr(755,root,root) %{_bindir}/gpre
%{_pkgconfigdir}/fbclient.pc
%{_includedir}/firebird
%{_includedir}/ib_util.h
%{_includedir}/ibase.h
%{_includedir}/iberror.h
%{_includedir}/perf.h
%{_examplesdir}/%{name}-%{version}

%files doc
%defattr(644,root,root,755)
%doc docs/*

%files ss
%defattr(644,root,root,755)
%attr(640,root,firebird) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/firebird/conf.d/server_mode-ss.conf
%attr(754,root,root) /etc/rc.d/init.d/firebird
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/firebird
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/tmpfiles.d/firebird.conf
%attr(755,root,root) %{ibdir}/bin/fbguard
%dir %attr(770,root,firebird) /run/firebird
%{systemdunitdir}/firebird.service

%files classic
%defattr(644,root,root,755)
%attr(640,root,firebird) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/firebird/conf.d/server_mode-classic.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/firebird
%{systemdunitdir}/firebird-classic@.service
%{systemdunitdir}/firebird-classic.socket
