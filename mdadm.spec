#
# Conditional build:
%bcond_without	initrd		# don't build initrd version
%bcond_without	dietlibc	# link initrd version with static glibc instead of dietlibc
#
Summary:	Tool for creating and maintaining software RAID devices
Summary(pl.UTF-8):	Narzędzie do tworzenia i obsługi programowych macierzy RAID
Name:		mdadm
Version:	2.6.9
Release:	1
License:	GPL v2+
Group:		Base
Source0:	http://www.kernel.org/pub/linux/utils/raid/mdadm/%{name}-%{version}.tar.bz2
# Source0-md5:	96c1bcac1699ba1aa70dfd04a08549c9
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.cron
Source4:	%{name}-checkarray
Source5:	%{name}-initramfs-hook
Source6:	%{name}-initramfs-local-top
Patch0:		%{name}-degraded.patch
URL:		http://www.kernel.org/pub/linux/utils/raid/mdadm/
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
Requires(post,preun):	/sbin/chkconfig
Requires:	/sbin/chkconfig
Requires:	rc-scripts >= 0.4.0.20
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
Conflicts:	geninitrd <= 10000.3

%description initrd
Tool for maintaining software RAID devices - statically linked for
initrd.

%description initrd -l pl.UTF-8
Narzędzie do zarządzania programowymi macierzami RAID - statycznie
skonsolidowane na potrzeby initrd.

%package initramfs
Summary:	Tool for maintaining software RAID devices - support scripts for initramfs-tools
Summary(pl.UTF-8):	Narzędzie do obsługi programowych macierzy RAID - skrypty dla initramfs-tools
Group:		Base
Requires:	%{name} = %{version}-%{release}
Requires:	initramfs-tools

%description initramfs
Tool for maintaining software RAID devices - support scripts for initramfs-tools.

%description initramfs -l pl.UTF-8
Narzędzie do obsługi programowych macierzy RAID - skrypty dla initramfs-tools.

%prep
%setup -q
# needs check if still needed - testcase is simple:
# just setup system with / on RAID1 and try to boot with the 1st or
# the 2nd disk disconnected
#%patch0 -p1

%build
%if %{with initrd}
%if %{with dietlibc}
%{__make} mdadm \
	CC="diet %{__cc} %{rpmcflags} %{rpmldflags} -Os -static" \
	CWFLAGS="-Wall"
mv -f mdadm initrd-mdadm
%{__make} clean
diet %{__cc} -DUCLIBC -DMDASSEMBLE_AUTO -DMDASSEMBLE %{rpmcflags} %{rpmldflags} -Os \
	-DHAVE_STDINT_H -o sha1.o -c sha1.c
diet %{__cc} -DUCLIBC -DMDASSEMBLE_AUTO -DMDASSEMBLE %{rpmcflags} %{rpmldflags} -Os -static \
	-o initrd-mdassemble mdassemble.c Assemble.c Manage.c config.c dlink.c \
	mdopen.c mdstat.c util.c sysfs.c super0.c super1.c sha1.o
%else
%{__make} mdadm.static \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"
mv -f mdadm.static initrd-mdadm
%{__make} clean
%{__cc} -DMDASSEMBLE_AUTO -DMDASSEMBLE %{rpmcflags} %{rpmldflags} -DHAVE_STDINT_H \
	-o sha1.o -c sha1.c
%{__cc} -DMDASSEMBLE_AUTO -DMDASSEMBLE %{rpmcflags} %{rpmldflags} -DHAVE_STDINT_H -static \
	-o initrd-mdassemble mdassemble.c Assemble.c Manage.c config.c dlink.c \
	mdopen.c mdstat.c util.c sysfs.c super0.c super1.c sha1.o
%endif
%{__make} clean
%endif

%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}" \
	SYSCONFDIR="%{_sysconfdir}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man{5,8},/etc/{rc.d/init.d,sysconfig,cron.d}} \
	$RPM_BUILD_ROOT%{_datadir}/initramfs-tools/{hooks,scripts/local-top}

%if %{with initrd}
install -d $RPM_BUILD_ROOT%{_libdir}/initrd
install initrd-mdadm $RPM_BUILD_ROOT%{_libdir}/initrd/mdadm
install initrd-mdassemble $RPM_BUILD_ROOT%{_libdir}/initrd/mdassemble
ln -s mdadm $RPM_BUILD_ROOT%{_libdir}/initrd/mdctl
%endif

install mdadm $RPM_BUILD_ROOT%{_sbindir}

install *.5 $RPM_BUILD_ROOT%{_mandir}/man5
install *.8 $RPM_BUILD_ROOT%{_mandir}/man8

install mdadm.conf-example $RPM_BUILD_ROOT%{_sysconfdir}/mdadm.conf

ln -s mdadm $RPM_BUILD_ROOT%{_sbindir}/mdctl

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

install %{SOURCE3} $RPM_BUILD_ROOT/etc/cron.d/mdadm-checkarray
install %{SOURCE4} $RPM_BUILD_ROOT%{_sbindir}/mdadm-checkarray

install %{SOURCE5} $RPM_BUILD_ROOT%{_datadir}/initramfs-tools/hooks/mdadm
install %{SOURCE6} $RPM_BUILD_ROOT%{_datadir}/initramfs-tools/scripts/local-top/mdadm

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
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) %config(noreplace,missingok) %verify(not md5 mtime size) %{_sysconfdir}/mdadm.conf
%{_mandir}/man?/*
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

%files initramfs
%defattr(644,root,root,755)
%attr(755,root,root) %{_datadir}/initramfs-tools/hooks/mdadm
%attr(755,root,root) %{_datadir}/initramfs-tools/scripts/local-top/mdadm
