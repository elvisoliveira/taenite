from src.constants import (
    DESKTOP_ENVIRONMENTS,
    COMMON_PACKAGES,
    THEME_PACKAGES,
    DEV_TOOLS_PACKAGES,
    VM_TOOLS_PACKAGES,
    CODEC_PACKAGES,
    RESTRICTED_PACKAGES,
)


def generate_desktop_package_list(config):
    return "task-desktop"


def generate_desktop_env_package_list(config):
    return DESKTOP_ENVIRONMENTS.get(config.desktop_environment, "gnome gdm3")


def generate_common_package_list():
    return " ".join(COMMON_PACKAGES)


def generate_theme_package_list(config):
    packages = THEME_PACKAGES.copy()
    if config.icon_theme != "Adwaita":
        packages.append("papirus-icon-theme")
    return " ".join(packages)


def generate_dev_tools_package_list(config):
    if config.include_dev_tools:
        return " ".join(DEV_TOOLS_PACKAGES)
    return ""


def generate_vm_tools_package_list(config):
    if config.include_vm_support:
        return " ".join(VM_TOOLS_PACKAGES)
    return ""


def generate_codec_package_list(config):
    if config.include_codecs:
        return " ".join(CODEC_PACKAGES)
    return ""


def generate_restricted_package_list(config):
    if config.include_restricted:
        return " ".join(RESTRICTED_PACKAGES)
    return ""


def generate_flatpak_package_list(config):
    if config.enable_flatpak:
        return "flatpak gnome-software-plugin-flatpak"
    return ""


def generate_snap_package_list(config):
    if config.enable_snap:
        return "snapd"
    return ""


def generate_ssh_package_list(config):
    if config.enable_ssh:
        return "openssh-server"
    return ""


def generate_firewall_package_list(config):
    if config.enable_firewall:
        return "ufw gufw"
    return ""


def generate_installer_package_list():
    return "calamares calamares-settings-debian"


def generate_custom_package_list(config):
    return " ".join(config.packages)
