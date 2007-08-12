#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	up		# don't build UP module
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)

#
# main package.
#
%define		_rel	1
Summary:	HSDPA driver for Broadband Wireless Data Card - Globe Trotter
Summary(pl.UTF-8):	Sterownik HSDPA dla kart bezprzewodowych Globe Trotter
Name:		nozomi
Version:	2.1
Release:	%{_rel}
Epoch:		0
License:	GPL
Group:		Base/Kernel
Source0:	http://www.pharscape.org/3G/%{name}_%{version}_060703.tar.gz
# Source0-md5:	56c822da9fbd95eca422873bafff8cd3
URL:		http://www.pharscape.org/
Patch0:		%{name}-tty_dont_flip.patch
Patch1:		%{name}-err.patch
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 3:2.6.14}
BuildRequires:	rpmbuild(macros) >= 1.308
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
HSDPA driver for Broadband Wireless Data Card - Globe Trotter.

%description -l pl.UTF-8
Sterownik HSDPA dla kart bezprzewodowych Globe Trotter.

%package -n kernel%{_alt_kernel}-char-nozomi
Summary:	Linux HSDPA driver for Broadband Wireless Data Card - Globe Trotter
Summary(pl.UTF-8):	Sterownik HSDPA dla Linuksa do kart bezprzewodowych Globe Trotter
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif

%description -n kernel%{_alt_kernel}-char-nozomi
This is HSDPA driver for Broadband Wireless Data Card - Globe Trotter
for Linux.

This package contains Linux module.

%description -n kernel%{_alt_kernel}-char-nozomi -l pl.UTF-8
Sterownik HSDPA dla Linuksa do kart bezprzewodowych Globe Trotter.

Ten pakiet zawiera moduł jądra Linuksa.

%package -n kernel%{_alt_kernel}-smp-char-nozomi
Summary:	Linux SMP HSDPA driver for Broadband Wireless Data Card - Globe Trotter
Summary(pl.UTF-8):	Sterownik HSDPA dla Linuksa SMP do kart bezprzewodowych Globe Trotter
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif

%description -n kernel%{_alt_kernel}-smp-char-nozomi
This is HSDPA driver for Broadband Wireless Data Card - Globe Trotter
for Linux.

This package contains Linux SMP module.

%description -n kernel%{_alt_kernel}-smp-char-nozomi -l pl.UTF-8
Sterownik HSDPA dla Linuksa do kart bezprzewodowych Globe Trotter.

Ten pakiet zawiera moduł jądra Linuksa SMP.

%prep
%setup -q -c
%patch0 -p1
%patch1 -p1

cat > Makefile << 'EOF'
obj-m += nozomi.o
nozomi-objs += kfifo.o
EOF

%build

%build_kernel_modules -m nozomi

%install
rm -rf $RPM_BUILD_ROOT

%install_kernel_modules -m nozomi -d kernel/drivers/char

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-char-nozomi
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-char-nozomi
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-smp-char-nozomi
%depmod %{_kernel_ver}smp

%postun	-n kernel%{_alt_kernel}-smp-char-nozomi
%depmod %{_kernel_ver}smp

%files -n kernel%{_alt_kernel}-char-nozomi
%defattr(644,root,root,755)
%doc CHANGELOG readme todo
/lib/modules/%{_kernel_ver}/kernel/drivers/char/*.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel%{_alt_kernel}-smp-char-nozomi
%defattr(644,root,root,755)
%doc CHANGELOG readme todo
/lib/modules/%{_kernel_ver}smp/kernel/drivers/char/*.ko*
%endif
