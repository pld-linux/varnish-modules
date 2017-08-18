#
# Conditional build:
%bcond_without	tests		# build without tests

%define abi 6.0
%define abi 5.0
%define abi 3.2

Summary:	A collection of modules ("vmods") extending Varnish VCL
Name:		varnish-modules
Version:	0.12.1
Release:	0.1
License:	BSD
Group:		Daemons
Source0:	https://download.varnish-software.com/varnish-modules/%{name}-%{version}.tar.gz
# Source0-md5:	8b66080b29e20271ab1b7047307c4d69
URL:		https://github.com/varnish/varnish-modules
BuildRequires:	pkgconfig
BuildRequires:	python-docutils >= 0.6
BuildRequires:	varnish
BuildRequires:	varnish-devel >= 4.1.4
#BuildRequires:	varnish-libs-devel
Requires:	varnishabi-%abi
Provides:	vmod-cookie = %{version}-%{release}
Provides:	vmod-header = %{version}-%{release}
Provides:	vmod-saintmode = %{version}-%{release}
Provides:	vmod-softpurge = %{version}-%{release}
Provides:	vmod-tcp = %{version}-%{release}
Provides:	vmod-var = %{version}-%{release}
Provides:	vmod-vsthrottle = %{version}-%{release}
Provides:	vmod-xkey = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a collection of modules ("vmods") extending Varnish VCL used
for describing HTTP request/response policies with additional
capabilities. This collection contains the following vmods (previously
kept individually): cookie, vsthrottle, header, saintmode, softpurge,
tcp, var, xkey

%prep
%setup -q

%build
%configure \
	--disable-static

%{__make}

%if %{with tests}
%{__make} check
%endif

# Build man pages
cd docs
for i in vmod*.rst; do
	rst2man -v "$i" "$(basename $i .rst).3"
done
cd -

chmod 644 src/*.h
chmod 644 src/*.c
chmod 644 docs/*rst

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL="install -p" \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_mandir}/man3
cp -p docs/*.3 $RPM_BUILD_ROOT%{_mandir}/man3

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs AUTHORS CHANGES.rst COPYING LICENSE README.rst
%{_libdir}/varnish/vmods/*
%{_mandir}/man3/*.3*
