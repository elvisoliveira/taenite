# Taenite ISO Builder

`taenite.py` provides a `DockerManager` that builds a Debian-based Linux ISO in Docker, with Calamares branding and distribution customization driven by a `config` object.

## What This File Does

The build pipeline in `taenite.py`:

1. Creates a temporary Docker build context.
2. Writes config and branding files into that context.
3. Optionally copies logo/wallpaper assets.
4. Generates live-build hooks and Debian apt source files.
5. Builds a Docker image (`debian:12` base + `live-build`).
6. Runs the container and executes live-build to produce an ISO.
7. Copies `*.iso` into an output directory (typically `output/`).

It supports two Docker execution modes:
- Docker Python SDK (`docker.from_env()` / unix socket)
- Docker CLI subprocess fallback when SDK connection fails

## Requirements

- Linux host with Docker installed and running
- User allowed to access Docker (`docker` group or sudo)
- Python 3

## Basic Usage

1. Fill `config.yaml` (or copy from `config.yaml.example`).
2. Generate build context files in the current folder:

```bash
python3 taenite.py
```

3. Run the printed Docker commands manually.

Generated ISO output will be under `./output`.

## How To Run

`live-build` mounts `/proc` and `/dev/pts` inside the build container, so unprivileged containers usually fail with `permission denied` (often `exit status 32`).

Use privileged mode when running the image.

### nerdctl

```bash
nerdctl build -t taeniteos-builder .
nerdctl run --rm --privileged --network=host \
  -v ./output:/build/output \
  taeniteos-builder
```

If your environment still blocks mounts, also try:

```bash
nerdctl run --rm --privileged \
  --security-opt apparmor=unconfined \
  --security-opt seccomp=unconfined \
  --network=host \
  -v ./output:/build/output \
  taeniteos-builder
```

### docker

```bash
docker build -t taeniteos-builder .
docker run --rm --privileged --network=host \
  -v ./output:/build/output \
  taeniteos-builder
```

## Build Internals (Hardcoded Behavior)

These values are currently fixed in code:

- Base image: `debian:12`
- Live-build distribution: `bookworm`
- Architecture: `amd64`
- Image type: `iso-hybrid`
- Mirrors:
  - `http://deb.debian.org/debian`
  - `http://security.debian.org/debian-security`
- `--apt-recommends false`
- Boot parameters always start with: `boot=live components hostname=<distro_name> username=live`

## Configuration Variables

The `config` object passed to `start_build(config, callback)` must expose these attributes.

### Core Identity

- `distro_name` (`str`): Distribution/product name.
- `distro_version` (`str`): Version label used in ISO metadata and branding.
- `desktop_environment` (`str`): Intended DE selection (`gnome`, `kde`, `xfce`, `mate`, `cinnamon`). Invalid values fall back to GNOME in the legacy setup script logic.

### Branding / Assets

- `logo_path` (`str | None`): Path to logo image. If file exists, copied as `logo.png`.
- `wallpaper_path` (`str | None`): Path to wallpaper image. If file exists, copied as `wallpaper.png` / Calamares welcome image.
- `calamares_branding_product_name` (`str`)
- `calamares_branding_short_product_name` (`str`)
- `calamares_branding_version` (`str`)
- `calamares_branding_short_version` (`str`)

### Localization / Host

- `timezone` (`str`): e.g. `America/New_York`.
- `locale` (`str`): e.g. `en_US.UTF-8`.
- `keyboard_layout` (`str`): e.g. `us`, `br`.
- `hostname_prefix` (`str`): Present in generated script variables; currently not applied later.

### Features / Services

- `enable_autologin` (`bool`): Sets display-manager autologin for `live` user.
- `enable_firewall` (`bool`): Enables and configures UFW defaults.
- `enable_ssh` (`bool`): Adds SSH package logic; also opens UFW ssh when firewall is enabled.

### Boot

- `boot_quiet` (`bool`): Adds `quiet splash` to boot parameters.
- `boot_splash` (`bool`): When `False`, adds `plymouth.enable=0`.

### Packages

- `packages` (`list[str]`): Custom package names joined into `custom.list.chroot` (in legacy setup script logic).

### Serialization

- `to_yaml()` (`callable -> str`): Method used to write `config/build_config.yaml` in build context.

## Options Referenced but Not Wired From `config`

The generated shell template references additional toggles, but `taenite.py` does not assign them from `config` before use:

- `include_dev_tools`
- `include_restricted`

These currently have no direct `config.<name>` source in this file.

## Important Implementation Notes

`taenite.py` writes `setup.sh` twice:

- First write: large script containing package-list/theming/localization logic.
- Second write: shorter script with `lb config` command.

The second write overwrites the first one, so behavior present only in the first script may not execute in the final container run.

## Generated Files/Artifacts

During build context creation, the script creates files such as:

- `config/build_config.yaml`
- `calamares/branding.yaml`
- `config/archives/debian.list.chroot`
- `config/archives/debian.pref.chroot`
- `config/hooks/live/*.hook.chroot`
- `config/includes.chroot/etc/skel/Desktop/install.desktop`
- `Dockerfile`
- `setup.sh`

ISO output is expected in:

- `output/*.iso`

## Troubleshooting

If Docker is unavailable, `start_build()` reports actionable guidance, including:

- Ensure Docker daemon is running.
- Add your user to the `docker` group.
- Re-login after group changes.
