#define beta rc
#define snapshot 20200627
%define major 6

%define _qtdir %{_libdir}/qt%{major}

%define libname %mklibname Qt6QuickControls2 %{major}
%define devname %mklibname -d Qt6QuickControls2

Name:		qt6-qtquickcontrols2
Version:	6.1.0
Release:	%{?beta:0.%{beta}.}%{?snapshot:0.%{snapshot}.}2
%if 0%{?snapshot:1}
# "git archive"-d from "dev" branch of git://code.qt.io/qt/qtbase.git
Source:		qtquickcontrols2-%{?snapshot:%{snapshot}}%{!?snapshot:%{version}}.tar.zst
%else
Source:		http://download.qt-project.org/%{?beta:development}%{!?beta:official}_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}%{?beta:-%{beta}}/submodules/qtquickcontrols2-everywhere-src-%{version}%{?beta:-%{beta}}.tar.xz
%endif
Group:		System/Libraries
Summary:	Qt %{major} Quick controls
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	%{_lib}Qt%{major}Core-devel
BuildRequires:	%{_lib}Qt%{major}Gui-devel
BuildRequires:	%{_lib}Qt%{major}Network-devel
BuildRequires:	%{_lib}Qt%{major}Qml-devel
BuildRequires:	%{_lib}Qt%{major}QmlDevTools-devel
BuildRequires:	%{_lib}Qt%{major}QmlModels-devel
BuildRequires:	%{_lib}Qt%{major}QmlQuick-devel
BuildRequires:	%{_lib}Qt%{major}QmlQuickWidgets-devel
BuildRequires:	%{_lib}Qt%{major}Xml-devel
BuildRequires:	%{_lib}Qt%{major}Widgets-devel
BuildRequires:	%{_lib}Qt%{major}QmlDevTools-devel
BuildRequires:	%{_lib}Qt%{major}Sql-devel
BuildRequires:	%{_lib}Qt%{major}PrintSupport-devel
BuildRequires:	%{_lib}Qt%{major}OpenGL-devel
BuildRequires:	%{_lib}Qt%{major}OpenGLWidgets-devel
BuildRequires:	%{_lib}Qt%{major}DBus-devel
BuildRequires:	qt%{major}-cmake
BuildRequires:	qt%{major}-qtdeclarative
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(vulkan)
BuildRequires:	cmake(LLVM)
BuildRequires:	cmake(Clang)
# Not really required, but referenced by LLVMExports.cmake
# (and then required because of the integrity check)
BuildRequires:	%{_lib}gpuruntime
License:	LGPLv3/GPLv3/GPLv2

%description
Qt %{major} Quick controls

%package -n %{libname}
Summary:	Qt %{major} Quick controls
Group:		System/Libraries
%rename %{name}

%description -n %{libname}
Qt %{major} Quick controls

%package -n %{devname}
Summary:	Qt %{major} Quick controls development files
Group:		Development/Qt and KDE

%description -n %{devname}
Qt %{major} Quick controls development files

%prep
%autosetup -p1 -n qtquickcontrols2%{!?snapshot:-everywhere-src-%{version}%{?beta:-%{beta}}}
# FIXME why are OpenGL lib paths autodetected incorrectly, preferring
# /usr/lib over /usr/lib64 even on 64-bit boxes?
%cmake -G Ninja \
	-DCMAKE_INSTALL_PREFIX=%{_qtdir} \
	-DQT_BUILD_EXAMPLES:BOOL=ON \
	-DQT_WILL_INSTALL:BOOL=ON

%build
export LD_LIBRARY_PATH="$(pwd)/build/lib:${LD_LIBRARY_PATH}"
%ninja_build -C build

%install
%ninja_install -C build
# Static helper lib without headers -- useless
rm -f %{buildroot}%{_libdir}/qt6/%{_lib}/libpnp_basictools.a
# Put stuff where tools will find it
# We can't do the same for %{_includedir} right now because that would
# clash with qt5 (both would want to have /usr/include/QtCore and friends)
mkdir -p %{buildroot}%{_bindir}
for i in %{buildroot}%{_qtdir}/lib/*.so*; do
	ln -s qt%{major}/lib/$(basename ${i}) %{buildroot}%{_libdir}/
done
mv %{buildroot}%{_qtdir}/lib/cmake %{buildroot}%{_libdir}/

%files -n %{libname}
%{_libdir}/libQt6QuickControls2.so.*
%{_libdir}/libQt6QuickControls2Impl.so.*
%{_libdir}/libQt6QuickTemplates2.so.*
%{_qtdir}/lib/libQt6QuickControls2.so.*
%{_qtdir}/lib/libQt6QuickControls2Impl.so.*
%{_qtdir}/lib/libQt6QuickTemplates2.so.*
%{_qtdir}/qml/Qt/labs/platform/libqtlabsplatformplugin.so
%{_qtdir}/qml/Qt/labs/platform/plugins.qmltypes
%{_qtdir}/qml/Qt/labs/platform/qmldir
%{_qtdir}/qml/QtQuick/Controls
%{_qtdir}/qml/QtQuick/NativeStyle
%{_qtdir}/qml/QtQuick/Templates

%files -n %{devname}
%{_libdir}/cmake/Qt6BuildInternals/StandaloneTests/QtQuickControls2TestsConfig.cmake
%{_libdir}/cmake/Qt6Qml/QmlPlugins/*
%{_libdir}/cmake/Qt6QuickControls2
%{_libdir}/cmake/Qt6QuickControls2Impl
%{_libdir}/cmake/Qt6QuickTemplates2
%{_libdir}/libQt6QuickControls2.so
%{_libdir}/libQt6QuickControls2Impl.so
%{_libdir}/libQt6QuickTemplates2.so
%{_qtdir}/examples/quickcontrols2
%{_qtdir}/include/QtQuickControls2
%{_qtdir}/include/QtQuickControls2Impl
%{_qtdir}/include/QtQuickTemplates2
%{_qtdir}/lib/libQt6QuickControls2.prl
%{_qtdir}/lib/libQt6QuickControls2.so
%{_qtdir}/lib/libQt6QuickControls2Impl.prl
%{_qtdir}/lib/libQt6QuickControls2Impl.so
%{_qtdir}/lib/libQt6QuickTemplates2.prl
%{_qtdir}/lib/libQt6QuickTemplates2.so
%{_qtdir}/lib/metatypes/*.json
%{_qtdir}/mkspecs/modules/*.pri
%{_qtdir}/modules/QuickControls2.json
%{_qtdir}/modules/QuickControls2Impl.json
%{_qtdir}/modules/QuickTemplates2.json
