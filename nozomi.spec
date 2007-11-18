#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_with	verbose		# verbose build (V=1)

%define		_rel	10
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
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
HSDPA driver for Broadband Wireless Data Card - Globe Trotter.

%description -l pl.UTF-8
Sterownik HSDPA dla kart bezprzewodowych Globe Trotter.

%package -n kernel%{_alt_kernel}-char-%{name}
Summary:	Linux HSDPA driver for Broadband Wireless Data Card - Globe Trotter
Summary(pl.UTF-8):	Sterownik HSDPA dla Linuksa do kart bezprzewodowych Globe Trotter
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:%requires_releq_kernel}

%description -n kernel%{_alt_kernel}-char-%{name}
This is HSDPA driver for Broadband Wireless Data Card - Globe Trotter
for Linux.

This package contains Linux module.

%description -n kernel%{_alt_kernel}-char-%{name} -l pl.UTF-8
Sterownik HSDPA dla Linuksa do kart bezprzewodowych Globe Trotter.

Ten pakiet zawiera moduł jądra Linuksa.

%prep
%setup -q -c
%patch0 -p1
%patch1 -p1
cat > Makefile <<'EOF'
obj-m += nozomi.o
nozomi-objs += kfifo.o
EOF

%build

%build_kernel_modules -m %{name}

%install
rm -rf $RPM_BUILD_ROOT

%install_kernel_modules -m %{name} -d kernel/drivers/char

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-char-%{name}
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-char-%{name}
%depmod %{_kernel_ver}

%if %{with dist_kernel}
%files -n kernel%{_alt_kernel}-char-%{name}
%defattr(644,root,root,755)
%doc CHANGELOG readme todo
/lib/modules/%{_kernel_ver}/kernel/drivers/char/*.ko*
%endif
