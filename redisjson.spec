Name:           redisjson
Version:        1.0.0
Release:        1%{?dist}
Summary:        JSON data type support module for Redis

License:        AGPL-3.0-only AND MIT AND Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause
URL:            https://github.com/RedisJSON/RedisJSON

# Upstream RedisJSON sources and release tarballs (release tag v%{upstream_version}).
%global upstream_version 8.6.0

Source0:        https://github.com/AngelYanev/redisjson-fedora/releases/download/v%{upstream_version}/redisjson-%{upstream_version}.tar.gz
Source1:        https://github.com/AngelYanev/redisjson-fedora/releases/download/v%{upstream_version}/redisjson-vendor-%{upstream_version}.tar.gz

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

# Registry crates that Fedora also ships as rust-*-devel (policy / licensing cross-check).
# The build still uses ``Source1`` vendor offline. Refresh from ``redisJSON-rpm``:
# ``python3 ../scripts/fedora_crate_audit.py ../RedisJSON/Cargo.lock --out-dir .``
# then replace the ``rust-*`` block below with ``fedora-buildrequires.inc``.
# Omit ``rust-nix*`` from %%BuildRequires — COPR/mock often cannot resolve those names; crate ``nix`` is vendored and listed under ``bundled(crate(nix))`` below.
BuildRequires:  rust-addr2line-devel
BuildRequires:  rust-adler2-devel
BuildRequires:  rust-ahash-devel
BuildRequires:  rust-aho-corasick-devel
BuildRequires:  rust-autocfg-devel
BuildRequires:  rust-backtrace-devel
BuildRequires:  rust-base64-devel
BuildRequires:  rust-bitflags1-devel
BuildRequires:  rust-bitvec-devel
BuildRequires:  rust-block-buffer-devel
BuildRequires:  rust-bumpalo-devel
BuildRequires:  rust-cexpr-devel
BuildRequires:  rust-cfg-if-devel
BuildRequires:  rust-clang-sys-devel
BuildRequires:  rust-cpufeatures-devel
BuildRequires:  rust-crunchy-devel
BuildRequires:  rust-crypto-common0.1-devel
BuildRequires:  rust-dashmap5-devel
BuildRequires:  rust-digest-devel
BuildRequires:  rust-either-devel
BuildRequires:  rust-env_logger0.10-devel
BuildRequires:  rust-equivalent-devel
BuildRequires:  rust-errno-devel
BuildRequires:  rust-funty-devel
BuildRequires:  rust-generic-array-devel
BuildRequires:  rust-getrandom0.2-devel
BuildRequires:  rust-getrandom0.3-devel
BuildRequires:  rust-gimli-devel
BuildRequires:  rust-glob-devel
BuildRequires:  rust-half-devel
BuildRequires:  rust-hashbrown-devel
BuildRequires:  rust-hashbrown0.13-devel
BuildRequires:  rust-hashbrown0.14-devel
BuildRequires:  rust-heck0.4-devel
BuildRequires:  rust-hex-devel
BuildRequires:  rust-home-devel
BuildRequires:  rust-humantime-devel
BuildRequires:  rust-is-terminal-devel
BuildRequires:  rust-itertools0.13-devel
BuildRequires:  rust-lazy_static-devel
BuildRequires:  rust-lazycell-devel
BuildRequires:  rust-libloading-devel
BuildRequires:  rust-linux-raw-sys0.4-devel
BuildRequires:  rust-lock_api-devel
BuildRequires:  rust-log-devel
BuildRequires:  rust-memoffset0.7-devel
BuildRequires:  rust-minimal-lexical-devel
BuildRequires:  rust-miniz_oxide-devel
BuildRequires:  rust-nom7-devel
BuildRequires:  rust-num-conv-devel
BuildRequires:  rust-num-traits-devel
BuildRequires:  rust-object-devel
BuildRequires:  rust-once_cell-devel
BuildRequires:  rust-parking_lot_core-devel
BuildRequires:  rust-paste-devel
BuildRequires:  rust-peeking_take_while-devel
BuildRequires:  rust-pin-utils-devel
BuildRequires:  rust-powerfmt-devel
BuildRequires:  rust-ppv-lite86-devel
BuildRequires:  rust-prettyplease-devel
BuildRequires:  rust-quote0.3-devel
BuildRequires:  rust-radium-devel
BuildRequires:  rust-rand-devel
BuildRequires:  rust-rand_chacha-devel
BuildRequires:  rust-rand_core-devel
BuildRequires:  rust-regex-devel
BuildRequires:  rust-rustc-demangle-devel
BuildRequires:  rust-rustc-hash1-devel
BuildRequires:  rust-rustix0.38-devel
BuildRequires:  rust-rustversion-devel
BuildRequires:  rust-ryu-devel
BuildRequires:  rust-scopeguard-devel
BuildRequires:  rust-serde-devel
BuildRequires:  rust-serde_bytes-devel
BuildRequires:  rust-serde_core-devel
BuildRequires:  rust-serde_derive-devel
BuildRequires:  rust-sha2-devel
BuildRequires:  rust-shlex-devel
BuildRequires:  rust-smallvec-devel
BuildRequires:  rust-strum_macros0.24-devel
BuildRequires:  rust-syn1-devel
BuildRequires:  rust-tap-devel
BuildRequires:  rust-termcolor-devel
BuildRequires:  rust-typenum-devel
BuildRequires:  rust-ucd-trie-devel
BuildRequires:  rust-version_check-devel
BuildRequires:  rust-which4-devel
BuildRequires:  rust-wyz-devel

# Bundled crates: git/path deps, workspace members, and registry versions not in Fedora at this lockfile.
# Refresh via ``../scripts/fedora_crate_audit.py`` (bundled-provides.inc snippet) when the lockfile changes.
Provides: bundled(crate(common)) = 0.1.0+git.3ff28c8c2987
Provides: bundled(crate(ijson)) = 0.1.3+git.5676f5929863
Provides: bundled(crate(redis-module)) = 2.1.3+git.3ff28c8c2987
Provides: bundled(crate(redis-module-macros)) = 99.99.99+git.3ff28c8c2987
Provides: bundled(crate(redis-module-macros-internals)) = 99.99.99+git.3ff28c8c2987
Provides: bundled(crate(json_path)) = 0.1.0
Provides: bundled(crate(redis_json)) = 8.6.0
# Vendored from ``Source1`` only (no ``rust-nix*`` %%BuildRequires; see rust block comment).
Provides: bundled(crate(nix)) = 0.26.4
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
%autosetup -n redisjson-%{upstream_version} -a 1

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
%cargo_vendor_manifest vendor
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
* Tue Apr 14 2026 Angel Yanev <angel.yanev@redis.com> - 1.0.0-1
- Development packaging (``Version`` 1.0.0; upstream tarball names use ``%%global upstream_version``). No ``hybrid_vendor`` — ``%%cargo_vendor_manifest vendor`` only.
- Inline ``rust-*-devel`` %%BuildRequires from ``fedora_crate_audit.py`` (``RedisJSON/Cargo.lock``); omit ``rust-nix*``; ``bundled(crate(nix))`` for vendored ``nix``.
