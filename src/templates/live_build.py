from src.constants import (
    DEFAULT_DEBIAN_MIRROR,
    DEBIAN_SECURITY_MIRROR,
    DEBIAN_VERSION,
)


def generate_debian_sources():
    return f"""deb {DEFAULT_DEBIAN_MIRROR} {DEBIAN_VERSION} main contrib non-free non-free-firmware
deb {DEBIAN_SECURITY_MIRROR} {DEBIAN_VERSION}-security main contrib non-free non-free-firmware
deb {DEFAULT_DEBIAN_MIRROR} {DEBIAN_VERSION}-updates main contrib non-free non-free-firmware
"""


def generate_debian_preferences():
    return """Package: *
Pin: release o=Debian
Pin-Priority: 900
"""


def generate_boot_params(config):
    boot_params = f"boot=live components hostname={config.distro_name} username=live"
    if config.boot_quiet:
        boot_params += " quiet splash"
    if not config.boot_splash:
        boot_params += " plymouth.enable=0"
    return boot_params


def generate_lb_config(config):
    boot_params = generate_boot_params(config)
    return f"""lb config \\
  --distribution {DEBIAN_VERSION} \\
  --architectures amd64 \\
  --binary-images iso-hybrid \\
  --bootappend-live "{boot_params}" \\
  --iso-application "{config.distro_name}" \\
  --iso-publisher "Custom Distribution" \\
  --iso-volume "{config.distro_name} {config.distro_version}" \\
  --mirror-bootstrap "{DEFAULT_DEBIAN_MIRROR}" \\
  --mirror-binary "{DEFAULT_DEBIAN_MIRROR}" \\
  --apt-recommends false
"""


def generate_setup_script(config):
    return f"""#!/bin/bash
# Setup script for live-build configuration

# Parse YAML configuration
distro_name="{config.distro_name}"
distro_version="{config.distro_version}"

# Execute live-build configuration
{generate_lb_config(config)}
"""


def generate_dockerfile(config):
    return """FROM debian:12

# Basic setup
RUN apt-get update && apt-get install -y \\
    live-build \\
    debootstrap \\
    curl \\
    wget \\
    git \\
    python3 \\
    sudo

WORKDIR /build

# Copy config, assets and scripts
COPY config/ /build/config/
COPY assets/ /build/assets/
COPY calamares/ /build/calamares/
COPY setup.sh /build/setup.sh

# Make scripts executable
RUN chmod +x /build/setup.sh

# Create output directory
RUN mkdir -p /build/output

# Build script
RUN echo '#!/bin/bash' > /build/build.sh && \\
    echo 'set -e' >> /build/build.sh && \\
    echo 'cd /build' >> /build/build.sh && \\
    echo './setup.sh' >> /build/build.sh && \\
    echo 'find /build/config/hooks/ -type f -name "*.hook.*" -exec chmod +x {} \\;' >> /build/build.sh && \\
    echo 'lb build' >> /build/build.sh && \\
    echo 'find /build -name "*.iso" -type f -exec cp -v {} /build/output/ \\;' >> /build/build.sh && \\
    echo 'echo "Build completed. Check output directory for the ISO file."' >> /build/build.sh && \\
    chmod +x /build/build.sh

CMD ["/build/build.sh"]
"""
