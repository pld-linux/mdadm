#
# Conditional build:
#  --without initrd -- build without initrd version
#
Summary:	Tool for creating and maintaining software RAID devices
Summary(pl):	Narzêdzie do tworzenia i obs³ugi programowych macierzy RAID
Name:		mdadm
Version:	1.3.0
Release:	2
License:	GPL
Group:		Base
Source0:	http://www.cse.unsw.edu.au/~neilb/source/mdadm/%{name}-%{version}.tgz
# Source0-md5:	61186df5073fae32569bd4bb12f9da36
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-BOOT.patch
%{!?_without_initrd:BuildRequires:	dietlibc-static}
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
%{!?_without_initrd:%{__make} CC="%{_target_cpu}-dietlibc-gcc" CFLAGS="%{rpmcflags}" LDFLAGS="%{rpmldflags} -static"}
%{!?_without_initrd:mv mdadm initrd-mdadm}
%{!?_without_initrd:%{__make} clean}

%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -D_GNU_SOURCE" \
	LDFLAGS="%{rpmldflags}" \
	SYSCONFDIR="%{_sysconfdir}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man{5,8},%{_sysconfdir}/{rc.d/init.d,sysconfig}}

%{!?_without_initrd:install initrd-mdadm $RPM_BUILD_ROOT%{_sbindir}}
install mdadm $RPM_BUILD_ROOT%{_sbindir}

install *.5 $RPM_BUILD_ROOT%{_mandir}/man5
install *.8 $RPM_BUILD_ROOT%{_mandir}/man8

install mdadm.conf-example $RPM_BUILD_ROOT%{_sysconfdir}/mdadm.conf

ln -s mdadm $RPM_BUILD_ROOT%{_sbindir}/mdctl
%{!?_without_initrd:ln -s initrd-mdadm $RPM_BUILD_ROOT%{_sbindir}/initrd-mdctl}

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

%if %{?_without_initrd:0}%{!?_without_initrd:1}
%files initrd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/initrd-mdadm
%endif
