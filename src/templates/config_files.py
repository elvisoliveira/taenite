def generate_custom_settings_desktop(config):
    return f"""[Desktop Entry]
Type=Application
Name=Custom Settings
Exec=sh -c 'sleep 10 && gsettings set org.gnome.desktop.background picture-uri file:///usr/share/backgrounds/custom-wallpaper.png && gsettings set org.gnome.desktop.background picture-uri-dark file:///usr/share/backgrounds/custom-wallpaper.png && gsettings set org.gnome.desktop.interface && gsettings set org.gnome.desktop.interface && gsettings set org.gnome.desktop.interface && gsettings set org.gnome.desktop.interface color-scheme prefer-dark'
Hidden=false
X-GNOME-Autostart-enabled=true
"""

def generate_os_release(config):
    distro_name_lower = config.distro_name.lower().replace(' ', '-')
    return f"""PRETTY_NAME="{config.distro_name} {config.distro_version}"
NAME="{config.distro_name}"
VERSION_ID="{config.distro_version}"
VERSION="{config.distro_version}"
VERSION_CODENAME="{config.distro_name.lower()}"
ID="{distro_name_lower}"
ID_LIKE="debian"
HOME_URL="https://www.debian.org/"
SUPPORT_URL="https://www.debian.org/support"
BUG_REPORT_URL="https://bugs.debian.org/"
"""

def generate_installer_desktop(config):
    return f"""[Desktop Entry]
Type=Application
Name=Install {config.distro_name}
GenericName=System Installer
Comment=Install {config.distro_name} on your computer
Exec=sudo calamares
Icon=/etc/calamares/branding/default/logo.png
Terminal=false
Categories=System;
StartupNotify=true
X-GNOME-UsesNotifications=true
"""
