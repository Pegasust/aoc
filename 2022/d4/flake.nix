{
  description = "D4 AOC with Lua!";
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = { nixpkgs, flake-utils, ... } @ inputs:
    flake-utils.lib.eachSystem flake-utils.lib.defaultSystems (sys:
      let
        overlays = [ ];
        pkgs = import nixpkgs { system = sys; overlays = overlays; };
        shellHookAfter = ''
          echo "The input files should be placed under ./data/{submission,example}.txt
          echo "This problem only "
        '';
      in
      rec {
        devShell = devShell.lua;
        devShell.lua = lib.mkShell {
          nativeBuildInputs = [
            pkgs.lua.withPackages
            (luapkgs:
              [ luapkgs.busted luapkgs.luafilesystem ]
            )
          ];
          shellHook = ''
            echo "> Lua runtime"
            echo "Run ./run-lua.sh to see solution's output"
          '' + shellHookAfter;
        };
        devShell.python = lib.mkShell {
          nativeBuildInputs = [ pkgs.python3 ];
          shellHook = ''
            echo "> Python3 runtime"
            echo "Run ./run-py.sh to see solution's output"
          '' + shellHookAfter;

        };
      }
    );
}
