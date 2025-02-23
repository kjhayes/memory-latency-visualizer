(use-modules (guix)
             (guix packages)
             (gnu packages)
             (gnu packages base)
             (gnu packages bash)
             (gnu packages build-tools)
             (gnu packages commencement)
             (gnu packages compression)
             (gnu packages gawk)
             (gnu packages gcc)
             (gnu packages llvm)
             (gnu packages moreutils)
             (gnu packages ncurses)
             (gnu packages python)
             (gnu packages python-science)
             (gnu packages python-xyz))

(packages->manifest
 (list gcc-toolchain
       gnu-make
       coreutils moreutils binutils
       findutils
       ;; Some scripts expect to have various locale environment variables set
       ;; For example, LC_COLLATE=en_US
       glibc-locales
       ncurses sed diffutils gawk grep
       ;; General scripting
       bash
       ;; Python
       python
       python-lsp-server
       python-rope
       python-black
       python-flake8
       python-networkx
       python-progress
       python-matplotlib
       python-seaborn
       python-numpy
       python-pandas python-pandas-stubs))
