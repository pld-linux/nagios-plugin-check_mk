# NOTE:
# - mk-livestatus is built from mk-livestatus package
%define		plugin	check_mk
Summary:	General purpose Nagios plugin for retrieving data
Name:		nagios-plugin-%{plugin}
Version:	1.2.6p9
Release:	0.2
License:	GPL v2
Group:		Networking
# Source0Download: https://mathias-kettner.de/check_mk_download_source.html
Source0:	https://mathias-kettner.de/download/check_mk-%{version}.tar.gz
# Source0-md5:	5c151625619ad39681f89d11dab819a6
URL:		http://mathias-kettner.com/check_mk.html
Requires:	mk-livestatus >= 1.2.6p9
Requires:	nagios-common
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir		/etc/nagios
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

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

DESTDIR=$RPM_BUILD_ROOT \
	enable_livestatus=no \
	nagios_config_file=%{_sysconfdir}/nagios.cfg \
	nagconfdir=%{_sysconfdir}/plugins \
	docdir=%{_docdir}/check-mk \
	checkmandir=%{_docdir}/check-mk/checkman \
	htdocsdir=%{_datadir}/nagios/htdocs \
	pnptemplates=%{_datadir}/nagios/htdocs/pnp/templates \
	nagpipe=/var/lib/nagios/rw/nagios.cmd \
	check_result_path=/var/spool/nagios/checkresults \
	nagiosurl=/nagios \
	cgiurl=/cgi-bin/nagios \
	check_icmp_path=%{_prefix}/lib/nagios/plugins/check_icmp \
	wwwuser=http \
	www_group=http \
	apache_config_dir=/etc/httpd/webapps.d \
	htpasswd_file=/etc/webapps/nagios/passwd \
	nagios_auth_name="Nagios" \
	nagios_binary=%{_sbindir}/nagios \
	nagios_startscript=/etc/rc.d/init.d/nagios \
./setup.sh --yes

%{__rm} $RPM_BUILD_ROOT/etc/check_mk/*.mk-%{version}

# avoid generating weird interpreter dependencies
%{__sed} -i -e '
	s#/usr/bin/bash#/bin/bash#
	s#/usr/bin/ksh93#/bin/ksh#g
	s#/usr/bin/ksh#/bin/ksh#g
	s#/usr/local/bin/bash#/bin/bash#g
' \
$RPM_BUILD_ROOT%{_datadir}/check_mk/agents/check_* \
$RPM_BUILD_ROOT%{_datadir}/check_mk/agents/plugins/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog
/etc/httpd/webapps.d/zzz_check_mk.conf
%dir /etc/check_mk
%dir /etc/check_mk/conf.d
/etc/check_mk/conf.d/README
/etc/check_mk/main.mk
/etc/check_mk/multisite.mk
%{_sysconfdir}/plugins/check_mk_templates.cfg
%attr(755,root,root) %{_bindir}/check_mk
%attr(755,root,root) %{_bindir}/cmk
%attr(755,root,root) %{_bindir}/mkp
%dir %{_datadir}/check_mk
%{_datadir}/check_mk/check_mk_templates.cfg
%{_datadir}/check_mk/agents
%{_datadir}/check_mk/checks
%{_datadir}/check_mk/inventory
%{_datadir}/check_mk/modules
%{_datadir}/check_mk/notifications
%{_datadir}/check_mk/web
%{_docdir}/check-mk
%{_datadir}/nagios/htdocs/pnp
%dir /var/lib/check_mk/packages
/var/lib/check_mk/packages/check_mk
