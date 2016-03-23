Summary:	SIMD-accelerated JPEG codec that provides both the libjpeg and TurboJPEG APIs
Name:		mozjpeg
Version:	3.0
Release:	0.1
License:	BSD
Group:		Applications/Graphics
Source0:	https://github.com/mozilla/mozjpeg/releases/download/v%{version}/%{name}-%{version}-release-source.tar.gz
# Source0-md5:	98d47219fab80797907f2c9aceb2c9b7
URL:		https://github.com/mozilla/mozjpeg
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
%ifarch %{ix86} %{x8664}
BuildRequires:	nasm
%endif
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
mozjpeg was forked from libjpeg-turbo.

The mozjpeg package contains simple client programs for accessing the
libjpeg functions. It contains cjpeg, djpeg, jpegtran, rdjpgcom and
wrjpgcom. Cjpeg compresses an image file into JPEG format. Djpeg
decompresses a JPEG file into a regular image file. Jpegtran can
perform various useful transformations on JPEG files. Rdjpgcom
displays any text comments included in a JPEG file. Wrjpgcom inserts
text comments into a JPEG file.

%package libs
Summary:	mozjpeg libraries
Group:		Libraries
Conflicts:	libjpeg-turbo

%description libs
libmozjpeg is a JPEG image codec that uses SIMD instructions (MMX,
SSE2, NEON) to accelerate baseline JPEG compression and decompression
on x86, x86-64, and ARM systems. On such systems, libmozjpeg is
generally 2-4x as fast as libjpeg, all else being equal. On other
types of systems, libmozjpeg can still outperform libjpeg by a
significant amount, by virtue of its highly-optimized Huffman coding
routines. In many cases, the performance of libmozjpeg rivals that of
proprietary high-speed JPEG codecs.

libmozjpeg implements both the traditional libjpeg API as well as the
less powerful but more straightforward TurboJPEG API. libmozjpeg also
features colorspace extensions that allow it to compress
from/decompress to 32-bit and big-endian pixel buffers (RGBX, XBGR,
etc.), as well as a full-featured Java interface.

%package devel
Summary:	Development files for libmozjpeg
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
The mozjpeg-devel package contains libraries and header files for
developing applications that use mozjpeg.

%prep
%setup -qc
mv mozjpeg/* .

# Fix perms
chmod -x README-turbo.txt

%build
%{__aclocal}
%{__libtoolize}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--disable-static

%{__make} %{?with_tests:test}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	docdir=%{_docdir} \
	exampledir=%{_docdir} \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc usage.txt wizard.txt
%attr(755,root,root) %{_bindir}/cjpeg
%attr(755,root,root) %{_bindir}/djpeg
%attr(755,root,root) %{_bindir}/jpegtran
%attr(755,root,root) %{_bindir}/rdjpgcom
%attr(755,root,root) %{_bindir}/wrjpgcom
%attr(755,root,root) %{_bindir}/tjbench
%{_mandir}/man1/cjpeg.1*
%{_mandir}/man1/djpeg.1*
%{_mandir}/man1/jpegtran.1*
%{_mandir}/man1/rdjpgcom.1*
%{_mandir}/man1/wrjpgcom.1*

%files libs
%defattr(644,root,root,755)
%doc README README-turbo.txt LICENSE.txt
%attr(755,root,root) %{_libdir}/libjpeg.so.*.*.*
%ghost %{_libdir}/libjpeg.so.62
%attr(755,root,root) %{_libdir}/libturbojpeg.so.*.*.*
%ghost %{_libdir}/libturbojpeg.so.0

%files devel
%defattr(644,root,root,755)
%doc coderules.txt jconfig.txt libjpeg.txt structure.txt example.c
%{_includedir}/jconfig.h
%{_includedir}/jerror.h
%{_includedir}/jmorecfg.h
%{_includedir}/jpeglib.h
%{_includedir}/turbojpeg.h
%{_libdir}/libjpeg.so
%{_libdir}/libturbojpeg.so
