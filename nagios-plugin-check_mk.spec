%define		plugin	check_mk
Summary:	General purpose Nagios plugin for retrieving data
Name:		nagios-plugin-%{plugin}
Version:	1.0.35
Release:	0.1
License:	GPL v2
Group:		Networking
Source0:	http://mathias-kettner.de/download/%{plugin}-%{version}.tar.gz
# Source0-md5:	022553ad48cd3da649c90f9352cdc80c
URL:		http://mathias-kettner.de/check_mk
Requires:	nagios-common
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir		/etc/nagios/plugins
%define		plugindir		%{_prefix}/lib/nagios/plugins

%define		_appdir			%{_datadir}/%{plugin}
%define		confdir			/etc/nagios/%{plugin}
%define		checksdir		%{_appdir}/checks
%define		modulesdir		%{_appdir}/modules
%define		agentsdir		%{_appdir}/agents
%define		mibsdir			%{_datadir}/snmp/mibs

%description
Check_mk adopts a new a approach for collecting data from operating
systems and network components. It obsoletes NRPE, check_by_ssh,
NSClient and check_snmp.

It has many benefits, the most important of which are:
- Significant reduction of CPU usage on the Nagios host.
- Automatic inventory of items to be checked on hosts.

The larger your Nagios installation is, the more important get these
points. In fact check_mk enables you to implement a monitoring
environment exceeding 20.000 checks/min on the first hand.

%prep
%setup -q -n %{plugin}-%{version}
for a in *.tar.gz; do
	d=${a%.tar.gz}
	install -d $d
	tar -xf $a -C $d
	rm -f $a
done
mv conf/main.mk{-%{version},}

%build
%{__cc} %{rpmcflags} -Wall agents/waitmax.c -o agents/waitmax

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_sbindir},%{pluginconfdir},%{plugindir},%{_mandir}/man1}
cp -a agents/check_mk_agent.linux $RPM_BUILD_ROOT%{_sbindir}/check_mk_agent
install -p modules/check_mk.py $RPM_BUILD_ROOT%{plugindir}/%{plugin}
cp -a doc/check_mk.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog INSTALL
%config(noreplace) %attr(640,root,nagios) %verify(not md5 mtime size) %{_sysconfdir}/%{plugin}.cfg
%attr(755,root,root) %{plugindir}/%{plugin}
%{_mandir}/man1/*.1*

%dir %attr(750,root,nagios) %{confdir}
%{confdir}/README
%config(noreplace) %attr(640,root,nagios) %verify(not md5 mtime size) %{confdir}/*.mk
