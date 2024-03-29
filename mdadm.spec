#
# Conditional build:
%bcond_with	initrd		# initrd version
%bcond_with	dietlibc	# link initrd version with static glibc instead of dietlibc
%bcond_without	tests		# unit tests

Summary:	Tool for creating and maintaining software RAID devices
Summary(pl.UTF-8):	Narzędzie do tworzenia i obsługi programowych macierzy RAID
Name:		mdadm
Version:	4.3
Release:	1
License:	GPL v2+
Group:		Base
Source0:	https://www.kernel.org/pub/linux/utils/raid/mdadm/%{name}-%{version}.tar.xz
# Source0-md5:	a42def84e31734a529111394f2289e0e
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.cron
Source4:	%{name}-checkarray
Source5:	cronjob-%{name}.timer
Source6:	cronjob-%{name}.service
URL:		https://www.kernel.org/pub/linux/utils/raid/mdadm/
BuildRequires:	corosync-devel
BuildRequires:	dlm-devel
BuildRequires:	groff
BuildRequires:	rpmbuild(macros) >= 1.671
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%if %{with initrd}
	%if %{with dietlibc}
BuildRequires:	dietlibc-static
	%else
BuildRequires:	glibc-static
	%endif
%endif
Requires(post,preun):	/sbin/chkconfig
Requires:	/sbin/chkconfig
Requires:	rc-scripts >= 0.4.2.4-2
Requires:	systemd-units >= 38
Suggests:	cronjobs
%{!?with_initrd:Obsoletes:	mdadm-initrd < %{version}-%{release}}
Obsoletes:	mdctl < 0.5
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
Conflicts:	geninitrd < 12787

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
%{__mv} mdadm initrd-mdadm
%else
%{__make} mdadm.static \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} %{rpmcppflags}" \
	LDFLAGS="%{rpmldflags}"
%{__mv} mdadm.static initrd-mdadm
%endif
%{__make} clean
%endif

%{__make} all mdadm mdadm.8 \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} %{rpmcppflags}" \
	LDFLAGS="%{rpmldflags}" \
	SYSCONFDIR="%{_sysconfdir}"

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man{5,8}} \
	$RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig,cron.d},%{systemdunitdir}}

%{__make} install install-udev install-systemd \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with initrd}
install -d $RPM_BUILD_ROOT%{_libdir}/initrd
install -p initrd-mdadm $RPM_BUILD_ROOT%{_libdir}/initrd/mdadm
ln -s mdadm $RPM_BUILD_ROOT%{_libdir}/initrd/mdctl
%endif

cp -p mdadm.conf-example $RPM_BUILD_ROOT%{_sysconfdir}/mdadm.conf

ln -s mdadm $RPM_BUILD_ROOT%{_sbindir}/mdctl

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

cp -p %{SOURCE3} $RPM_BUILD_ROOT/etc/cron.d/mdadm-checkarray
install -p %{SOURCE4} $RPM_BUILD_ROOT%{_sbindir}/mdadm-checkarray
install -p %{SOURCE5} $RPM_BUILD_ROOT%{systemdunitdir}/cronjob-mdadm.timer
install -p %{SOURCE6} $RPM_BUILD_ROOT%{systemdunitdir}/cronjob-mdadm.service

ln -s /dev/null $RPM_BUILD_ROOT%{systemdunitdir}/mdadm.service

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service mdadm restart "RAID monitoring"
%systemd_post mdmonitor.service cronjob-mdadm.timer

%preun
if [ "$1" = "0" ]; then
	%service mdadm stop
	/sbin/chkconfig --del mdadm
fi
%systemd_preun mdmonitor.service cronjob-mdadm.timer

%postun
/sbin/ldconfig
%systemd_reload

%triggerpostun -- %{name} < 4.0-3
%systemd_trigger cronjob-mdadm.timer

%files
%defattr(644,root,root,755)
%doc ANNOUNCE* ChangeLog TODO
%attr(755,root,root) %{_sbindir}/mdadm
%attr(755,root,root) %{_sbindir}/mdadm-checkarray
%attr(755,root,root) %{_sbindir}/mdctl
%attr(755,root,root) %{_sbindir}/mdmon
%{systemdunitdir}-shutdown/mdadm.shutdown
%{systemdunitdir}/mdadm-grow-continue@.service
%{systemdunitdir}/mdadm-last-resort@.service
%{systemdunitdir}/mdadm-last-resort@.timer
%{systemdunitdir}/mdadm.service
%{systemdunitdir}/mdmon@.service
%{systemdunitdir}/mdmonitor.service
%{systemdunitdir}/cronjob-mdadm.service
%{systemdunitdir}/cronjob-mdadm.timer
%{systemdunitdir}/mdcheck_continue.service
%{systemdunitdir}/mdcheck_continue.timer
%{systemdunitdir}/mdcheck_start.service
%{systemdunitdir}/mdcheck_start.timer
%{systemdunitdir}/mdmonitor-oneshot.service
%{systemdunitdir}/mdmonitor-oneshot.timer
/lib/udev/rules.d/01-md-raid-creating.rules
/lib/udev/rules.d/63-md-raid-arrays.rules
/lib/udev/rules.d/64-md-raid-assembly.rules
/lib/udev/rules.d/69-md-clustered-confirm-device.rules
%attr(640,root,root) %config(noreplace,missingok) %verify(not md5 mtime size) %{_sysconfdir}/mdadm.conf
%{_mandir}/man4/md.4*
%{_mandir}/man5/mdadm.conf.5*
%{_mandir}/man8/mdadm.8*
%{_mandir}/man8/mdmon.8*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%config(noreplace) %attr(640,root,root) /etc/cron.d/mdadm-checkarray

%if %{with initrd}
%files initrd
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/initrd/mdadm
%attr(755,root,root) %{_libdir}/initrd/mdctl
%endif
