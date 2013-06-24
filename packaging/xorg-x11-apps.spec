%define _unpackaged_files_terminate_build 0

Summary: X.Org X11 applications
Name: xorg-x11-apps
# NOTE: The package version should be set to the X11 major release from which
# the OS release is based upon.
Version: 7.6
Release: 5
License: MIT
Group: User Interface/X
URL: http://www.x.org

Source: %{name}-%{version}.tar.gz

# Clock apps
#Source0:  ftp://ftp.x.org/pub/individual/app/oclock-1.0.2.tar.bz2
#Source1:  ftp://ftp.x.org/pub/individual/app/xclock-1.0.5.tar.bz2
# X Window Dump (xwd) utilities
#Source2:  ftp://ftp.x.org/pub/individual/app/xwd-1.0.4.tar.bz2
#Source3:  ftp://ftp.x.org/pub/individual/app/xwud-1.0.3.tar.bz2
#Source4:  ftp://ftp.x.org/pub/individual/app/xpr-1.0.3.tar.bz2
# Miscellaneous other applications
#Source5:  ftp://ftp.x.org/pub/individual/app/luit-1.1.0.tar.bz2
#Source6:  ftp://ftp.x.org/pub/individual/app/x11perf-1.5.3.tar.bz2
#Source7:  ftp://ftp.x.org/pub/individual/app/xbiff-1.0.2.tar.bz2
#Source8:  ftp://ftp.x.org/pub/individual/app/xclipboard-1.1.1.tar.bz2
#Source9:  ftp://ftp.x.org/pub/individual/app/xconsole-1.0.4.tar.bz2
#Source10: ftp://ftp.x.org/pub/individual/app/xcursorgen-1.0.4.tar.bz2
#Source11: ftp://ftp.x.org/pub/individual/app/xeyes-1.1.1.tar.bz2
#Source13: ftp://ftp.x.org/pub/individual/app/xload-1.1.0.tar.bz2
#Source14: ftp://ftp.x.org/pub/individual/app/xlogo-1.0.3.tar.bz2
#Source15: ftp://ftp.x.org/pub/individual/app/xmag-1.0.4.tar.bz2
#Source16: ftp://ftp.x.org/pub/individual/app/xmessage-1.0.3.tar.bz2
#Source18: ftp://ftp.x.org/pub/individual/app/xfd-1.1.0.tar.bz2
#Source19: ftp://ftp.x.org/pub/individual/app/xfontsel-1.0.3.tar.bz2
#Source20: ftp://ftp.x.org/pub/individual/app/xvidtune-1.0.2.tar.bz2
#Source21: ftp://ftp.x.org/pub/individual/app/xev-1.2.1.tar.bz2

#Patch0: x11perf-1.4.1-x11perf-datadir-cleanups.patch
#Patch2: xconsole-1.0.3-streams-me-softer.patch
#Patch6: xbiff-1.0.2-xmu-configure.patch

BuildRequires: autoconf automake

# xfd needs gettext
BuildRequires: gettext
BuildRequires: zlib-devel
BuildRequires: libfontenc-devel
BuildRequires: libX11-devel
BuildRequires: libXmu-devel
BuildRequires: libXext-devel
BuildRequires: libXt-devel
BuildRequires: libXaw-devel
BuildRequires: libXpm-devel
BuildRequires: libXft-devel
BuildRequires: libXrender-devel
BuildRequires: libxkbfile-devel
BuildRequires: libXcursor-devel
BuildRequires: libpng-devel
BuildRequires: libXfixes-devel
BuildRequires: libXi-devel >= 1.2
BuildRequires: libXxf86vm-devel
BuildRequires: xbitmaps-devel
BuildRequires: libXrandr-devel
BuildRequires: xproto

Provides: luit oclock x11perf xclipboard xclock xconsole xcursorgen
Provides: xeyes xload xlogo xmag xmessage xpr xwd xwud
Provides: xfd xfontsel xvidtune
#Provides: xbiff

# NOTE: xwd, xwud, luit used to be in these.
#Obsoletes: XFree86, xorg-x11
# NOTE: x11perf, xclipboard used to be in these.
#Obsoletes: XFree86-tools, xorg-x11-tools
# Xaw app moves
#Conflicts: xorg-x11-utils < 7.4-5.fc12
#Conflicts: xorg-x11-server-utils < 7.4-8.fc12

%description
A collection of common X Window System applications.

%define apps luit oclock x11perf xclipboard xclock xconsole xcursorgen xeyes xload xlogo xmag xmessage xpr xwd xwud xfd xfontsel xvidtune

%prep
%setup -q
#%setup -q -c %{name}-%{version} -a1 -a2 -a3 -a4 -a5 -a6 -a7 -a8 -a9 -a10 -a11 -a13 -a14 -a15 -a16 -a18 -a19 -a20
#%patch0 -p0 -b .x11perf-datadir-cleanups
##%patch2 -p0 -b .streams-me-softer
#%patch6 -p1 -b .xmu-configure

%build
# Build all apps
{
CFLAGS="${CFLAGS} -D_F_BLOCK_MULTI_VIS_"
for app in luit oclock x11perf xclipboard xclock xconsole xcursorgen xeyes xload xlogo xmag xmessage xpr xwd xwud xfd xfontsel xvidtune xev; do
	pushd $app
		sed -i '/XAW_/ s/)/, xaw7)/; /XAW_/ s/XAW_CHECK_XPRINT_SUPPORT/PKG_CHECK_MODULES/' configure.ac
		autoreconf -v --install
		%configure --disable-xprint
		make
	popd
done
}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}/usr/share/license
cp -af COPYING %{buildroot}/usr/share/license/%{name}

# Install all apps
{
for app in luit oclock x11perf xclipboard xclock xconsole xcursorgen xeyes xload xlogo xmag xmessage xpr xwd xwud xfd xfontsel xvidtune xev; do
	pushd $app
	make install DESTDIR=$RPM_BUILD_ROOT
	popd
done
}

%remove_docs

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/*
/usr/share/license/%{name}
#%{_bindir}/luit
#%{_bindir}/oclock
#%{_bindir}/x11perf
#%{_bindir}/x11perfcomp
#%{_bindir}/xbiff
#%{_bindir}/xclipboard
#%{_bindir}/xclock
#%{_bindir}/xconsole
#%{_bindir}/xcursorgen
#%{_bindir}/xcutsel
#%{_bindir}/xdpr
#%{_bindir}/xev
#%{_bindir}/xeyes
#%{_bindir}/xfd
#%{_bindir}/xfontsel
#%{_bindir}/xload
#%{_bindir}/xlogo
#%{_bindir}/xmag
#%{_bindir}/xmessage
#%{_bindir}/xpr
#%{_bindir}/xvidtune
#%{_bindir}/xwd
#%{_bindir}/xwud
#%{_datadir}/X11/app-defaults/Clock-color
#%{_datadir}/X11/app-defaults/XClipboard
#%{_datadir}/X11/app-defaults/XClock
#%{_datadir}/X11/app-defaults/XClock-color
#%{_datadir}/X11/app-defaults/XConsole
#%{_datadir}/X11/app-defaults/XFontSel
#%{_datadir}/X11/app-defaults/Xfd
#%{_datadir}/X11/app-defaults/XLoad
#%{_datadir}/X11/app-defaults/XLogo
#%{_datadir}/X11/app-defaults/XLogo-color
#%{_datadir}/X11/app-defaults/Xmag
#%{_datadir}/X11/app-defaults/Xmessage
#%{_datadir}/X11/app-defaults/Xmessage-color
#%{_datadir}/X11/app-defaults/Xvidtune
#%dir %{_datadir}/X11/x11perfcomp
#%{_datadir}/X11/x11perfcomp/Xmark
#%{_datadir}/X11/x11perfcomp/fillblnk
#%{_datadir}/X11/x11perfcomp/perfboth
#%{_datadir}/X11/x11perfcomp/perfratio
