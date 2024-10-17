%global		_disable_ld_no_undefined	1
%global		module		Cgl

Name:		coin-or-%{module}

Summary:	Cut Generation Library
Version:	0.58.5
Release:	1%{?dist}
License:	EPL
URL:		https://projects.coin-or.org/%{module}
Source0:	http://www.coin-or.org/download/pkgsource/%{module}/%{module}-%{version}.tgz
Source1:	%{name}.rpmlintrc
BuildRequires:	blas-devel
BuildRequires:	bzip2-devel
BuildRequires:	coin-or-Clp-devel
BuildRequires:	coin-or-CoinUtils-devel
BuildRequires:	coin-or-Osi-devel
BuildRequires:	doxygen
BuildRequires:	glpk-devel
BuildRequires:	graphviz
BuildRequires:	lapack-devel
BuildRequires:	libatlas-devel
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
BuildRequires:	zlib-devel

# Properly handle DESTDIR
Patch0:		%{name}-pkgconfig.patch

# Install documentation in standard rpm directory
Patch1:		%{name}-docdir.patch

%description
The COIN-OR Cut Generation Library (Cgl) is a collection of cut generators
that can be used with other COIN-OR packages that make use of cuts, such as,
among others, the linear solver Clp or the mixed integer linear programming
solvers Cbc or BCP.

%package	devel
Summary:	Development files for %{name}

Requires:	coin-or-CoinUtils-devel
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package	doc
Summary:	Documentation files for %{name}

Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description	doc
This package contains the documentation for %{name}.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1
%patch1 -p1

%build
mkdir bin; pushd bin; ln -sf %{_bindir}/ld.bfd ld; popd; export PATH=$PWD/bin:$PATH
CFLAGS="%{optflags} -fuse-ld=bfd" CXXFLAGS="%{optflags} -fuse-ld=bfd" \
%configure2_5x
make %{?_smp_flags} all doxydoc

%install
export PATH=$PWD/bin:$PATH
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/*.la
cp -a doxydoc/html %{buildroot}%{_docdir}/%{name}

%check
export PATH=$PWD/bin:$PATH
make test

%files
%dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/AUTHORS
%doc %{_docdir}/%{name}/cgl_addlibs.txt
%doc %{_docdir}/%{name}/LICENSE
%doc %{_docdir}/%{name}/README
%{_libdir}/*.so.*

%files		devel
%{_includedir}/coin/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%files		doc
%doc %{_docdir}/%{name}/html

%changelog
* Wed Jan  8 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.58.5-1
- Update to latest upstream release.
- Remove "missing" patch applied upstream.

* Mon Nov  4 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.58.2-4
- Correct source url path (#894587#c7).
- Add coin-or-CoinUtils-devel requires to the devel package (#894587#c7).

* Fri Nov  1 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.58.2-3
- Install missing header file required by other coin-or modules.

* Fri Nov  1 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.58.2-2
- Use proper _smp_flags macro (#894586#c6).

* Fri Nov  1 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.58.2-1
- Update to latest upstream release.

* Mon Jan 14 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.57.4-1
- Update to latest upstream release.

* Sat Jan 12 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.57.3-3
- Rename repackaged tarball.

* Sun Nov 18 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.57.3-2
- Rename package to coin-or-Cgl.
- Do not package Thirdy party data or data without clean license.

* Thu Sep 27 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.57.3-1
- Initial coinor-Cgl spec.
