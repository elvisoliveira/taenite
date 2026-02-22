def generate_calamares_branding(config):
    return f"""---
componentName: {config.calamares_branding_short_product_name}
welcomeStyleCalamares: true
welcomeExpandingLogo: true
windowExpanding: normal
windowSize: 800px,520px
windowPlacement: center
sidebar: widget
navigation: widget

strings:
    productName:         "{config.calamares_branding_product_name}"
    shortProductName:    "{config.calamares_branding_short_product_name}"
    version:             "{config.calamares_branding_version}"
    shortVersion:        "{config.calamares_branding_short_version}"
    versionedName:       "{config.calamares_branding_product_name} {config.calamares_branding_version}"
    shortVersionedName:  "{config.calamares_branding_short_product_name} {config.calamares_branding_short_version}"
    bootloaderEntryName: "{config.calamares_branding_short_product_name}"
    productUrl:          "https://calamares.io/"
    supportUrl:          "https://github.com/calamares/calamares/wiki"
    knownIssuesUrl:      "https://github.com/calamares/calamares/issues"
    releaseNotesUrl:     "https://calamares.io/news/"
    donateUrl:           "https://kde.org/community/donations/"

images:
    productLogo:         "logo.png"
    productIcon:         "logo.png"
    productWelcome:      "welcome.png"

slideshow:               "show.qml"

style:
   SidebarBackground:    "#292F34"
   SidebarText:          "#FFFFFF"
   SidebarTextCurrent:   "#292F34"
   SidebarBackgroundCurrent: "#D35400"
"""
