Summary:	Irqbalance daemon
Name:		irqbalance
Version:	1.1.0
Release:	4%{?dist}
License:	GPLv2
URL:		https://github.com/Irqbalance/irqbalance
Group:		System Environment/Services
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://github.com/Irqbalance/%{name}/archive/v%{version}.tar.gz
%define sha1 v1=bffafb547dd24a15645dbd1968c440218de6425d
BuildRequires:  systemd
Requires:  systemd
%description
Irqbalance is a daemon to help balance the cpu load generated by
interrupts across all of a systems cpus.
%prep
%setup -q
%build
./autogen.sh
./configure \
	--prefix=%{_prefix} \
	--disable-static \
	--with-systemd
	
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -D -m 0644 misc/irqbalance.env %{buildroot}/etc/sysconfig/irqbalance
sed -i 's#/path/to/irqbalance.env#/etc/sysconfig/irqbalance#' misc/irqbalance.service
sed -i 's/After=syslog.target//g' misc/irqbalance.service
install -D -m 0644 misc/irqbalance.service %{buildroot}%{_prefix}/lib/systemd/system/irqbalance.service

%post
%systemd_post %{name}.service
%preun
%systemd_preun %{name}.service
%postun
%systemd_postun_with_restart %{name}.service

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/*
%{_sbindir}/*
%exclude %{_libdir}/debug/*
%{_libdir}/systemd/*
%{_datadir}/*

%changelog
*  Thu Jul 27 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.1.0-4
-  Remove syslog.target from the service file
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.1.0-3
-	GA - Bump release of all rpms
*  Thu May 05 2016 Kumar Kaushik <kaushikk@vmware.com> 1.1.0-2
-  Adding package upgrade support.
*  Fri Jan 15 2016 Alexey Makhalov <amakhalov@vmware.com> 1.1.0-1
-  Initial version
