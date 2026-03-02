Name:           redis-json
Version:        8.6.0
Release:        0.1%{?dist}
Summary:        RedisJSON module for Redis (Rust)

# RedisJSON licensing for Redis 8 series is published as tri-license (RSALv2 / SSPLv1 / AGPLv3).
# Set to match the LICENSE files actually present in your Source0 tarball.
License:        AGPL-3.0-only AND MIT AND Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause
URL:            https://github.com/RedisJSON/RedisJSON

# Your GitHub Release assets
Source0:        https://github.com/AngelYanev/redisjson-fedora/releases/download/v%{version}/redisjson-%{version}.tar.gz
Source1:        https://github.com/AngelYanev/redisjson-fedora/releases/download/v%{version}/redisjson-vendor-%{version}.tar.gz

ExclusiveArch:  %{rust_arches}

BuildRequires:  redis-devel
BuildRequires:  clang-devel

BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  rust-packaging
BuildRequires:  cargo-rpm-macros

# Correct Redis module ABI requirement / install conventions
Requires:       redis(modules_abi)%{?_isa} = %{redis_modules_abi}
Supplements:    redis

%global modso   rejson.so
%global cfgname redis-json.conf

%description
RedisJSON is a Redis module that implements JSON as a native data type.

%prep
# Source0 should untar to redisjson-8.6.0/ (because you used git archive --prefix=redisjson-8.6.0/)
# -a 1 unpacks Source1 (vendor tarball) into the build tree.
%autosetup -n redisjson-%{version} -a 1

# Optional: a small config snippet to load the module
cat > %{cfgname} <<'EOF'
# RedisJSON
loadmodule %{redis_modules_dir}/rejson.so
EOF

%build
# Prepare Cargo environment (Fedora Rust guideline) and point it at ./vendor for offline builds.
%cargo_prep -v vendor
%cargo_build --frozen --release

%install
mkdir -p %{buildroot}%{redis_modules_dir}

# RedisJSON output naming can vary; install whatever was produced into the canonical name.
if [ -f target/release/rejson.so ]; then
  install -Dpm755 target/release/rejson.so %{buildroot}%{redis_modules_dir}/%{modso}
elif [ -f target/release/librejson.so ]; then
  install -Dpm755 target/release/librejson.so %{buildroot}%{redis_modules_dir}/%{modso}
elif [ -f target/release/redisjson.so ]; then
  install -Dpm755 target/release/redisjson.so %{buildroot}%{redis_modules_dir}/%{modso}
else
  echo "ERROR: Could not find module .so in target/release"
  ls -la target/release || true
  exit 1
fi

# Install module config snippet if redis packaging exposes redis_modules_cfg
%if 0%{?redis_modules_cfg:1}
install -Dpm640 %{cfgname} %{buildroot}%{redis_modules_cfg}/%{cfgname}
%endif

%files
%license LICENSE* COPYING* NOTICE* 2>/dev/null || true
%doc README* CHANGELOG* 2>/dev/null || true
%{redis_modules_dir}/%{modso}
%if 0%{?redis_modules_cfg:1}
%config(noreplace) %{redis_modules_cfg}/%{cfgname}
%endif

%changelog
* Mon Mar 02 2026 Angel Yanev <angel.yanev@redis.com> - 8.6.0-0.1
- Initial COPR test build (vendored Rust deps; bundled provides deferred)