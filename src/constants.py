SUPPORTED_DESKTOPS = ["gnome", "kde", "xfce", "mate", "cinnamon"]

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
    "firefox-esr",
    "libreoffice",
    "vlc",
]

THEME_PACKAGES = [
    "gnome-themes-extra",
    "gtk2-engines-pixbuf",
    "gtk2-engines-murrine",
    "sassc",
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

VM_TOOLS_PACKAGES = [
    "open-vm-tools",
    "virtualbox-guest-x11",
    "spice-vdagent",
    "qemu-guest-agent",
]

RESTRICTED_PACKAGES = [
    "unrar",
    "libavcodec-extra",
    "libdvd-pkg",
]

DESKTOP_ENVIRONMENTS = {
    "gnome": "gnome gdm3",
    "kde": "kde-standard sddm",
    "xfce": "xfce4 xfce4-goodies lightdm",
    "mate": "mate-desktop-environment lightdm",
    "cinnamon": "cinnamon lightdm",
}

BUILD_DIRECTORIES = [
    "config",
    "assets",
    "calamares",
    "config/includes.chroot/etc/skel/",
    "config/includes.chroot/etc/skel/.config/autostart/",
    "config/includes.chroot/etc/skel/.config/gtk-3.0/",
    "config/includes.chroot/etc/skel/.config/gtk-4.0/",
    "config/includes.chroot/etc/skel/Desktop/",
    "config/includes.chroot/usr/share/backgrounds/",
    "config/includes.chroot/usr/share/icons/",
    "config/includes.chroot/etc/calamares/branding/default/",
    "config/hooks/live",
    "config/package-lists/",
    "config/archives",
]
