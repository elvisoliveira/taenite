from src.constants import (
    DESKTOP_ENVIRONMENTS,
    DISPLAY_MANAGERS,
    COMMON_PACKAGES,
    DEV_TOOLS_PACKAGES
)

def generate_desktop_package_list(config):
    return "task-desktop"

def generate_desktop_env_package_list(config):
    desktop_packages = DESKTOP_ENVIRONMENTS.get(config.desktop_environment, "openbox")
    display_manager_packages = DISPLAY_MANAGERS.get(config.display_manager, "lightdm")
    return f"{desktop_packages} {display_manager_packages}"

def generate_common_package_list():
    return " ".join(COMMON_PACKAGES)

def generate_dev_tools_package_list(config):
    return " ".join(DEV_TOOLS_PACKAGES) if config.include_dev_tools else ""

def generate_ssh_package_list(config):
    return "openssh-server" if config.enable_ssh else ""

def generate_firewall_package_list(config):
    return "ufw gufw" if config.enable_firewall else ""

def generate_custom_package_list(config):
    return " ".join(config.packages)
