DEFAULT_DEBIAN_MIRROR = "http://deb.debian.org/debian"
DEBIAN_SECURITY_MIRROR = "http://security.debian.org/debian-security"
DEBIAN_VERSION = "bookworm"

DEFAULT_LOGO_FILENAME = "logo.png"
DEFAULT_WALLPAPER_FILENAME = "wallpaper.png"

DEFAULT_PACKAGES = [
    "vim",
    "curl",
]

COMMON_PACKAGES = [
    "gparted",
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

RESTRICTED_PACKAGES = [
    "unrar",
    "libavcodec-extra",
    "libdvd-pkg",
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
    "assets",
    "calamares",
    "config/includes.chroot/etc/skel/",
    "config/includes.chroot/etc/skel/Desktop/",
    "config/includes.chroot/usr/share/backgrounds/",
    "config/includes.chroot/usr/share/icons/",
    "config/includes.chroot/etc/calamares/branding/default/",
    "config/hooks/live",
    "config/package-lists/",
    "config/archives",
]
