DEFAULT_DEBIAN_MIRROR = "http://deb.debian.org/debian"
DEBIAN_SECURITY_MIRROR = "http://security.debian.org/debian-security"
DEBIAN_VERSION = "bookworm"

COMMON_PACKAGES = [
    "sudo",
    "zstd",
    "squashfs-tools",
    "debian-installer-launcher"
]

DEV_TOOLS_PACKAGES = [
    "build-essential",
    "git",
    "gcc",
    "g++",
    "make",
    "cmake",
    "autoconf",
    "automake",
    "pkg-config",
]

DESKTOP_ENVIRONMENTS = {
    "gnome": "gnome",
    "kde": "kde-standard",
    "xfce": "xfce4 xfce4-goodies",
    "mate": "mate-desktop-environment",
    "cinnamon": "cinnamon",
    "openbox": "openbox",
}

DISPLAY_MANAGERS = {
    "gdm3": "gdm3",
    "sddm": "sddm",
    "lightdm": "lightdm",
}

BUILD_DIRECTORIES = [
    "config",
    "config/includes.chroot/etc/skel/",
    "config/includes.chroot/etc/skel/Desktop/",
    "config/hooks/live",
    "config/package-lists/",
    "config/archives",
]
