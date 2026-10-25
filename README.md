# EE347 Fall 2026 - Group 5 Lab Repository

## Getting Started

For a LateX IDE, [TeXstudio](https://www.texstudio.org/#download) is a good option.

## OpenSUSE

The following instructions detail how to install a LateX editing and compiling environment on OpenSUSE

### Install TexLive

TexLive is a set of tools to support compiling LateX into PDFs, among other things. There are a *lot* of different packages for TeXLive we could download.
This command installs the set of tools I needed to compile the report template. Yes, it's a lot of packages.

```sh
sudo zypper in texlive-scheme-medium
sudo zypper in texlive-draftwatermark texlive-draftwatermark-doc
```

Note that it is possible to use this to install significantly less packages.

```sh
sudo zypper in texlive-scheme-minimal
```

But you will need to install the missing dependencies yourself.

Example command to build Main.tex inside the report template into report.pdf inside a build dir:

```sh
cd tex/templates/report
mkdir build
pdflatex -jobname=report -output-directory=build Main.tex
```

Then, install TeXstudio

```sh
opi texstudio
```

## Collaboration

TeXstudio enables real time collaborative editing. This is done through [teamtype](https://github.com/teamtype/teamtype) integration.

The easiest method to install teamtype is to simply download a [release](https://github.com/teamtype/teamtype/releases). And place it somewhere in your PATH.

Another good option if you have `cargo` installed,

```sh
cargo install --locked teamtype
```

### Sharing a Session

Inside TeXstudio, go to tools -> start sharing folder and follow the prompt on screen. Once the prompt disappears,
at the bottom of the TeXstudio window is a status line. There is an icon that looks like two plugs joined. Hovering over it should reveal the access code, or right clicking it will copy the code to your clipboard.

### Joining a Session

Inside TeXStudio, go to tools -> Connect to other user for collaboration. It will prompt you for the access code. Enter the code and hit ok.
It will prompt you for where to place the collaboration folder. The default should be fine. You should now be connected to the other session. Updates will happen when you save.
