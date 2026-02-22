import os
import shutil
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("nanite")

from src.constants import (
    BUILD_DIRECTORIES,
    DEFAULT_LOGO_FILENAME,
    DEFAULT_WALLPAPER_FILENAME,
)
from src.templates.calamares import generate_calamares_branding
from src.templates.hooks import (
    generate_locale_timezone_hook,
    generate_keyboard_hook,
    generate_launcher_icon_hook,
    generate_sudo_hook,
    generate_polkit_hook,
    generate_distro_info_hook,
    generate_package_fix_hook,
    generate_apt_config_hook,
)
from src.templates.packages import (
    generate_desktop_package_list,
    generate_desktop_env_package_list,
    generate_common_package_list,
    generate_theme_package_list,
    generate_dev_tools_package_list,
    generate_vm_tools_package_list,
    generate_restricted_package_list,
    generate_flatpak_package_list,
    generate_snap_package_list,
    generate_ssh_package_list,
    generate_firewall_package_list,
    generate_installer_package_list,
    generate_custom_package_list,
)
from src.templates.config_files import (
    generate_gtk_settings,
    generate_custom_settings_desktop,
    generate_os_release,
    generate_installer_desktop,
)
from src.templates.live_build import (
    generate_debian_sources,
    generate_debian_preferences,
    generate_lb_config,
    generate_setup_script,
    generate_dockerfile,
)

class DockerManager:
    def __init__(self):
        self.temp_dir = None

    def _create_build_directories(self, base_dir):
        for directory in BUILD_DIRECTORIES:
            os.makedirs(os.path.join(base_dir, directory), exist_ok=True)

    def _copy_assets(self, config, build_dir):
        assets_dir = os.path.join(build_dir, "assets")

        if config.logo_path and os.path.exists(config.logo_path):
            shutil.copy(
                config.logo_path,
                os.path.join(assets_dir, DEFAULT_LOGO_FILENAME)
            )

        if config.wallpaper_path and os.path.exists(config.wallpaper_path):
            shutil.copy(
                config.wallpaper_path,
                os.path.join(assets_dir, DEFAULT_WALLPAPER_FILENAME)
            )

    def _write_calamares_branding(self, config, build_dir):
        branding_file = os.path.join(
            build_dir,
            "calamares",
            "branding.yaml"
        )
        with open(branding_file, "w") as f:
            f.write(generate_calamares_branding(config))

    def _write_package_lists(self, config, build_dir):
        package_lists_dir = os.path.join(build_dir, "config/package-lists")

        package_lists = {
            "installer.list.chroot": generate_installer_package_list(),
            "desktop.list.chroot": generate_desktop_package_list(config),
            "desktop-env.list.chroot": generate_desktop_env_package_list(config),
            "common.list.chroot": generate_common_package_list(),
            "themes.list.chroot": generate_theme_package_list(config),
            "custom.list.chroot": generate_custom_package_list(config),
        }

        optional_lists = {
            "dev-tools.list.chroot": generate_dev_tools_package_list(config),
            "vm-tools.list.chroot": generate_vm_tools_package_list(config),
            "restricted.list.chroot": generate_restricted_package_list(config),
            "flatpak.list.chroot": generate_flatpak_package_list(config),
            "snap.list.chroot": generate_snap_package_list(config),
            "ssh.list.chroot": generate_ssh_package_list(config),
            "firewall.list.chroot": generate_firewall_package_list(config),
        }

        for filename, content in package_lists.items():
            if content:
                with open(os.path.join(package_lists_dir, filename), "w") as f:
                    f.write(content)

        for filename, content in optional_lists.items():
            if content:
                with open(os.path.join(package_lists_dir, filename), "w") as f:
                    f.write(content)

    def _write_config_files(self, config, build_dir):
        includes_dir = os.path.join(build_dir, "config/includes.chroot")

        gtk3_settings = os.path.join(includes_dir, "etc/skel/.config/gtk-3.0/settings.ini")
        with open(gtk3_settings, "w") as f:
            f.write(generate_gtk_settings(config))

        gtk4_settings = os.path.join(includes_dir, "etc/skel/.config/gtk-4.0/settings.ini")
        shutil.copy(gtk3_settings, gtk4_settings)

        autostart_desktop = os.path.join(
            includes_dir,
            "etc/skel/.config/autostart/custom-settings.desktop"
        )
        with open(autostart_desktop, "w") as f:
            f.write(generate_custom_settings_desktop(config))

        os_release = os.path.join(includes_dir, "etc/os-release")
        with open(os_release, "w") as f:
            f.write(generate_os_release(config))

        installer_desktop = os.path.join(includes_dir, "etc/skel/Desktop/install.desktop")
        with open(installer_desktop, "w") as f:
            f.write(generate_installer_desktop(config))

        os.chmod(installer_desktop, 0o755)

    def _write_hooks(self, config, build_dir):
        hooks_dir = os.path.join(build_dir, "config/hooks/live")

        hooks = {
            "0020-configure-apt.hook.chroot": generate_apt_config_hook(),
            "0025-fix-package-issues.hook.chroot": generate_package_fix_hook(),
            "0050-configure-locale-timezone.hook.chroot": generate_locale_timezone_hook(config),
            "0051-configure-keyboard.hook.chroot": generate_keyboard_hook(config),
            "0060-create-launcher-icon.hook.chroot": generate_launcher_icon_hook(config),
            "0070-configure-sudo.hook.chroot": generate_sudo_hook(),
            "0080-configure-polkit.hook.chroot": generate_polkit_hook(),
            "0090-update-distro-info.hook.chroot": generate_distro_info_hook(config),
        }

        for filename, content in hooks.items():
            hook_file = os.path.join(hooks_dir, filename)
            with open(hook_file, "w") as f:
                f.write(content)
            os.chmod(hook_file, 0o755)

    def _write_apt_config(self, build_dir):
        archives_dir = os.path.join(build_dir, "config/archives")

        sources_file = os.path.join(archives_dir, "debian.list.chroot")
        with open(sources_file, "w") as f:
            f.write(generate_debian_sources())

        preferences_file = os.path.join(archives_dir, "debian.pref.chroot")
        with open(preferences_file, "w") as f:
            f.write(generate_debian_preferences())

    def _write_setup_script(self, config, build_dir):
        setup_file = os.path.join(build_dir, "setup.sh")
        with open(setup_file, "w") as f:
            f.write(generate_setup_script(config))
        os.chmod(setup_file, 0o755)

    def _write_dockerfile(self, config, build_dir):
        dockerfile = os.path.join(build_dir, "Dockerfile")
        with open(dockerfile, "w") as f:
            f.write(generate_dockerfile(config))

    def _create_build_context(self, config, output_dir="."):
        self.temp_dir = os.path.abspath(output_dir)
        logger.debug(f"Using build directory: {self.temp_dir}")

        self._create_build_directories(self.temp_dir)
        self._copy_assets(config, self.temp_dir)
        self._write_calamares_branding(config, self.temp_dir)
        self._write_package_lists(config, self.temp_dir)
        self._write_config_files(config, self.temp_dir)
        self._write_hooks(config, self.temp_dir)
        self._write_apt_config(self.temp_dir)
        self._write_setup_script(config, self.temp_dir)
        self._write_dockerfile(config, self.temp_dir)

        return self.temp_dir

    def start_build(self, config, callback, output_dir="."):
        logger.info("Generating build context files")
        try:
            build_dir = self._create_build_context(config, output_dir=output_dir)
            output_iso_dir = os.path.join(build_dir, "output")
            os.makedirs(output_iso_dir, exist_ok=True)
            image_name = f"{config.distro_name.lower().replace(' ', '-')}-builder"

            callback(f"Build context generated at: {build_dir}")
            callback("Run these commands manually:")
            callback(f"docker build -t {image_name} {build_dir}")
            callback(
                f"docker run --rm --privileged --network=host -v {output_iso_dir}:/build/output {image_name}"
            )
            callback(f"ISO output will be written to: {output_iso_dir}")
            return True
        except Exception as e:
            logger.error(f"Failed to generate build context: {e}")
            if callback:
                callback(f"ERROR: Failed to generate build context: {e}")
            return False
