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

def generate_sudo_hook():
    return """#!/bin/bash
# Configure sudo for the live user (no password for calamares)
mkdir -p /etc/sudoers.d/
cat > /etc/sudoers.d/live-user << EOF
# Allow live user to run specific commands without password
live ALL=(ALL) NOPASSWD: /usr/bin/calamares
EOF
chmod 440 /etc/sudoers.d/live-user
"""

def generate_polkit_hook():
    return """#!/bin/bash
# Create PolicyKit rule for calamares
mkdir -p /etc/polkit-1/localauthority/50-local.d/
cat > /etc/polkit-1/localauthority/50-local.d/99-live-user-calamares.pkla << EOF
[Allow live user to run Calamares]
Identity=unix-user:live
Action=org.kde.calamares.pkexec.run
ResultAny=yes
ResultInactive=yes
ResultActive=yes
EOF

# Create PolicyKit file for Calamares
mkdir -p /usr/share/polkit-1/actions/
cat > /usr/share/polkit-1/actions/org.kde.calamares.pkexec.policy << EOL
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE policyconfig PUBLIC
 "-//freedesktop//DTD PolicyKit Policy Configuration 1.0//EN"
 "http://www.freedesktop.org/standards/PolicyKit/1/policyconfig.dtd">
<policyconfig>
  <action id="org.kde.calamares.pkexec.run">
    <description>Run Calamares Installer</description>
    <message>Authentication is required to install the system</message>
    <icon_name>calamares</icon_name>
    <defaults>
      <allow_any>auth_admin</allow_any>
      <allow_inactive>auth_admin</allow_inactive>
      <allow_active>auth_admin</allow_active>
    </defaults>
    <annotate key="org.freedesktop.policykit.exec.path">/usr/bin/calamares</annotate>
    <annotate key="org.freedesktop.policykit.exec.allow_gui">true</annotate>
  </action>
</policyconfig>
EOL

# Create direct launcher for Calamares (alternative method)
cat > /usr/local/bin/install-system << EOL
#!/bin/bash
pkexec calamares
EOL
chmod +x /usr/local/bin/install-system
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

# Set a known password for the live user (for Calamares)
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
