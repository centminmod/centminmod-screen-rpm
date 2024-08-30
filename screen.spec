%bcond_with multiuser
%global _hardened_build 1

Summary:        A screen manager that supports multiple logins on one terminal
Name:           screen
Version:        5.0.0
Release:        1%{?dist}
License:        GPLv3+
URL:            http://www.gnu.org/software/screen
Requires(pre):  /usr/sbin/groupadd
Requires(preun): /sbin/install-info
Requires(post): /sbin/install-info
BuildRequires:  ncurses-devel pam-devel autoconf
BuildRequires:  automake gcc
BuildRequires:  systemd
BuildRequires:  gettext-devel
BuildRequires:  systemd-devel

Source0:        screen-%{version}.tar.gz
Source1:        screen.pam

%description
The screen utility allows you to have multiple logins on just one
terminal. Screen is useful for users who telnet into a machine or are
connected via a dumb terminal but want to use more than just one
login.

Install the screen package if you need a screen manager that can
support multiple logins on one terminal.

%prep
%autosetup -p1

%build
./autogen.sh

%configure \
   --enable-pam \
   --enable-colors256 \
   --enable-rxvt_osc \
   --enable-use-locale \
   --enable-telnet \
   --with-pty-mode=0620 \
   --with-pty-group=$(getent group tty | cut -d : -f 3) \
   --with-sys-screenrc="%{_sysconfdir}/screenrc" \
   --with-socket-dir="%{_rundir}/screen"

sed -i -e 's/.*#.*undef.*HAVE_BRAILLE.*/#define HAVE_BRAILLE 1/;' config.h
sed -i -e 's/\(\/usr\)\?\/local\/etc/\/etc/g;' doc/screen.{1,texinfo}

for i in doc/screen.texinfo; do
    iconv -f iso8859-1 -t utf-8 < $i > $i.utf8 && mv -f ${i}{.utf8,}
done

rm -f doc/screen.info*
make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
mv -f $RPM_BUILD_ROOT%{_bindir}/screen{-%{version},}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
install -m 0644 etc/etcscreenrc $RPM_BUILD_ROOT%{_sysconfdir}/screenrc
cat etc/screenrc >> $RPM_BUILD_ROOT%{_sysconfdir}/screenrc

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pam.d
install -p -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/screen

mkdir -p $RPM_BUILD_ROOT%{_rundir}/screen

mkdir -p $RPM_BUILD_ROOT%{_tmpfilesdir}
cat <<EOF > $RPM_BUILD_ROOT%{_tmpfilesdir}/screen.conf
%if %{with multiuser}
d %{_rundir}/screen 0755 root root
%else
d %{_rundir}/screen 0775 root screen
%endif
EOF

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%pre
/usr/sbin/groupadd -g 84 -r -f screen
:

%post
:

%preun
:

%files
%doc README doc/FAQ doc/README.DOTSCREEN ChangeLog
%license COPYING
%{_mandir}/man1/screen.*
%{_datadir}/screen
%config(noreplace) %{_sysconfdir}/screenrc
%config(noreplace) %{_sysconfdir}/pam.d/screen
%{_tmpfilesdir}/screen.conf
%if %{with multiuser}
%attr(4755,root,root) %{_bindir}/screen
%attr(755,root,root) %{_rundir}/screen
%else
%attr(2755,root,screen) %{_bindir}/screen
%attr(775,root,screen) %{_rundir}/screen
%endif

%changelog
* Sat Aug 31 2024 George Liu <centminmod.com> - 5.0-1
- Initial build of screen 5.0 for Centmin Mod LEMP stacks.