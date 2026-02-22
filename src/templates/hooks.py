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


def generate_launcher_icon_hook(config):
    return f"""#!/bin/bash
# Create a desktop launcher with a larger icon for Calamares
mkdir -p /etc/skel/Desktop
cat > /etc/skel/Desktop/install-{config.distro_name}.desktop << DESKTOP
[Desktop Entry]
Type=Application
Name=Install {config.distro_name}
GenericName=System Installer
Comment=Install {config.distro_name} on your computer
Exec=sudo calamares
Icon=/etc/calamares/branding/default/logo.png
Terminal=false
Categories=System;Qt;
Keywords=calamares;system;installer;
StartupNotify=true
X-GNOME-UsesNotifications=true
DESKTOP

# Make the launcher executable
chmod +x /etc/skel/Desktop/install-{config.distro_name}.desktop
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

# Configure autologin if enabled
if [ "{str(config.enable_autologin).lower()}" = "true" ]; then
  if [ -d /etc/gdm3 ]; then
    # Configure GDM autologin
    mkdir -p /etc/gdm3/
    cat > /etc/gdm3/custom.conf << GDM
[daemon]
AutomaticLoginEnable=true
AutomaticLogin=live
GDM
  elif [ -d /etc/lightdm ]; then
    # Configure LightDM autologin
    mkdir -p /etc/lightdm/
    cat > /etc/lightdm/lightdm.conf << LIGHTDM
[SeatDefaults]
autologin-user=live
autologin-user-timeout=0
LIGHTDM
  elif [ -d /etc/sddm.conf.d ]; then
    # Configure SDDM autologin
    mkdir -p /etc/sddm.conf.d/
    cat > /etc/sddm.conf.d/autologin.conf << SDDM
[Autologin]
User=live
Session=plasma.desktop
SDDM
  fi
fi

# Configure firewall if enabled
if [ "{str(config.enable_firewall).lower()}" = "true" ]; then
  ufw enable
  ufw default deny incoming
  ufw default allow outgoing
  if [ "{str(config.enable_ssh).lower()}" = "true" ]; then
    ufw allow ssh
  fi
fi
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
