def generate_locale_timezone_hook(config):
    return f"""#!/bin/bash
# Set the default locale
echo "{config.locale}" > /etc/default/locale
sed -i 's/# {config.locale}/{config.locale}/' /etc/locale.gen
locale-gen

# Set the timezone
ln -sf /usr/share/zoneinfo/{config.timezone} /etc/localtime
echo "{config.timezone}" > /etc/timezone
"""

def generate_keyboard_hook(config):
    return f"""#!/bin/bash
# Set the keyboard layout
cat > /etc/default/keyboard << KEYBOARD
XKBMODEL="pc105"
XKBLAYOUT="{config.keyboard_layout}"
XKBVARIANT=""
XKBOPTIONS=""
BACKSPACE="guess"
KEYBOARD
"""

def generate_autologin_hook(config):
    if not config.enable_autologin:
        return ""

    if config.display_manager == "gdm3":
        return """#!/bin/bash
# Configure GDM autologin
mkdir -p /etc/gdm3/
cat > /etc/gdm3/custom.conf << GDM
[daemon]
AutomaticLoginEnable=true
AutomaticLogin=live
GDM
"""
    elif config.display_manager == "lightdm":
        return """#!/bin/bash
# Configure LightDM autologin
mkdir -p /etc/lightdm/lightdm.conf.d/
cat > /etc/lightdm/lightdm.conf.d/50-autologin.conf << LIGHTDM
[Seat:*]
autologin-user=live
autologin-user-timeout=0
LIGHTDM
"""
    elif config.display_manager == "sddm":
        return """#!/bin/bash
# Configure SDDM autologin
mkdir -p /etc/sddm.conf.d/
cat > /etc/sddm.conf.d/autologin.conf << SDDM
[Autologin]
User=live
Session=plasma.desktop
SDDM
"""
    return ""

def generate_firewall_hook(config):
    if not config.enable_firewall:
        return ""

    firewall_script = """#!/bin/bash
# Configure firewall
ufw enable
ufw default deny incoming
ufw default allow outgoing"""

    if config.enable_ssh:
        firewall_script += """
ufw allow ssh"""

    firewall_script += "\n"
    return firewall_script

def generate_distro_info_hook(config):
    return f"""#!/bin/bash
# Update distro information in system files
echo "{config.distro_name}" > /etc/hostname
sed -i "s/debian/{config.distro_name}/g" /etc/hosts

# Set up the Desktop directory
mkdir -p /etc/skel/Desktop
chmod 755 /etc/skel/Desktop

# Create and configure the live user for the live session
if ! id -u live >/dev/null 2>&1; then
  useradd -m -s /bin/bash -G sudo live
fi
echo "live:live" | chpasswd
"""

def generate_package_fix_hook():
    return """#!/bin/bash
# Set a less strict apt configuration for building
cat > /etc/apt/apt.conf.d/99build-fixes << CONF
APT::Get::Fix-Missing "true";
APT::Get::Fix-Broken "true";
Acquire::Check-Valid-Until "false";
APT::Get::Assume-Yes "true";
Acquire::Retries "10";
CONF

# Make sure we have the latest package lists
apt-get update

# Try to fix any broken packages
apt-get -f install

# Pre-install critical packages to avoid download issues
apt-get install --no-install-recommends -y passwd gcc-12-base libc6 gnupg ca-certificates

# Create directory for package cache
mkdir -p /var/cache/apt/archives/partial
chmod 755 /var/cache/apt/archives/partial
"""

def generate_apt_config_hook():
    return """#!/bin/bash
# Set better apt configuration for the live system
echo 'Acquire::Retries "5";' > /etc/apt/apt.conf.d/80retries
echo 'APT::Install-Recommends "false";' > /etc/apt/apt.conf.d/80recommends

# Use more reliable mirrors
cat > /etc/apt/sources.list << SOURCES
deb http://deb.debian.org/debian bookworm main contrib non-free non-free-firmware
deb http://security.debian.org/debian-security bookworm-security main contrib non-free non-free-firmware
deb http://deb.debian.org/debian bookworm-updates main contrib non-free non-free-firmware
SOURCES

# Update package lists
apt-get update
"""
