Summary: X.Org X11 applications
Name: xorg-x11-apps
Version: 7.5
Release: 2
License: MIT/X11
Group: User Interface/X
URL: http://www.x.org
Source: %{name}-%{version}.tar.gz

Patch0: 01_xedit_mkdir_races.diff
Patch1: 03_xconsole_implicit_pointer_conversion.diff
Patch2: 05_xmore_fix_segv_without_xprint.diff

BuildRequires: pkgconfig(xorg-macros)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xaw7)
BuildRequires: pkgconfig(xcursor)
BuildRequires: pkgconfig(xext)
BuildRequires: pkgconfig(xft)
BuildRequires: pkgconfig(xkbfile)
BuildRequires: pkgconfig(xmuu)
BuildRequires: pkgconfig(xrender)
BuildRequires: pkgconfig(xt)
BuildRequires: pkgconfig(xmu)
BuildRequires: pkgconfig(xbitmaps)

%define DEF_SUBDIRS bitmap ico oclock xcalc xclock xeyes xwd xwud

Provides: %{DEF_SUBDIRS}

# NOTE: xwd, xwud, luit used to be in these.
Obsoletes: XFree86, xorg-x11
# NOTE: x11perf, xclipboard used to be in these.
Obsoletes: XFree86-tools, xorg-x11-tools
%description
A collection of common X Window System applications.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
# Build all apps
{
    CFLAGS="${CFLAGS} -D_F_BLOCK_MULTI_VIS_"
    for app in %{DEF_SUBDIRS}; do
        pushd $app
        %configure \
            --disable-xprint \
            --with-sysmanpath=/usr/man:/usr/share/man:/usr/local/man:/usr/local/share/man:/usr/X11R6/man:/opt/man \
            RSH=rsh \
            MANCONF="/etc/manpath.config"
        popd
    done
}

%install
rm -rf $RPM_BUILD_ROOT
# Install all apps
{
   for app in %{DEF_SUBDIRS} ; do
      pushd $app
      make install DESTDIR=$RPM_BUILD_ROOT
      popd
   done
}

%remove_docs

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_bindir}/*
%{_includedir}/X11/bitmaps/*
/etc/X11/app-defaults/*
