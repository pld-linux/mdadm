#
# Conditional build:
%bcond_without	initrd		# don't build initrd version
%bcond_without	uClibc		# link initrd version with static glibc instead of uClibc
#
%ifarch amd64
%undefine	with_uClibc
%endif
Summary:	Tool for creating and maintaining software RAID devices
Summary(pl):	Narzêdzie do tworzenia i obs³ugi programowych macierzy RAID
Name:		mdadm
Version:	1.9.0
Release:	2
License:	GPL
Group:		Base
Source0:	http://www.cse.unsw.edu.au/~neilb/source/mdadm/%{name}-%{version}.tgz
# Source0-md5:	4c5667761ba98890069127e54682e879
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-degraded.patch
%if %{with initrd}
%{!?with_uClibc:BuildRequires:	glibc-static}
%{?with_uClibc:BuildRequires:	uClibc-static}
%endif
BuildRequires:	groff
Obsoletes:	mdctl
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Requires(post):	/sbin/chkconfig

%define		_sbindir		/sbin

%description
This package includes tool you need to set up and maintain a software
RAID device under Linux. It's thought as an alternative to raidtools
package.

%description -l pl
Pakiet ten zawiera narzêdzie potrzebne do tworzenia i obs³ugi
programowych macierzy RAID. Program ten jest pomy¶lany jako
alternatywa dla pakietu raidtools.

%package initrd
Summary:	Tool for maintaining software RAID devices - initrd version
Summary(pl):	Narzêdzie do obs³ugi programowych macierzy RAID, wersja dla initrd
Group:		Base

%description initrd
Tool for maintaining software RAID devices - statically linked for
initrd.

%description initrd -l pl
Narzêdzie do zarz±dzania programowymi macierzami RAID - statycznie
skonsolidowane na potrzeby initrd.

%prep
%setup -q
%patch0 -p1

%build
%if %{with initrd}
%if %{with uClibc}
%{__make} mdadm.uclibc \
	UCLIBC_GCC="%{_target_cpu}-uclibc-gcc %{rpmcflags} %{rpmldflags} -static"
mv -f mdadm.uclibc initrd-mdadm
%{__make} clean
%{_target_cpu}-uclibc-gcc -DUCLIBC %{rpmcflags} %{rpmldflags} -static \
	 -o initrd-mdassemble mdassemble.c Assemble.c config.c dlink.c util.c
%else
%{__make} mdadm.static \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -D_GNU_SOURCE" \
	LDFLAGS="%{rpmldflags}"
mv -f mdadm.static initrd-mdadm
%{__make} clean
%{__cc} %{rpmcflags} %{rpmldflags} -static \
	 -o initrd-mdassemble mdassemble.c Assemble.c config.c dlink.c util.c
%endif
%{__make} clean
%endif

%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -D_GNU_SOURCE" \
	LDFLAGS="%{rpmldflags}" \
	SYSCONFDIR="%{_sysconfdir}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man{5,8},/etc/{rc.d/init.d,sysconfig}}

%if %{with initrd}
install initrd-mdadm $RPM_BUILD_ROOT%{_sbindir}
install initrd-mdassemble $RPM_BUILD_ROOT%{_sbindir}
ln -s initrd-mdadm $RPM_BUILD_ROOT%{_sbindir}/initrd-mdctl
%endif

install mdadm $RPM_BUILD_ROOT%{_sbindir}

install *.5 $RPM_BUILD_ROOT%{_mandir}/man5
install *.8 $RPM_BUILD_ROOT%{_mandir}/man8

install mdadm.conf-example $RPM_BUILD_ROOT%{_sysconfdir}/mdadm.conf

ln -s mdadm $RPM_BUILD_ROOT%{_sbindir}/mdctl

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
if [ -f /var/lock/subsys/mdadm ]; then
	/etc/rc.d/init.d/mdadm restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/mdadm start\" to start RAID monitoring."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/mdadm ]; then
		/etc/rc.d/init.d/mdadm stop 1>&2
	fi
	/sbin/chkconfig --del mdadm
fi

%files
%defattr(644,root,root,755)
%doc ANNOUNCE* TODO
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) %config(noreplace,missingok) %verify(not md5 size mtime) %{_sysconfdir}/mdadm.conf
%{_mandir}/man?/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/%{name}
%if %{with initrd}
%exclude %{_sbindir}/initrd-*

%files initrd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/initrd-*
%endif
