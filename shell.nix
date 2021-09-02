with import <nixpkgs> {};
let
  pythonEnv = python38.withPackages (ps: [
    ps.pip
    ps.virtualenv
  ]);
in mkShell {
  packages = [
    pythonEnv

    black
    mypy

    wkhtmltopdf
  ];
}