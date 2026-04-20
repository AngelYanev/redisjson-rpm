Name:           redisjson
Version:        8.6.0
Release:        21%{?dist}
Summary:        JSON data type support module for Redis

License:        AGPL-3.0-only AND MIT AND Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause
URL:            https://github.com/RedisJSON/RedisJSON

# hybrid_vendor: same full crates.io vendor tarball as the default build (bytes must match Cargo.lock checksums).
# Pruning registry trees and re-copying from Fedora %%{_prefix}/share/cargo/registry breaks ``cargo build --frozen``
# (Fedora-normalized sources differ from crates.io). Optional smaller-tarball experiments stay in ../scripts/.
%bcond_with hybrid_vendor

Source0:        https://github.com/AngelYanev/redisjson-fedora/releases/download/v%{version}/redisjson-%{version}.tar.gz
Source1:        https://github.com/AngelYanev/redisjson-fedora/releases/download/v%{version}/redisjson-vendor-%{version}.tar.gz
%if %{with hybrid_vendor}
# ``cargo-vendor.txt`` from Cargo.lock instead of ``%%cargo_vendor_manifest`` / ``cargo tree``.
Source2:        cargo_vendor_txt_from_lock.py
%endif

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

# Bundled crates: git/path deps, workspace members, and registry versions not in Fedora at this lockfile.
# With hybrid_vendor, refresh via ../scripts/fedora_crate_audit.py (bundled-provides.inc snippet).
Provides: bundled(crate(common)) = 0.1.0+git.3ff28c8c2987
Provides: bundled(crate(ijson)) = 0.1.3+git.5676f5929863
Provides: bundled(crate(redis-module)) = 2.1.3+git.3ff28c8c2987
Provides: bundled(crate(redis-module-macros)) = 99.99.99+git.3ff28c8c2987
Provides: bundled(crate(redis-module-macros-internals)) = 99.99.99+git.3ff28c8c2987
Provides: bundled(crate(json_path)) = 0.1.0
Provides: bundled(crate(redis_json)) = 8.6.0
Provides: bundled(crate(bindgen)) = 0.66.1
Provides: bundled(crate(bitflags)) = 2.10.0
Provides: bundled(crate(bson)) = 2.15.0
Provides: bundled(crate(cc)) = 1.2.51
Provides: bundled(crate(deranged)) = 0.5.5
Provides: bundled(crate(enum-primitive-derive)) = 0.1.2
Provides: bundled(crate(find-msvc-tools)) = 0.1.6
Provides: bundled(crate(hermit-abi)) = 0.5.2
Provides: bundled(crate(indexmap)) = 2.12.1
Provides: bundled(crate(itoa)) = 1.0.17
Provides: bundled(crate(js-sys)) = 0.3.82
Provides: bundled(crate(libc)) = 0.2.178
Provides: bundled(crate(linkme)) = 0.3.35
Provides: bundled(crate(linkme-impl)) = 0.3.35
Provides: bundled(crate(memchr)) = 2.7.6
Provides: bundled(crate(num-traits)) = 0.1.43
Provides: bundled(crate(pest)) = 2.8.4
Provides: bundled(crate(pest_derive)) = 2.8.4
Provides: bundled(crate(pest_generator)) = 2.8.4
Provides: bundled(crate(pest_meta)) = 2.8.4
Provides: bundled(crate(proc-macro2)) = 1.0.104
Provides: bundled(crate(quote)) = 1.0.42
Provides: bundled(crate(r-efi)) = 5.3.0
Provides: bundled(crate(redox_syscall)) = 0.5.18
Provides: bundled(crate(regex-automata)) = 0.4.13
Provides: bundled(crate(regex-syntax)) = 0.8.8
Provides: bundled(crate(serde_json)) = 1.0.145
Provides: bundled(crate(serde_syn)) = 0.1.0
Provides: bundled(crate(syn)) = 0.11.11
Provides: bundled(crate(syn)) = 2.0.111
Provides: bundled(crate(synom)) = 0.11.3
Provides: bundled(crate(time)) = 0.3.44
Provides: bundled(crate(time-core)) = 0.1.6
Provides: bundled(crate(time-macros)) = 0.2.24
Provides: bundled(crate(unicode-ident)) = 1.0.22
Provides: bundled(crate(unicode-xid)) = 0.0.4
Provides: bundled(crate(uuid)) = 1.19.0
Provides: bundled(crate(wasi)) = 0.11.1+wasi~snapshot~preview1
Provides: bundled(crate(wasip2)) = 1.0.1+wasi~0.2.4
Provides: bundled(crate(wasm-bindgen)) = 0.2.105
Provides: bundled(crate(wasm-bindgen-macro)) = 0.2.105
Provides: bundled(crate(wasm-bindgen-macro-support)) = 0.2.105
Provides: bundled(crate(wasm-bindgen-shared)) = 0.2.105
Provides: bundled(crate(winapi-util)) = 0.1.11
Provides: bundled(crate(windows-link)) = 0.2.1
Provides: bundled(crate(windows-sys)) = 0.59.0
Provides: bundled(crate(windows-sys)) = 0.61.2
Provides: bundled(crate(windows-targets)) = 0.52.6
Provides: bundled(crate(windows_aarch64_gnullvm)) = 0.52.6
Provides: bundled(crate(windows_aarch64_msvc)) = 0.52.6
Provides: bundled(crate(windows_i686_gnu)) = 0.52.6
Provides: bundled(crate(windows_i686_gnullvm)) = 0.52.6
Provides: bundled(crate(windows_i686_msvc)) = 0.52.6
Provides: bundled(crate(windows_x86_64_gnu)) = 0.52.6
Provides: bundled(crate(windows_x86_64_gnullvm)) = 0.52.6
Provides: bundled(crate(windows_x86_64_msvc)) = 0.52.6
Provides: bundled(crate(wit-bindgen)) = 0.46.0
Provides: bundled(crate(zerocopy)) = 0.8.31
Provides: bundled(crate(zerocopy-derive)) = 0.8.31

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
%cargo_prep -v vendor
if [ -f vendor/.cargo/config.toml ]; then
  mkdir -p .cargo
  cp -a vendor/.cargo/config.toml .cargo/config.toml
else
  echo "ERROR: Could not find vendor/.cargo/config.toml"
  exit 1
fi
%if %{with hybrid_vendor}
python3 %{_sourcedir}/cargo_vendor_txt_from_lock.py .
%else
%cargo_vendor_manifest vendor
%endif
export CARGO_HOME=$PWD/.cargo
cargo build --frozen --release

#--------------------------------
# Install module
#--------------------------------
%install
mkdir -p %{buildroot}%{redis_modules_dir}

install -Dpm755 target/release/librejson.so %{buildroot}%{redis_modules_dir}/%{libname}

install -D -m0644 %{cfgname} %{buildroot}%{redis_confdir}/%{cfgname}

%files
%license LICENSE.txt
%license cargo-vendor.txt
%doc *.md
%{redis_modules_dir}/%{libname}
%config(noreplace) %{redis_confdir}/%{cfgname}

%changelog
* Wed Apr 15 2026 Angel Yanev <angel.yanev@redis.com> - 8.6.0-21
- Hybrid: drop redundant git-cargo append (full ``vendor/.cargo/config.toml`` already defines git sources).

* Wed Apr 15 2026 Angel Yanev <angel.yanev@redis.com> - 8.6.0-17
- Hybrid: restore_vendor_hybrid accepts ``vendor/<name>`` layout (not only ``name-version``).

* Wed Apr 15 2026 Angel Yanev <angel.yanev@redis.com> - 8.6.0-16
- Hybrid: restore pruned crates from Fedora registry when missing in vendor/; re-include fedora-buildrequires.inc.

* Wed Apr 15 2026 Angel Yanev <angel.yanev@redis.com> - 8.6.0-15
- Hybrid: cargo-vendor.txt from Cargo.lock (pruned vendor lacks crates cargo tree needs).

* Wed Apr 15 2026 Angel Yanev <angel.yanev@redis.com> - 8.6.0-14
- Hybrid: drop Fedora merge at %%build (Cargo.lock checksum mismatch); minimal tarball must be prune-only crates.io vendor.
- Makefile: ``mock`` passes ``--with hybrid_vendor`` to mock.

* Tue Apr 14 2026 Angel Yanev <angel.yanev@redis.com> - 8.6.0-3
- Inline bundled Provides; drop auxiliary packaging-only files.

* Tue Apr 14 2026 Angel Yanev <angel.yanev@redis.com> - 8.6.0-2
- Add bundled Provides for crates not covered by Fedora rust-* at lock versions.

* Mon Mar 02 2026 Angel Yanev <angel.yanev@redis.com> - 8.6.0-1
- Initial package for RedisJSON module
