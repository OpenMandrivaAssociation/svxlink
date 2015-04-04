## Specfile based on Fedora made by developper
%define name	svxlink
%define main_version 11.11.1

Name:		%{name}
Summary:	Repeater controller and EchoLink (simplex or repeater)
Version:	%{main_version}
Release:	3
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:	http://downloads.sourceforge.net/%{name}/sounds-en_US-heather-11.11.tar.bz2
URL:		http://svxlink.sourceforge.net

Group:		Communications
#files contained in sounds package are licensed under GPLv2
#the rest of files are licensed under GPLv2+
License:	GPLv2 and GPLv2+
Patch0:		svxlink-11.11.1-gcc-47.patch

BuildRequires:	glibc-devel
BuildRequires:	alsa-oss-devel
BuildRequires:	libsigc++1.2-devel
BuildRequires:	pkgconfig(libmng) >= 2.0.2
BuildRequires:	tcl-devel
BuildRequires:	qt4-devel 
BuildRequires:	gsm-devel
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(popt)
BuildRequires:	pkgconfig(speex)
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

#---------------------------------------------------------------
%define asyncmajor	0	
%define libasync %mklibname async %{asyncmajor}

%package -n %{libasync}
Summary: 	Svxlink async libs
Group: 		System/Libraries
Version: 	0.18

%description -n %{libasync}
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

%files -n %{libasync}
%doc async/ChangeLog
%defattr(755,root,root)
%{_libdir}/libasync*.so.*
%{_libdir}/libasync*.*.so
#---------------------------------------------------------------
%define devasync	%mklibname async -d

%package -n %{devasync}
Summary: 	Svxlink async development files
Group: 		System/Libraries
Version: 	0.18
Requires: 	%{libasync} = %{EVRD}
Obsoletes:	svxlink-server-devel < 0.11.1-2

%description -n %{devasync}
The async library development files

%files -n %{devasync}
%doc doc/async/html
%{_libdir}/libasyncaudio.so
%{_libdir}/libasynccore.so
%{_libdir}/libasynccpp.so
%{_libdir}/libasyncqt.so
%dir %{_includedir}/svxlink
%{_includedir}/svxlink/Async*
%{_includedir}/svxlink/SigCAudio*.h
%{_includedir}/svxlink/common.h

#---------------------------------------------------------------
%define echomajor	0
%define echolib		%mklibname echolib %{echomajor}

%package -n %{echolib}
Summary: 	EchoLink communications library
Group: 		System/Libraries
Version: 	0.14

%description -n %{echolib}
EchoLib is a library that is used as a base for writing EchoLink applications.
It implements the directory server protocol as well as the station to station
protocol. EchoLink is used to link ham radio stations together over the
Internet.
This is a development version. The released version doesn't build on newer 
Mandriva Distributions.

%files -n %{echolib}
%doc echolib/ChangeLog
%defattr(755,root,root)
%{_libdir}/libecholib*.so.*
%{_libdir}/libecholib*.*.so

#---------------------------------------------------------------
%define devecholib	%mklibname echolib -d

%package -n %{devecholib}
Summary: 	Development files for the EchoLink communications library
Group: 		System/Libraries
Version: 	0.14
Requires: 	%{echolib} = %{EVRD}
Obsoletes:	svxlink-server-devel < 0.11.1-2

%description -n %{devecholib}
Development files for the EchoLink communications library


%files -n %{devecholib}
%doc doc/echolib/html
%{_libdir}/libecholib.so
%dir %{_includedir}/svxlink
%{_includedir}/svxlink/EchoLink*
#---------------------------------------------------------------

%package -n qtel
Summary: 	The Qt EchoLink Client
Group: 		Communications
Version: 	0.11.2

%description -n qtel
This package contains Qtel, the Qt EchoLink client. It is an implementation of
the EchoLink software in Qt. This is only an EchoLink client, that is it can
not be connected to a transciever to create a link. If it is a pure link node
you want, install the svxlink-server package.
This is a development version. The released version doesn't build on newer 
Mandriva Distributions.

%files -n qtel
%doc COPYRIGHT qtel/ChangeLog
%{_bindir}/qtel
%{_datadir}/qtel
%{_datadir}/icons/link.xpm
%{_datadir}/applications/qtel.desktop

#---------------------------------------------------------------
%package -n svxlink-server
Summary: 	SvxLink - A general purpose voice services system
Version: 	0.11.1
Group: 		Networking/Other
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

%files -n svxlink-server
%doc COPYRIGHT svxlink/ChangeLog
%{_bindir}/svxlink
%{_bindir}/remotetrx
%{_bindir}/siglevdetcal
%dir %{_libdir}/svxlink
%{_libdir}/svxlink/Module*.so
%dir %{_sysconfdir}/%{name}/svxlink.d
%{_datadir}/svxlink
%defattr(644,root,root)
%config(noreplace) %{_sysconfdir}/%{name}/svxlink.conf
%config(noreplace) %{_sysconfdir}/%{name}/.procmailrc
%config(noreplace) %{_sysconfdir}/%{name}/svxlink.d/*
%config(noreplace) %{_sysconfdir}/%{name}/TclVoiceMail.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/svxlink-server
%config(noreplace) %{_sysconfdir}/logrotate.d/remotetrx
%config(noreplace) %{_sysconfdir}/%{name}/remotetrx.conf
%config(noreplace) %{_sysconfdir}/sysconfig/svxlink
%config(noreplace) %{_sysconfdir}/sysconfig/remotetrx
%config(noreplace) %{_sysconfdir}/security/console.perms.d/90-svxlink.perms
/lib/udev/rules.d/10-svxlink.rules
%{_mandir}/man*/*
%attr(755,svxlink,daemon) %dir %{_localstatedir}/spool/svxlink
%attr(755,svxlink,daemon) %dir %{_localstatedir}/spool/svxlink/voice_mail
%defattr(755,root,root)
%{_sysconfdir}/init.d/svxlink
%{_sysconfdir}/init.d/remotetrx
%defattr(644,root,root)
%ghost /var/log/*
#---------------------------------------------------------------

%prep
%setup -q -n %{name}-%{main_version}
%setup -q -D -T -a 1 -n %{name}-%{main_version}
%patch0 -p0

%build
sed -i -e "s:/lib:/%{_libdir}:g" makefile.cfg
sed -i -e "s:/etc/udev:/lib/udev:" svxlink/scripts/Makefile.default
sed -i -e "s:lgsm:lgsm -lspeex:" qtel/Makefile.default

#LDFLAGS="${LDFLAGS:--Wl,-as-needed}" ; export LDFLAGS
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS
%make
doxygen doxygen.async
doxygen doxygen.echolib


%install
make DESTDIR=%{buildroot} NO_CHOWN=1 LIB_INSTALL_DIR=%{_libdir} \
        INC_INSTALL_DIR=%{_includedir}/svxlink BIN_INSTALL_DIR=%{_bindir} \
        SBIN_INSTALL_DIR=%{_sbindir} PLUGIN_INSTALL_DIR=%{_libdir}/svxlink install
mkdir -p %{buildroot}%{_datadir}/svxlink
cp -a en_US-heather %{buildroot}%{_datadir}/svxlink/
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
rm -f %{buildroot}%{_libdir}/liblocationinfo.a
rm -f %{buildroot}%{_libdir}/libtrx.a


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


