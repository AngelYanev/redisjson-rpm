Name:           redisjson
Version:        8.6.0
Release:        1%{?dist}
Summary:        JSON data type support module for Redis

License:        AGPL-3.0-only AND MIT AND Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause
URL:            https://github.com/RedisJSON/RedisJSON

Source0:        https://github.com/AngelYanev/redisjson-fedora/releases/download/v%{version}/redisjson-%{version}.tar.gz
Source1:        https://github.com/AngelYanev/redisjson-fedora/releases/download/v%{version}/redisjson-vendor-%{version}.tar.gz

%global redis_modules_dir %{_libdir}/redis/modules
%global redis_confdir    %{_sysconfdir}/redis/modules
%global libname rejson.so
%global cfgname redisjson.conf

ExclusiveArch:  x86_64 aarch64

BuildRequires:  redis-devel
BuildRequires:  clang-devel
BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  rust-packaging
BuildRequires:  cargo-rpm-macros

Provides: bundled(crate(common)) = 0.1.0+git.3ff28c8c2987
Provides: bundled(crate(ijson)) = 0.1.3+git.5676f5929863
Provides: bundled(crate(redis-module)) = 2.1.3+git.3ff28c8c2987
Provides: bundled(crate(redis-module-macros)) = 99.99.99+git.3ff28c8c2987
Provides: bundled(crate(redis-module-macros-internals)) = 99.99.99+git.3ff28c8c2987
Provides: bundled(crate(redis_json)) = 8.6.0

Supplements:    redis

%description
RedisJSON is a Redis module that implements ECMA-404 (JSON) as a native
data type. It allows storing, querying, and manipulating JSON documents
within Redis using JSONPath syntax. The module provides atomic operations
on JSON values, nested key access, and type-aware commands for arrays,
objects, strings, and numbers.

This package contains the shared library (rejson.so) that can be loaded
into a Redis server with the MODULE LOAD command or via configuration.

%prep
%autosetup -n redisjson-%{version} -a 1

cat > %{cfgname} <<'EOF'
loadmodule %{redis_modules_dir}/%{libname}
EOF

#--------------------------------
# Build module
#--------------------------------
%build
# Prepare and vendor dependencies using macros, then build
%cargo_prep -v vendor
# Ensure cargo uses the provided vendor directory (handles git deps like ijson)
if [ -f vendor/.cargo/config.toml ]; then
  mkdir -p .cargo
  cp -a vendor/.cargo/config.toml .cargo/config.toml
else
  echo "ERROR: Could not find vendor/.cargo/config.toml"
  exit 1
fi
# Generate vendor manifest for bundled provides and include as license
%cargo_vendor_manifest vendor
# Build with standard release profile using vendored sources, offline
export CARGO_HOME=$PWD/.cargo
cargo build --frozen --release

#--------------------------------
# Install module
#--------------------------------
%install
mkdir -p %{buildroot}%{redis_modules_dir}

# Enforce canonical module name
install -Dpm755 target/release/librejson.so %{buildroot}%{redis_modules_dir}/%{libname}

# install config into buildroot (autoload by default)
install -D -m0644 %{cfgname} %{buildroot}%{redis_confdir}/%{cfgname}

%files
%license LICENSE.txt
%license cargo-vendor.txt
%doc *.md
%{redis_modules_dir}/%{libname}
%config(noreplace) %{redis_confdir}/%{cfgname}

%changelog
* Mon Mar 02 2026 Angel Yanev <angel.yanev@redis.com> - 8.6.0-0.1
- Initial package for RedisJSON module