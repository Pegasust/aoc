{
  description = "Python + Rust workspace for AoC";
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    rust-overlay.url = "github:oxalica/rust-overlay";
  };
  outputs = { nixpkgs, flake-utils, rust-overlay, ... } @ inputs:
    flake-utils.lib.eachSystem flake-utils.lib.defaultSystems (sys:
      let
        overlays = [ rust-overlay.overlays.default ];
        pkgs = import nixpkgs { system = sys; overlays = overlays; };
        shellHookAfter = ''
          echo "The input files should be placed under ./data/{submission,example}.txt"
          echo "This problem shares one input between two parts"
        '';
        py_pkgs = [ pkgs.python310 ];
        rs_pkgs = [
          pkgs.openssl
          pkgs.pkg-config

          # Add rust-src, which rust-analyzer seems to rely upon
          (pkgs.rust-bin.selectLatestNightlyWith
            (
              toolchain:
              toolchain.default.override {
                extensions = [ "rust-src" ];
              }
            ))
          # rust devex
          pkgs.bacon  # kinda like nodemon
          pkgs.rust-analyzer
        ];
      in
      {
        # Jack of all trades
        devShell = pkgs.mkShell
          {
            buildInputs = py_pkgs ++ rs_pkgs;
            shellHook = ''
              echo "> Default runtime. This contains both rust and python3 env"
              echo "Run ./run-py.sh for Python's output and ./run-rs.sh for Rust's output"
            '' + shellHookAfter;
          };
        devShells = {
          # nix develop ./#lua
          # lua = pkgs.mkShell {
          #   nativeBuildInputs = lua_pkgs;
          #   shellHook = ''
          #     echo "> Lua runtime"
          #     echo "Run ./run-lua.sh to see the output of the solution"
          #   '' + shellHookAfter;
          # };

          # nix develop ./#fennel

          # nix develop ./#python
          rust = pkgs.mkShell {
            nativeBuildInputs = rs_pkgs;
            shellHook = ''
              echo "> Rust runtime"
              echo "Run ./run-rs.sh to see output of the solution"
              echo "For quick feedback loop: bacon check-all"
            '' + shellHookAfter;
          };
          python = pkgs.mkShell {
            nativeBuildInputs = py_pkgs;
            shellHook = ''
              echo "> Python3 runtime"
              echo "Run ./run-py.sh to see the output of the solution"
            '' + shellHookAfter;

          };
        };
      }
    );
}
