import yaml
import json
from dataclasses import dataclass, field

@dataclass
class BuildConfig:
    distro_name: str = "TaeniteOS"
    distro_version: str = "1.0"
    desktop_environment: str = "openbox"
    display_manager: str = "lightdm"

    calamares_branding_product_name: str = "TaeniteOS"
    calamares_branding_short_product_name: str = "Taenite"
    calamares_branding_version: str = "1.0"
    calamares_branding_short_version: str = "1.0"

    logo_path: str = ""
    wallpaper_path: str = ""

    timezone: str = "UTC"
    locale: str = "en_US.UTF-8"
    keyboard_layout: str = "us"
    hostname_prefix: str = "taenite"

    enable_autologin: bool = True
    enable_firewall: bool = False
    enable_ssh: bool = False

    boot_quiet: bool = True
    boot_splash: bool = True

    packages: list = field(default_factory=lambda: ["vim", "curl"])

    include_dev_tools: bool = False
    include_restricted: bool = False

    @classmethod
    def from_yaml_file(cls, config_path="config.yaml"):
        with open(config_path, "r", encoding="utf-8") as handle:
            raw = handle.read()

        try:
            data = yaml.safe_load(raw) or {}
        except Exception:
            data = json.loads(raw)

        if not isinstance(data, dict):
            raise ValueError("Config root must be a mapping/object")

        allowed = set(cls.__dataclass_fields__.keys())
        filtered = {k: v for k, v in data.items() if k in allowed}

        packages = filtered.get("packages")
        if isinstance(packages, str):
            filtered["packages"] = [p for p in packages.split() if p]

        return cls(**filtered)
