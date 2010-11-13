## Specfile based on Fedora made by developper
%define name	svxlink
%define main_version 101108

Name:		%{name}
Summary:	Repeater controller and EchoLink (simplex or repeater)
Version:	%{main_version}
Release:	%mkrel 1
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:	http://downloads.sourceforge.net/%{name}/sounds-%{version}.tar.gz
URL:		http://svxlink.sourceforge.net

Group:		Networking/Other
#files contained in sounds package are licensed under GPLv2
#the rest of files are licensed under GPLv2+
License:	GPLv2 and GPLv2+

BuildRequires:	%{_lib}sigc++1.2_5-devel
BuildRequires:	mng-devel
BuildRequires:	tcl-devel
BuildRequires:	qt3-devel 
BuildRequires:	gsm-devel
BuildRequires:	libxi-devel
BuildRequires:	popt-devel
BuildRequires:	speex-devel
BuildRequires:	doxygen
BuildRequires:	desktop-file-utils
BuildRequires:	%{_lib}gcrypt-devel

Requires (preun): chkconfig
Requires (preun): initscripts
Requires (post): chkconfig
Requires (postun): initscripts

%description
The SvxLink project is a multi purpose voice services system for
ham radio use. For example, EchoLink connections are supported.
Also, the SvxLink server can act as a repeater controller.
This is a development version. The released version doesn't build on newer 
Mandriva Distributions.

%package -n libasync
Summary: 	Svxlink async libs
Group: 		Development/Libraries
Version: 	0.17.0

%description -n libasync
The Async library is a programming framework that is used to write event driven
applications. It provides abstractions for file descriptor watches, timers,
network communications, serial port communications and config file reading.

Async is written in such a way that it can support other frameworks. Right now
there are two basic frameworks, a simple "select" based implementation and a Qt
implementation. The idea is that advanced libraries can be implemented in such
a way that they only depend on Async. That means that these libraries can be
used in both Qt and pure console applications and in any future frameworks
supported by Async (e.g. Gtk, wxWidgets etc).

Another big part of Async is the audio pipe framework. It is an audio handling
framework that is geared towards single channel (mono) audio applications. The
framework consists of a large number of audio handling classes such as
audio i/o, filtering, mixing, audio codecs etc.
This is a development version. The released version doesn't build on newer 
Mandriva Distributions.

%package -n libasync-devel
Summary: 	Svxlink async development files
Group: 		Development/Libraries
Version: 	0.17.0
Requires: 	libasync = 0.17.0
Obsoletes:	svxlink-server-devel < 0.11.1-2

%description -n libasync-devel
The async library development files

%package -n echolib
Summary: 	EchoLink communications library
Group: 		Development/Libraries
Version: 	0.13.1

%description -n echolib
EchoLib is a library that is used as a base for writing EchoLink applications.
It implements the directory server protocol as well as the station to station
protocol. EchoLink is used to link ham radio stations together over the
Internet.
This is a development version. The released version doesn't build on newer 
Mandriva Distributions.

%package -n echolib-devel
Summary: 	Development files for the EchoLink communications library
Group: 		Development/Libraries
Version: 	0.13.1
Requires: 	echolib = 0.13.1
Obsoletes:	svxlink-server-devel < 0.11.1-2

%description -n echolib-devel
Development files for the EchoLink communications library

%package -n qtel
Summary: 	The Qt EchoLink Client
Group: 		Applications/Communications
Version: 	0.11.2

%description -n qtel
This package contains Qtel, the Qt EchoLink client. It is an implementation of
the EchoLink software in Qt. This is only an EchoLink client, that is it can
not be connected to a transciever to create a link. If it is a pure link node
you want, install the svxlink-server package.
This is a development version. The released version doesn't build on newer 
Mandriva Distributions.

%package -n svxlink-server
Summary: 	SvxLink - A general purpose voice services system
Version: 	0.11.1
Group: 		Applications/Communications
Requires: 	udev
Requires (pre): shadow-utils

%description -n svxlink-server
The SvxLink server is a general purpose voice services system for ham radio
use. Each voice service is implemented as a plugin called a module.
Some examples of voice services are: Help system, Simplex repeater,
EchoLink communications and voice mail.

The core of the system handle the radio interface and is quite flexible
as well. It can act both as a simplex node and as a repeater controller. It is
also possible to link multiple receivers in via TCP/IP. The best receiver is
chosen using a software voter.
This is a development version. The released version doesn't build on newer 
Mandriva Distributions.

%prep
%setup -q -n %{name}-%{main_version}
%setup -q -D -T -a 1 -n %{name}-%{main_version}


%build
#LDFLAGS="${LDFLAGS:--Wl,-as-needed}" ; export LDFLAGS
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS
make %{?_smp_mflags}
doxygen doxygen.async
doxygen doxygen.echolib


%install
rm -rf %{buildroot}
make INSTALL_ROOT=$RPM_BUILD_ROOT NO_CHOWN=1 LIB_INSTALL_DIR=%{_libdir} \
	INC_INSTALL_DIR=%{_includedir}/svxlink BIN_INSTALL_DIR=%{_bindir} \
	SBIN_INSTALL_DIR=%{_sbindir} PLUGIN_INSTALL_DIR=%{_libdir}/svxlink install
mkdir -p %{buildroot}%{_datadir}/svxlink
cp -a sounds %{buildroot}%{_datadir}/svxlink/
mkdir -p %{buildroot}%{_localstatedir}/log
touch %{buildroot}%{_localstatedir}/log/svxlink
touch %{buildroot}%{_localstatedir}/log/svxlink.{1,2,3,4}
desktop-file-install \
	--dir=%{buildroot}%{_datadir}/applications qtel/qtel.desktop
mv %{buildroot}%{_sysconfdir}/logrotate.d/svxlink %{buildroot}%{_sysconfdir}/logrotate.d/svxlink-server
sed -i -e "s/subsys\/\$PROG/subsys\/svxlink/g" %{buildroot}%{_sysconfdir}/init.d/svxlink
sed -i -e "s/subsys\/\$PROG/subsys\/remotetrx/g" %{buildroot}%{_sysconfdir}/init.d/remotetrx
#remove static libs
rm -f %{buildroot}%{_libdir}/libasync*.a
rm -f %{buildroot}%{_libdir}/libecholib.a
rm -f %{buildroot}%{_libdir}/libtrx.a
#Next line added 11/13/2010
rm -f %{buildroot}%{_libdir}/liblocationinfo.a

%post -n libasync -p /sbin/ldconfig
%postun -n libasync -p /sbin/ldconfig

%post -n echolib -p /sbin/ldconfig
%postun -n echolib -p /sbin/ldconfig

%pre -n svxlink-server
getent group daemon >/dev/null || groupadd -r daemon
getent passwd svxlink >/dev/null || \
useradd -r -g daemon -d / -s /sbin/nologin \
-c "SvxLink Daemon " svxlink
exit 0

%post -n svxlink-server
/sbin/chkconfig --add svxlink

%preun -n svxlink-server
if [ $1 = 0 ]; then
  /sbin/service svxlink stop >/dev/null 2>&1 || :
  /sbin/chkconfig --del svxlink
fi

%postun -n svxlink-server 
if [ "$1" -ge "1" ] ; then
 /sbin/service svxlink condrestart >/dev/null 2>&1 || :
fi

%clean
rm -rf %{buildroot}


%files -n libasync
%defattr(-,root,root,-)
%doc async/ChangeLog
%defattr(755,root,root)
%{_libdir}/libasync*.so.*
%{_libdir}/libasync*.*.so

%files -n libasync-devel
%defattr(-,root,root,-)
%doc doc/async/html
%{_libdir}/libasyncaudio.so
%{_libdir}/libasynccore.so
%{_libdir}/libasynccpp.so
%{_libdir}/libasyncqt.so
%dir %{_includedir}/svxlink
%{_includedir}/svxlink/Async*
%{_includedir}/svxlink/SigCAudio*.h
%{_includedir}/svxlink/common.h

%files -n echolib
%defattr(-,root,root,-)
%doc echolib/ChangeLog
%defattr(755,root,root)
%{_libdir}/libecholib*.so.*
%{_libdir}/libecholib*.*.so

%files -n echolib-devel
%defattr(-,root,root,-)
%doc doc/echolib/html
%{_libdir}/libecholib.so
%dir %{_includedir}/svxlink
%{_includedir}/svxlink/EchoLink*

%files -n qtel
%defattr(-,root,root,-)
%doc qtel/ChangeLog
%{_bindir}/qtel
%{_datadir}/qtel
%{_datadir}/icons/link.xpm
%{_datadir}/applications/qtel.desktop

%files -n svxlink-server
%defattr(-,root,root,-)
%doc svxlink/ChangeLog
%{_bindir}/svxlink
%{_bindir}/remotetrx
%{_bindir}/siglevdetcal
%dir %{_libdir}/svxlink
%{_libdir}/svxlink/Module*.so
%dir %{_sysconfdir}/svxlink.d
%{_datadir}/svxlink
%defattr(644,root,root)
%config(noreplace) %{_sysconfdir}/svxlink.conf
%config(noreplace) %{_sysconfdir}/svxlink.d/*
%config(noreplace) %{_sysconfdir}/TclVoiceMail.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/svxlink-server
%config(noreplace) %{_sysconfdir}/remotetrx.conf
%config(noreplace) %{_sysconfdir}/sysconfig/svxlink
%config(noreplace) %{_sysconfdir}/sysconfig/remotetrx
%config(noreplace) %{_sysconfdir}/security/console.perms.d/90-svxlink.perms
%config(noreplace) %{_sysconfdir}/udev/rules.d/10-svxlink.rules
%{_mandir}/man*/*
%attr(755,svxlink,daemon) %dir %{_localstatedir}/spool/svxlink
%attr(755,svxlink,daemon) %dir %{_localstatedir}/spool/svxlink/voice_mail
%defattr(755,root,root)
%{_sysconfdir}/init.d/svxlink
%{_sysconfdir}/init.d/remotetrx
%{_sysconfdir}/svxlink/.procmailrc/procmailrc
%defattr(644,root,root)
%ghost /var/log/*
