Name:           openjade
Version:        1.3.2
Release:        61
Summary:        A implementation of DSSSL
License:        DMIT
URL:            http://openjade.sourceforge.net/
Source0:        http://download.sourceforge.net/openjade/%{name}-%{version}.tar.gz
Source1:        config.guess
Source2:        config.sub

Patch0:         openjade-ppc64.patch
Patch1:         openjade-1.3.1-nsl.patch
Patch2:         openjade-deplibs.patch
Patch3:         openjade-nola.patch
Patch4:         openjade-1.3.2-gcc46.patch
Patch5:         openjade-getoptperl.patch

Provides:       jade = %{version}-%{release}
BuildRequires:  gcc-c++ opensp-devel perl-interpreter chrpath
Requires:       sgml-common

%description
OpenJade is a project undertaken by the DSSSL community to maintain and extend Jade,
as well as the related SP suite of SGML/XML processing tools. OpenJade and OpenSP are
distributed under the same license as Jade.

%package_help

%prep
%autosetup -n %{name}-%{version} -p1

%build
cp -p %{SOURCE1} %{SOURCE2} config/
export CXXFLAGS="%optflags -fno-lifetime-dse"
%configure --disable-static --datadir=%{_datadir}/sgml/%{name}-%{version} --enable-splibdir=%{_libdir}
%make_build

%install
%make_install install-man

ln -s openjade %{buildroot}%{_bindir}/jade
pushd %{buildroot}%{_mandir}/man1
ln -s %{name}.1 jade.1
popd

pushd dsssl
cp catalog %{buildroot}/%{_datadir}/sgml/%{name}-%{version}/
for file in *.dtd
do
    cp $file %{buildroot}/%{_datadir}/sgml/%{name}-%{version}/
done
popd

mkdir -p %{buildroot}/etc/sgml
pushd %{buildroot}/etc/sgml
touch %{name}-%{version}-%{release}.soc
ln -s %{name}-%{version}-%{release}.soc %{name}.soc
popd

pushd %{buildroot}%{_libdir}
rm -f *.so
rm -f *.la
popd

chrpath -d %{buildroot}/%{_libdir}/libospgrove.so.0.0.1
chrpath -d %{buildroot}/%{_libdir}/libostyle.so.0.0.1
chrpath -d %{buildroot}/%{_bindir}/openjade

%post
/sbin/ldconfig
/usr/bin/install-catalog --add /etc/sgml/%{name}-%{version}-%{release}.soc \
    %{_datadir}/sgml/%{name}-%{version}/catalog >/dev/null 2>/dev/null || :

%postun -p /sbin/ldconfig

%preun
/usr/bin/install-catalog --remove /etc/sgml/%{name}-%{version}-%{release}.soc \
    %{_datadir}/sgml/%{name}-%{version}/catalog >/dev/null 2>/dev/null || :

%files
%doc README
%license COPYING
%ghost %{_sysconfdir}/sgml/%{name}-%{version}-%{release}.soc
%{_bindir}/*
%{_libdir}/*.so.*
%{_datadir}/sgml/%{name}-%{version}
%{_sysconfdir}/sgml/%{name}.soc

%files help
%doc jadedoc/* dsssl/README.jadetex VERSION
%{_mandir}/man1/*

%changelog
* Tue Aug 23 2022 wulei <wulei80@h-partners.com> - 1.3.2-61
- Remove rpath

* Tue Dec 3 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.3.2-60
- Package init
