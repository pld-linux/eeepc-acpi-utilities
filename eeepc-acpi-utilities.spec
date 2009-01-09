Summary:	ACPI scripts for EeePC netbook computers
Summary(pl.UTF-8):	Skrypty ACPI dla notebooków EeePC
Name:		eeepc-acpi-utilities
Version:	1.0.9
Release:	0.2
License:	GPL
Group:		X11/Applications
Source0:	http://dl.sourceforge.net/eeepc-acpi-util/%{name}_%{version}.tar.gz
# Source0-md5:	cc32bd733b980d76beaac051f6b2cf4e
Source1:	%{name}.init
URL:		http://eeepc-acpi-util.sourceforge.net/
Requires:	acpid
Requires:	coreutils
Requires:	dmidecode
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ACPI scripts for EeePC netbook computers.

Keys are configured as follows by default:

Top row (4 keys)

- Touchpad On / Off
- Screen resolution cycle (1024x600, 800x600, 640x480)
- Bluetooth On / Off
- Webcam On / Off

Alternately any two of the following can be enabled instead of
Bluetooth / Webcam:

- Rotate Screen (Cycles Left, Inverted, Right, then Normal)
- CPU Mode cycle (Performance, On Demand, Power Saver)
- Firefox (Customizable)
- Pidgin (Customizable)

The FN-[F1-F12] keys are set to the following by default:

- F1 - Sleep (not managed by my ACPI Scripts)
- F2 - WIFI (It will autodetect your adapter, or alternately you can
  select ndiswrapper mode)
- F5-F6 Brightness (not managed by my ACPI Scripts)
- F7 - LCD power Toggle On / Off
- F8 - VGA Output toggle
- F9 - Gnome System Monitor
- F10 - Volume Mute
- F11 - Volume -
- F12 - Volume +

Features: Zero resident memory footprint unless keys are pressed, fast
response, parameter save / restore, fan management, CPU frequency
management, and more.

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{acpi,cron.d,sysconfig,rc.d/init.d,xdg}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/acpi/{eeepc,events}
install -d $RPM_BUILD_ROOT%{_datadir}/{,applications,pixmaps}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart
install -d $RPM_BUILD_ROOT/var/eeepc

install acpi/eeepc/*.sh $RPM_BUILD_ROOT%{_sysconfdir}/acpi/eeepc/
install acpi/events/eeepc-hotkeys $RPM_BUILD_ROOT%{_sysconfdir}/acpi/events/
install cron.d/eeepc-fan $RPM_BUILD_ROOT/etc/cron.d/
install default/eeepc-acpi $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/eeepc-restore
install usr/share/applications/eeepc.desktop $RPM_BUILD_ROOT%{_desktopdir}/
install usr/share/pixmaps/eee.png $RPM_BUILD_ROOT%{_pixmapsdir}/
install xdg/autostart/eeepc-acpi-util.desktop $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add eeepc-restore
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del eeepc-restore
fi

%files
%defattr(644,root,root,755)
%dir  %{_sysconfdir}/acpi/eeepc
%attr(755,root,root) %{_sysconfdir}/acpi/eeepc/*.sh
%{_sysconfdir}/acpi/events/eeepc-hotkeys
/etc/cron.d/eeepc-fan
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/eeepc-acpi
%attr(754,root,root) /etc/rc.d/init.d/eeepc-restore
%{_sysconfdir}/xdg/autostart/eeepc-acpi-util.desktop
%{_desktopdir}/eeepc.desktop
%{_pixmapsdir}/eee.png
%dir /var/eeepc
