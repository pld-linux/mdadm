#
# Conditional build:
%bcond_without	initrd		# don't build initrd version
%bcond_without	diet		# link initrd version with static glibc instead of dietlibc
#
Summary:	Tool for creating and maintaining software RAID devices
Summary(pl.UTF-8):	Narzędzie do tworzenia i obsługi programowych macierzy RAID
Name:		mdadm
Version:	2.6.3
Release:	1
License:	GPL
Group:		Base
Source0:	http://www.kernel.org/pub/linux/utils/raid/mdadm/%{name}-%{version}.tar.bz2
# Source0-md5:	2d3950028253a856f065763e5bd78b1c
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-degraded.patch
URL:		http://www.kernel.org/pub/linux/utils/raid/mdadm/
BuildRequires:	groff
BuildRequires:	rpmbuild(macros) >= 1.213
%if %{with initrd}
%{!?with_diet:BuildRequires:	glibc-static}
%if %{with diet}
BuildRequires:	dietlibc-static
%endif
Requires:	%{name}-initrd = %{epoch}:%{version}-%{release}
%endif
Requires(post,preun):	/sbin/chkconfig
Requires:	/sbin/chkconfig
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

%description initrd
Tool for maintaining software RAID devices - statically linked for
initrd.

%description initrd -l pl.UTF-8
Narzędzie do zarządzania programowymi macierzami RAID - statycznie
skonsolidowane na potrzeby initrd.

%prep
%setup -q
#%patch0 -p1

%build
%if %{with initrd}
%if %{with diet}
%{__make} mdadm \
	CC="diet %{__cc} %{rpmcflags} %{rpmldflags} -static" \
	CWFLAGS="-Wall"
mv -f mdadm initrd-mdadm
%{__make} clean
diet %{__cc}  -DUCLIBC -DMDASSEMBLE %{rpmcflags} %{rpmldflags} \
	-DHAVE_STDINT_H -o sha1.o -c sha1.c
diet %{__cc} -DUCLIBC -DMDASSEMBLE %{rpmcflags} %{rpmldflags} -static \
	-o initrd-mdassemble mdassemble.c Assemble.c Manage.c config.c dlink.c \
	util.c super0.c super1.c sha1.o
%else
%{__make} mdadm.static \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -D_GNU_SOURCE" \
	LDFLAGS="%{rpmldflags}"
mv -f mdadm.static initrd-mdadm
%{__make} clean
%{__cc} -DMDASSEMBLE %{rpmcflags} %{rpmldflags} -DHAVE_STDINT_H \
	-o sha1.o -c sha1.c
%{__cc} -DMDASSEMBLE %{rpmcflags} %{rpmldflags} -DHAVE_STDINT_H -static \
	-o initrd-mdassemble mdassemble.c Assemble.c Manage.c config.c dlink.c \
	util.c super0.c super1.c sha1.o
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
%doc ANNOUNCE* ChangeLog TODO
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) %config(noreplace,missingok) %verify(not md5 mtime size) %{_sysconfdir}/mdadm.conf
%{_mandir}/man?/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%if %{with initrd}
%exclude %{_sbindir}/initrd-*

%files initrd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/initrd-*
%endif
