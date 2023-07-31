#
# Conditional build:
%bcond_with	initrd		# don't build initrd version
%bcond_with	dietlibc	# link initrd version with static glibc instead of dietlibc
%bcond_without	tests		# don't perform "make test"

Summary:	Tool for creating and maintaining software RAID devices
Summary(pl.UTF-8):	Narzędzie do tworzenia i obsługi programowych macierzy RAID
Name:		mdadm
Version:	4.2
Release:	1
License:	GPL v2+
Group:		Base
Source0:	https://www.kernel.org/pub/linux/utils/raid/mdadm/%{name}-%{version}.tar.xz
# Source0-md5:	a304eb0a978ca81045620d06547050a6
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.cron
Source4:	%{name}-checkarray
Source5:	cronjob-%{name}.timer
Source6:	cronjob-%{name}.service
URL:		https://www.kernel.org/pub/linux/utils/raid/mdadm/
# Upstream patches
Patch000:	0001-Unify-error-message.patch
Patch001:	0002-%{name}-Fix-double-free.patch
Patch002:	0003-Grow_reshape-Add-r0-grow-size-error-message-and-upda.patch
Patch003:	0004-udev-adapt-rules-to-systemd-v247.patch
Patch004:	0005-Replace-error-prone-signal-with-sigaction.patch
Patch005:	0006-%{name}-Respect-config-file-location-in-man.patch
Patch006:	0007-%{name}-Update-ReadMe.patch
Patch007:	0008-%{name}-Update-config-man-regarding-default-files-and-.patch
Patch008:	0009-%{name}-Update-config-manual.patch
Patch009:	0010-Create-Build-use-default_layout.patch
Patch010:	0011-%{name}-add-map_num_s.patch
Patch011:	0012-%{name}-systemd-remove-KillMode-none-from-service-file.patch
Patch012:	0013-mdmon-Stop-parsing-duplicate-options.patch
Patch013:	0014-Grow-block-n-on-external-volumes.patch
Patch014:	0015-Incremental-Fix-possible-memory-and-resource-leaks.patch
Patch015:	0016-Mdmonitor-Fix-segfault.patch
Patch016:	0017-Mdmonitor-Improve-logging-method.patch
Patch017:	0018-Fix-possible-NULL-ptr-dereferences-and-memory-leaks.patch
Patch018:	0019-imsm-Remove-possibility-for-get_imsm_dev-to-return-N.patch
Patch019:	0020-Revert-%{name}-fix-coredump-of-mdadm-monitor-r.patch
Patch020:	0021-util-replace-ioctl-use-with-function.patch
Patch021:	0022-%{name}-super1-restore-commit-45a87c2f31335-to-fix-clu.patch
Patch022:	0023-imsm-introduce-get_disk_slot_in_dev.patch
Patch023:	0024-imsm-use-same-slot-across-container.patch
Patch024:	0025-imsm-block-changing-slots-during-creation.patch
Patch025:	0026-%{name}-block-update-ppl-for-non-raid456-levels.patch
Patch026:	0027-%{name}-Fix-array-size-mismatch-after-grow.patch
Patch027:	0028-%{name}-Remove-dead-code-in-imsm_fix_size_mismatch.patch
Patch028:	0029-Monitor-use-devname-as-char-array-instead-of-pointer.patch
Patch029:	0030-Monitor-use-snprintf-to-fill-device-name.patch
Patch030:	0031-Makefile-Don-t-build-static-build-with-everything-an.patch
Patch031:	0032-DDF-Cleanup-validate_geometry_ddf_container.patch
Patch032:	0033-DDF-Fix-NULL-pointer-dereference-in-validate_geometr.patch
Patch033:	0034-%{name}-Grow-Fix-use-after-close-bug-by-closing-after-.patch
Patch034:	0035-monitor-Avoid-segfault-when-calling-NULL-get_bad_blo.patch
Patch035:	0036-%{name}-Fix-mdadm-r-remove-option-regression.patch
Patch036:	0037-%{name}-Fix-optional-write-behind-parameter.patch
Patch037:	0038-tests-00raid0-add-a-test-that-validates-raid0-with-l.patch
Patch038:	0039-tests-fix-raid0-tests-for-0.90-metadata.patch
Patch039:	0040-tests-04update-metadata-avoid-passing-chunk-size-to-.patch
Patch040:	0041-tests-02lineargrow-clear-the-superblock-at-every-ite.patch
Patch041:	0042-%{name}-test-Add-a-mode-to-repeat-specified-tests.patch
Patch042:	0043-%{name}-test-Mark-and-ignore-broken-test-failures.patch
Patch043:	0044-tests-Add-broken-files-for-all-broken-tests.patch
Patch044:	0045-%{name}-Replace-obsolete-usleep-with-nanosleep.patch
Patch045:	0046-tests-00readonly-Run-udevadm-settle-before-setting-r.patch
Patch046:	0047-tests-add-test-for-names.patch
Patch047:	0048-%{name}-remove-symlink-option.patch
Patch048:	0049-%{name}-move-data_offset-to-struct-shape.patch
Patch049:	0050-%{name}-Don-t-open-md-device-for-CREATE-and-ASSEMBLE.patch
Patch050:	0051-Grow-Split-Grow_reshape-into-helper-function.patch
Patch051:	0052-Assemble-check-if-device-is-container-before-schedul.patch
Patch052:	0053-super1-report-truncated-device.patch
Patch053:	0054-%{name}-Correct-typos-punctuation-and-grammar-in-man.patch
Patch054:	0055-Manage-Block-unsafe-member-failing.patch
Patch055:	0056-Monitor-Fix-statelist-memory-leaks.patch
Patch056:	0057-%{name}-added-support-for-Intel-Alderlake-RST-on-VMD-p.patch
Patch057:	0058-%{name}-Add-Documentation-entries-to-systemd-services.patch
Patch058:	0059-ReadMe-fix-command-line-help.patch
Patch059:	0060-%{name}-replace-container-level-checking-with-inline.patch
Patch060:	0061-Mdmonitor-Omit-non-md-devices.patch
Patch061:	0062-Mdmonitor-Split-alert-into-separate-functions.patch
Patch062:	0063-Monitor-block-if-monitor-modes-are-combined.patch
Patch063:	0064-Update-%{name}-Monitor-manual.patch
Patch064:	0065-Grow-fix-possible-memory-leak.patch
Patch065:	0066-%{name}-create-ident_init.patch
Patch066:	0067-%{name}-Add-option-validation-for-update-subarray.patch
Patch067:	0068-Fix-update-subarray-on-active-volume.patch
Patch068:	0069-Add-code-specific-update-options-to-enum.patch
Patch069:	0070-super-ddf-Remove-update_super_ddf.patch
Patch070:	0071-super0-refactor-the-code-for-enum.patch
Patch071:	0072-super1-refactor-the-code-for-enum.patch
Patch072:	0073-super-intel-refactor-the-code-for-enum.patch
Patch073:	0074-Change-update-to-enum-in-update_super-and-update_sub.patch
Patch074:	0075-Manage-Incremental-code-refactor-string-to-enum.patch
Patch075:	0076-Change-char-to-enum-in-context-update-refactor-code.patch
Patch076:	0077-mdmon-fix-segfault.patch
Patch077:	0078-util-remove-obsolete-code-from-get_md_name.patch
Patch078:	0079-%{name}-udev-Don-t-handle-change-event-on-raw-devices.patch
Patch079:	0080-Manage-do-not-check-array-state-when-drive-is-remove.patch
Patch080:	0081-incremental-manage-do-not-verify-if-remove-is-safe.patch
Patch081:	0082-super-intel-make-freesize-not-required-for-chunk-siz.patch
Patch082:	0083-manage-move-comment-with-function-description.patch
Patch083:	0084-Revert-%{name}-systemd-remove-KillMode-none-from-servi.patch
Patch084:	0085-Grow-fix-can-t-change-bitmap-type-from-none-to-clust.patch
Patch085:	0086-Fix-NULL-dereference-in-super_by_fd.patch
Patch086:	0087-Mdmonitor-Make-alert_info-global.patch
Patch087:	0088-Mdmonitor-Pass-events-to-alert-using-enums-instead-o.patch
Patch088:	0089-Mdmonitor-Add-helper-functions.patch
Patch089:	0090-Add-helpers-to-determine-whether-directories-or-file.patch
Patch090:	0091-Mdmonitor-Refactor-write_autorebuild_pid.patch
Patch091:	0092-Mdmonitor-Refactor-check_one_sharer-for-better-error.patch
Patch092:	0093-util.c-reorder-code-lines-in-parse_layout_faulty.patch
Patch093:	0094-util.c-fix-memleak-in-parse_layout_faulty.patch
Patch094:	0095-Detail.c-fix-memleak-in-Detail.patch
Patch095:	0096-isuper-intel.c-fix-double-free-in-load_imsm_mpb.patch
Patch096:	0097-super-intel.c-fix-memleak-in-find_disk_attached_hba.patch
Patch097:	0098-super-ddf.c-fix-memleak-in-get_vd_num_of_subarray.patch
Patch098:	0099-Create-goto-abort_locked-instead-of-return-1-in-erro.patch
Patch099:	0100-Create-remove-safe_mode_delay-local-variable.patch
Patch100:	0101-Create-Factor-out-add_disks-helpers.patch
Patch101:	0102-%{name}-Introduce-pr_info.patch
Patch102:	0103-%{name}-Add-write-zeros-option-for-Create.patch
Patch103:	0104-tests-00raid5-zero-Introduce-test-to-exercise-write-.patch
Patch104:	0105-manpage-Add-write-zeroes-option-to-manpage.patch
Patch105:	0106-Define-alignof-using-_Alignof-when-using-C11-or-newe.patch
Patch106:	0107-Use-existence-of-etc-initrd-release-to-detect-initrd.patch
Patch107:	0108-mdmon-don-t-test-both-all-and-container_name.patch
Patch108:	0109-mdmon-change-systemd-unit-file-to-use-foreground.patch
Patch109:	0110-mdmon-Remove-need-for-KillMode-none.patch
Patch110:	0111-mdmon-Improve-switchroot-interactions.patch
Patch111:	0112-mdopen-always-try-create_named_array.patch
Patch112:	0113-Improvements-for-IMSM_NO_PLATFORM-testing.patch
Patch113:	0114-Revert-Revert-%{name}-systemd-remove-KillMode-none-fro.patch
Patch114:	0115-Create-Fix-checking-for-container-in-update_metadata.patch
Patch115:	0116-Fix-null-pointer-for-incremental-in-%{name}.patch
Patch116:	0117-super1-fix-truncation-check-for-journal-device.patch
Patch117:	0118-Fix-some-cases-eyesore-formatting.patch
Patch118:	0119-Bump-minimum-kernel-version-to-2.6.32.patch
Patch119:	0120-Remove-the-config-files-in-mdcheck_start-continue-se.patch
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
Conflicts:	geninitrd < 12787

%description initrd
Tool for maintaining software RAID devices - statically linked for
initrd.

%description initrd -l pl.UTF-8
Narzędzie do zarządzania programowymi macierzami RAID - statycznie
skonsolidowane na potrzeby initrd.

%prep
%setup -q
%patch000 -p1
%patch001 -p1
%patch002 -p1
%patch003 -p1
%patch004 -p1
%patch005 -p1
%patch006 -p1
%patch007 -p1
%patch008 -p1
%patch009 -p1
%patch010 -p1
%patch011 -p1
%patch012 -p1
%patch013 -p1
%patch014 -p1
%patch015 -p1
%patch016 -p1
%patch017 -p1
%patch018 -p1
%patch019 -p1
%patch020 -p1
%patch021 -p1
%patch022 -p1
%patch023 -p1
%patch024 -p1
%patch025 -p1
%patch026 -p1
%patch027 -p1
%patch028 -p1
%patch029 -p1
%patch030 -p1
%patch031 -p1
%patch032 -p1
%patch033 -p1
%patch034 -p1
%patch035 -p1
%patch036 -p1
%patch037 -p1
%patch038 -p1
%patch039 -p1
%patch040 -p1
%patch041 -p1
%patch042 -p1
%patch043 -p1
%patch044 -p1
%patch045 -p1
%patch046 -p1
%patch047 -p1
%patch048 -p1
%patch049 -p1
%patch050 -p1
%patch051 -p1
%patch052 -p1
%patch053 -p1
%patch054 -p1
%patch055 -p1
%patch056 -p1
%patch057 -p1
%patch058 -p1
%patch059 -p1
%patch060 -p1
%patch061 -p1
%patch062 -p1
%patch063 -p1
%patch064 -p1
%patch065 -p1
%patch066 -p1
%patch067 -p1
%patch068 -p1
%patch069 -p1
%patch070 -p1
%patch071 -p1
%patch072 -p1
%patch073 -p1
%patch074 -p1
%patch075 -p1
%patch076 -p1
%patch077 -p1
%patch078 -p1
%patch079 -p1
%patch080 -p1
%patch081 -p1
%patch082 -p1
%patch083 -p1
%patch084 -p1
%patch085 -p1
%patch086 -p1
%patch087 -p1
%patch088 -p1
%patch089 -p1
%patch090 -p1
%patch091 -p1
%patch092 -p1
%patch093 -p1
%patch094 -p1
%patch095 -p1
%patch096 -p1
%patch097 -p1
%patch098 -p1
%patch099 -p1
%patch100 -p1
%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1
%patch105 -p1
%patch106 -p1
%patch107 -p1
%patch108 -p1
%patch109 -p1
%patch110 -p1
%patch111 -p1
%patch112 -p1
%patch113 -p1
%patch114 -p1
%patch115 -p1
%patch116 -p1
%patch117 -p1
%patch118 -p1
%patch119 -p1

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
