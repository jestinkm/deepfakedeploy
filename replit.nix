{ pkgs }: {
  deps = [
    pkgs.python310
    pkgs.python310Packages.flask
    pkgs.python310Packages.flask-cors
    pkgs.python310Packages.numpy
    pkgs.opencv
    pkgs.cmake
    pkgs.pkg-config
    pkgs.xorg.libX11
    pkgs.xorg.libXext
    pkgs.xorg.libXcursor
    pkgs.xorg.libXi
    pkgs.xorg.libXrandr
    pkgs.xorg.libXinerama
    pkgs.xorg.libXxf86vm
    pkgs.libGL
    pkgs.glib
    pkgs.gdk-pixbuf
    pkgs.cairo
    pkgs.pango
    pkgs.atk
    pkgs.gtk3
    pkgs.boost
    pkgs.dlib
  ];
}
