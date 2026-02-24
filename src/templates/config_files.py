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
