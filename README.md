# EE347 Fall 2026 - Group 5 Lab Repository

## Getting Started

For a Windows LateX environment, [TeXstudio](https://www.texstudio.org/#download) is a good option.

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

### Build TeXpresso

TeXpresso is a live viewer of LateX docs with good Neovim integrations. It must be built from source.

#### Install dependencies

There is no official OpenSUSE dependencies list, but we can look at the Fedora deps for a decent starting point.

The dependencies I needed are as follows. You may need more.

```bash
sudo zypper in sdl2-compat-devel libSDL2-2_0-0 clang clang23 clang-tools glibc-devel-static jbig2dec-devel \
libclang13 libclang-cpp23 libclang_rt23 libcmark-gfm0_29_0_gfm_13 libcmark-gfm-extensions0_29_0_gfm_13 \
lld lld23 llvm23-gold libopenssl-devel freetype2-devel freetype2-devel-2.14.3-1.2.x86_64 libjbig2dec0 \
openjpeg2-devel openjpeg2-devel-2.5.4-2.6.x86_64 mupdf mupdf-devel tesseract jbig2dec mujs leptonica-devel

opi gumbo-parser # or build it yourself
```

#### Clone the repo

```bash
git clone git@github.com:let-def/texpresso.git
```

#### Build and Install

Inside the cloned repo, do

```bash
make texpresso
make texpresso-xetex
```

Then copy output to somewhere in path, for example

```bash
cp build/texpresso ~/.local/bin/texpresso
cp build/texpresso-xetex ~/.local/bin/texpresso-xetex
```

#### Set up Neovim Plugin

##### Lazy.nvim

```lua
return {
  "let-def/texpresso.vim",
  config = function() require("texpresso").texpresso_path = "/home/will/.local/bin/texpresso" end,
}
```

#### Usage

in Neovim,

```neovim
:TeXpresso tex/templates/report/Main.tex
```
