# Hugo Simple Sections Theme

- [Features](#features)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Configuration](#configuration)
- [Content](#content)
  - [Section index](#section-index)
  - [Files inside section folder](#files-inside-section-folder)
- [Instagram feed](#instagram-feed)
- [Shortcodes](#shortcodes)
- [Sites using hugo-landing-sections](#sites-using-hugo-landing-sections)
- [Contribution](#contribution)
- [Donations](#donations)

## Features

Hugo Simple Sections is a simple Hugo theme for creating organizations landing pages
with a few sections. It is a simple and clean theme.

Main features:

- Responsive
- Supports Instagram feed
- Uses Bootstrap

## Screenshots

Main page

[![Main
page](https://codeberg.org/VaDeCodiNet/hugo-simple-sections/raw/branch/main/images/main-page.png
"Main
page")](https://codeberg.org/VaDeCodiNet/hugo-simple-sections/raw/branch/main/images/main-page-big.png)

Section page

[![Section
page](https://codeberg.org/VaDeCodiNet/hugo-simple-sections/raw/branch/main/images/section-page.png
"Section
page")](https://codeberg.org/VaDeCodiNet/hugo-simple-sections/raw/branch/main/images/section-page-big.png)

Menu

[![Section
page](https://codeberg.org/VaDeCodiNet/hugo-simple-sections/raw/branch/main/images/menu.png
"Section
page")](https://codeberg.org/VaDeCodiNet/hugo-simple-sections/raw/branch/main/images/menu-big.png)

Small devices

[![Section
page](https://codeberg.org/VaDeCodiNet/hugo-simple-sections/raw/branch/main/images/small-devices.png
"Section
page")](https://codeberg.org/VaDeCodiNet/hugo-simple-sections/raw/branch/main/images/small-devices-big.png)

## Installation

The easiest way to install `hugo-simple-sections` is to make example site work
and then configure and write your own configs and content. You have two options
depending if you want to use git submodules or not.

1. Use git submodules

    ```bash
    mkdir -p mysite/themes
    cd mysite
    git init
    cd themes
    git submodule add https://codeberg.org/VaDeCodiNet/hugo-simple-sections.git
    cd ..
    cp -r themes/hugo-simple-sections/exampleSite/* .
    npm install
    hugo server
    ```

1. Do not use git submodules (clone the theme)

    ```bash
    mkdir -p mysite/themes
    cd mysite/themes
    git clone https://codeberg.org/VaDeCodiNet/hugo-simple-sections.git
    cd ..
    cp -r themes/hugo-simple-sections/exampleSite/* .
    npm install
    hugo server
    ```

## Configuration

| Parameter          | Description                                    | Type    | Default       |
| ------------------ | -----------------------------------------------| --------| --------------|
| banner             | Banner image file name                         | string  | 'banner.png'  |
| email              | Contact email                                  | string  | ''            |
| favicon            | Favicon icon                                   | string  | 'favicon.ico' |
| instagram.enabled  | Show/hide Instagram feed and instagram contact | boolean | False         |
| instagram.tokenURL | URL with your Instagram profile token          | string  | ''            |
| instagram.url      | URL with your instagram profile                | boolean | False         |
| logo               | Logo image file name                           | string  | 'logo.png'    |
| style.brandColor1  | Menu links background color                    | string  | '#1f1f26'   |
| style.brandColor2  | Menu background and footer background color    | string  | '#43AA60'   |
| style.brandColor3  | Menu and footer text color                     | string  | '#ffffff'   |

## Content

Each section is a subfolder in `content/pages`. In each section you will have an
`index.md`file with no content but configurations in matter and a file for each
info you want to have in the corresponding section page.

### Section index

In each section `index.md` file will specify the section name, the icon that
will appear in main page, its colors, how many columns the section page will
have and if it is big content (in this case, top margin will be smaller). Icons
are bootstrap icons, you can find icon names at
<https://icons.getbootstrap.com/>

Front matter example:

```yaml
---
title: Section 1
weight: 10
cols: 3
icon: question-circle
iconColor: "#ffffff"
iconBgColor: "#000000"
bigContent: True
---
```

### Files inside section folder

In each section, you will have as files as you need with section folder. These
files will be different subsections in section page.

Front matter example:

```yaml
---
title: Info 1
weight: 10
---
```

## Instagram feed

`hugo-simple-sections` uses [Instafeed.js](https://instafeedjs.com/) to load
your Instagram feed. To make your Instagram feed work, you should have a service
that provides an Instagram access token. An open source implementation of this
service is
[instatokend](https://github.com/jasper-clarke/instatoken-refreshers/tree/instatokend).

You have more information about instagram tokens here:
<https://instafeedjs.com/#/tokens>

## Shortcodes

You can use the following shortcodes in your content:

| Shortcode | Parameters       | Description      | Example                                                |
| --------- | -----------------| ---------------- | ------------------------------------------------------ |
| iframe    | URL width height | Insert an iframe | `{{< iframe "https://example.com" "100%" "1000px" >}}` |

## Sites using hugo-landing-sections

- <https://afaildefonscerda.cat> ([Source code](https://codeberg.org/VaDeCodiNet/afaildefonscerda.cat))

## Contribution

All contributions are always welcome! Create issues and MRs and we will review
them with pleasure :-)

## Donations

We accept donation to maintain this theme via LiberaPay.

[![LiberaPay donation logo](https://liberapay.com/assets/widgets/donate.svg)](https://liberapay.com/vadecodi/donate)
