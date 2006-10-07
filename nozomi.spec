#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)

#
# main package.
#
%define		_rel	1
Summary:	HSDPA driver for Broadband Wireless Data Card - Globe Trotter
Summary(pl):	Sterownik HSDPA dla kart bezprzewodowych Globe Trotter
Name:		nozomi
Version:	2.1
Release:	%{_rel}
Epoch:		0
License:	GPL
Group:		Base/Kernel
Source0:	http://www.pharscape.org/3G/%{name}_%{version}_060703.tar.gz
# Source0-md5:	56c822da9fbd95eca422873bafff8cd3
URL:		http://www.pharscape.org/
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 3:2.6.14}
BuildRequires:	rpmbuild(macros) >= 1.286
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
HSDPA driver for Broadband Wireless Data Card - Globe Trotter.

%description -l pl
Sterownik HSDPA dla kart bezprzewodowych Globe Trotter.

%package -n kernel-char-nozomi
Summary:	Linux HSDPA driver for Broadband Wireless Data Card - Globe Trotter
Summary(pl):	Sterownik HSDPA dla Linuksa do kart bezprzewodowych Globe Trotter
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif

%description -n kernel-char-nozomi
This is HSDPA driver for Broadband Wireless Data Card - Globe Trotter
for Linux.

This package contains Linux module.

%description -n kernel-char-nozomi -l pl
Sterownik HSDPA dla Linuksa do kart bezprzewodowych Globe Trotter.

Ten pakiet zawiera modu³ j±dra Linuksa.

%package -n kernel-smp-char-nozomi
Summary:	Linux SMP HSDPA driver for Broadband Wireless Data Card - Globe Trotter
Summary(pl):	Sterownik HSDPA dla Linuksa SMP do kart bezprzewodowych Globe Trotter
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif

%description -n kernel-smp-char-nozomi
This is HSDPA driver for Broadband Wireless Data Card - Globe Trotter
for Linux.

This package contains Linux SMP module.

%description -n kernel-smp-char-nozomi -l pl
Sterownik HSDPA dla Linuksa do kart bezprzewodowych Globe Trotter.

Ten pakiet zawiera modu³ j±dra Linuksa SMP.

%prep
%setup -q -c

echo 'obj-m += nozomi.o' > Makefile

%build
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	install -d o/include/linux
	ln -sf %{_kernelsrcdir}/config-$cfg o/.config
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg o/Module.symvers
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h o/include/linux/autoconf.h
%if %{with dist_kernel}
	%{__make} -j1 -C %{_kernelsrcdir} O=$PWD/o prepare scripts
%else
	install -d o/include/config
	touch o/include/config/MARKER
	ln -sf %{_kernelsrcdir}/scripts o/scripts
%endif
	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		SYSSRC=%{_kernelsrcdir} \
		SYSOUT=$PWD/o \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}
	%{__make} -C %{_kernelsrcdir} modules \
		CC="%{__cc}" CPP="%{__cpp}" \
		SYSSRC=%{_kernelsrcdir} \
		SYSOUT=$PWD/o \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}

	mv nozomi{,-$cfg}.ko
done

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/kernel/drivers/char
install nozomi-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/char/nozomi.ko
%if %{with smp} && %{with dist_kernel}
install nozomi-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/drivers/char/nozomi.ko
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel-char-nozomi
%depmod %{_kernel_ver}

%postun	-n kernel-char-nozomi
%depmod %{_kernel_ver}

%post	-n kernel-smp-char-nozomi
%depmod %{_kernel_ver}smp

%postun	-n kernel-smp-char-nozomi
%depmod %{_kernel_ver}smp

%files -n kernel-char-nozomi
%defattr(644,root,root,755)
%doc CHANGELOG readme todo
/lib/modules/%{_kernel_ver}/kernel/drivers/char/*.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-char-nozomi
%defattr(644,root,root,755)
%doc CHANGELOG readme todo
/lib/modules/%{_kernel_ver}smp/kernel/drivers/char/*.ko*
%endif
