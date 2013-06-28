Url:            http://expect.nist.gov
Name:           expect
BuildRequires:  autoconf
BuildRequires:  tcl-devel
Version:        5.45
Release:        0
Summary:        A Tool for Automating Interactive Programs
License:        SUSE-Public-Domain
Group:          Development/Languages/Tcl
Source:         %{name}%{version}.tar.gz
Source1:        expect-rpmlintrc
Source1001: 	expect.manifest

%description
Expect is a tool primarily for automating interactive applications,
such as telnet, ftp, passwd, fsck, rlogin, tip, and more.  Expect
really makes this stuff trivial.  Expect is also useful for testing
these applications.  It is described in many books, articles, papers,
and FAQs.  There is an entire book on it available from O'Reilly.

%package devel
Summary:        Header Files and C API Documentation for expect
Group:          Development/Libraries/Tcl

%description devel
This package contains header files and documentation needed for linking
to expect from programs written in compiled languages like C, C++, etc.

This package is not needed for developing scripts that run under the
/usr/bin/expect interpreter, or any other Tcl interpreter with the
expect package loaded.

%prep
%setup -q -n %name%version
cp %{SOURCE1001} .

%build
autoreconf
%configure \
	--with-tcl=%_libdir \
	--with-tk=no_tk \
	--with-tclinclude=%_includedir \
	--enable-shared
make %{?_smp_mflags} all pkglibdir=%_libdir/tcl/%name%version


%check
make test

%install
# set the right path to the expect binary...
sed -i \
    -e '1s,^#![^ ]*expectk,#!/usr/bin/wish\npackage require Expect,' \
    -e '1s,^#![^ ]*expect,#!/usr/bin/expect,' \
    example/*
make install DESTDIR=$RPM_BUILD_ROOT pkglibdir=%_libdir/tcl/%name%version
# Remove some executables and manpages we don't want to ship
rm $RPM_BUILD_ROOT%_prefix/bin/*passwd
rm $RPM_BUILD_ROOT%_mandir/*/*passwd*

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%_prefix/bin/*
%_libdir/tcl/*
%_libdir/lib*.so
%doc %_mandir/man1/*

%files devel
%manifest %{name}.manifest
%defattr(-,root,root)
%_includedir/*
%doc %_mandir/man3/*

%changelog
