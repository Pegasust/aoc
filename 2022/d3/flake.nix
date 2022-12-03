{
  description = "Typescript and Deno";
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachSystem flake-utils.lib.defaultSystems (sys:
      let pkgs = import nixpkgs { system = sys; }; in
      {
        devShell = pkgs.mkShell {
          nativeBuildInputs = [
            pkgs.bashInteractive
            pkgs.deno
          ];
          shellHook = ''
            echo "Testing deno's installed version:"
            deno --version
          '';
        };
      }
    );
}
