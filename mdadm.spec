#
# Conditional build:
%bcond_with	initrd		# don't build initrd version
%bcond_with	dietlibc	# link initrd version with static glibc instead of dietlibc
%bcond_without	tests		# don't perform "make test"

Summary:	Tool for creating and maintaining software RAID devices
Summary(pl.UTF-8):	Narzędzie do tworzenia i obsługi programowych macierzy RAID
Name:		mdadm
Version:	3.3.1
Release:	1
License:	GPL v2+
Group:		Base
Source0:	https://www.kernel.org/pub/linux/utils/raid/mdadm/%{name}-%{version}.tar.xz
# Source0-md5:	4227d48de62dfb217c92fa0c54171bbe
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.cron
Source4:	%{name}-checkarray
URL:		https://www.kernel.org/pub/linux/utils/raid/mdadm/
BuildRequires:	groff
BuildRequires:	rpmbuild(macros) >= 1.213
%if %{with initrd}
	%if %{with dietlibc}
BuildRequires:	dietlibc-static
	%else
BuildRequires:	glibc-static
	%endif
%endif
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,preun):	/sbin/chkconfig
Requires:	/sbin/chkconfig
Requires:	rc-scripts >= 0.4.2.4-2
Suggests:	crondaemon
%{!?with_initrd:Obsoletes:	mdadm-initrd < %{version}-%{release}}
Obsoletes:	mdctl
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir		/sbin

%description
This package includes tool you need to set up and maintain a software
RAID device under Linux. It's thought as an alternative to raidtools
package.

%description -l pl.UTF-8
Pakiet ten zawiera narzędzie potrzebne do tworzenia i obsługi
programowych macierzy RAID. Program ten jest pomyślany jako
alternatywa dla pakietu raidtools.

%package initrd
Summary:	Tool for maintaining software RAID devices - initrd version
Summary(pl.UTF-8):	Narzędzie do obsługi programowych macierzy RAID, wersja dla initrd
Group:		Base
Conflicts:	geninitrd < 10000.10

%description initrd
Tool for maintaining software RAID devices - statically linked for
initrd.

%description initrd -l pl.UTF-8
Narzędzie do zarządzania programowymi macierzami RAID - statycznie
skonsolidowane na potrzeby initrd.

%prep
%setup -q

%build
%if %{with initrd}
%if %{with dietlibc}
%{__make} mdadm \
	CC="diet %{__cc} %{rpmcflags} %{rpmcppflags} %{rpmldflags} -Os -static" \
	CWFLAGS="-Wall"
mv -f mdadm initrd-mdadm
%{__make} clean
diet %{__cc} -DUCLIBC -DMDASSEMBLE_AUTO -DMDASSEMBLE %{rpmcflags} %{rpmcppflags} %{rpmldflags} -Os -static \
	-o initrd-mdassemble \
	mdassemble.c Assemble.c Manage.c config.c policy.c dlink.c util.c lib.c \
	super0.c super1.c super-ddf.c super-intel.c sha1.c crc32.c sg_io.c mdstat.c \
	platform-intel.c probe_roms.c sysfs.c super-mbr.c super-gpt.c mdopen.c maps.c xmalloc.c
%else
%{__make} mdadm.static \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} %{rpmcppflags}" \
	LDFLAGS="%{rpmldflags}"
mv -f mdadm.static initrd-mdadm
%{__make} clean
%{__cc} -DMDASSEMBLE_AUTO -DMDASSEMBLE %{rpmcflags} %{rpmcppflags} %{rpmldflags} -DHAVE_STDINT_H -static \
	-o initrd-mdassemble \
	mdassemble.c Assemble.c Manage.c config.c policy.c dlink.c util.c lib.c \
	super0.c super1.c super-ddf.c super-intel.c sha1.c crc32.c sg_io.c mdstat.c \
	platform-intel.c probe_roms.c sysfs.c super-mbr.c super-gpt.c mdopen.c maps.c xmalloc.c
%endif
%{__make} clean
%endif

%{__make} mdassemble \
	MDASSEMBLE_AUTO=1 \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} %{rpmcppflags}" \
	LDFLAGS="%{rpmldflags}" \
	SYSCONFDIR="%{_sysconfdir}"
mv mdassemble regular-mdassemble
%{__make} clean

%{__make} all mdadm mdadm.8 \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} %{rpmcppflags}" \
	LDFLAGS="%{rpmldflags}" \
	SYSCONFDIR="%{_sysconfdir}"

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man{5,8},/etc/{rc.d/init.d,sysconfig,cron.d}}

%if %{with initrd}
install -d $RPM_BUILD_ROOT%{_libdir}/initrd
install -p initrd-mdadm $RPM_BUILD_ROOT%{_libdir}/initrd/mdadm
install -p initrd-mdassemble $RPM_BUILD_ROOT%{_libdir}/initrd/mdassemble
ln -s mdadm $RPM_BUILD_ROOT%{_libdir}/initrd/mdctl
%endif

install -p regular-mdassemble $RPM_BUILD_ROOT%{_sbindir}/mdassemble
install -p mdadm $RPM_BUILD_ROOT%{_sbindir}

cp -p md*.5 $RPM_BUILD_ROOT%{_mandir}/man5
cp -p md*.8 $RPM_BUILD_ROOT%{_mandir}/man8

cp -p mdadm.conf-example $RPM_BUILD_ROOT%{_sysconfdir}/mdadm.conf

ln -s mdadm $RPM_BUILD_ROOT%{_sbindir}/mdctl

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

cp -p %{SOURCE3} $RPM_BUILD_ROOT/etc/cron.d/mdadm-checkarray
install -p %{SOURCE4} $RPM_BUILD_ROOT%{_sbindir}/mdadm-checkarray

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service mdadm restart "RAID monitoring"

%preun
if [ "$1" = "0" ]; then
	%service mdadm stop
	/sbin/chkconfig --del mdadm
fi

%files
%defattr(644,root,root,755)
%doc ANNOUNCE* ChangeLog TODO
%attr(755,root,root) %{_sbindir}/mdadm
%attr(755,root,root) %{_sbindir}/mdadm-checkarray
%attr(755,root,root) %{_sbindir}/mdassemble
%attr(755,root,root) %{_sbindir}/mdctl
%attr(640,root,root) %config(noreplace,missingok) %verify(not md5 mtime size) %{_sysconfdir}/mdadm.conf
%{_mandir}/man5/mdadm.conf.5*
%{_mandir}/man8/mdadm.8*
%{_mandir}/man8/mdassemble.8*
%{_mandir}/man8/mdmon.8*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%config(noreplace) %attr(640,root,root) /etc/cron.d/mdadm-checkarray

%if %{with initrd}
%files initrd
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/initrd/mdadm
%attr(755,root,root) %{_libdir}/initrd/mdassemble
%attr(755,root,root) %{_libdir}/initrd/mdctl
%endif
