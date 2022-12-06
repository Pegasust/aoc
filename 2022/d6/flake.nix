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
          echo "The input files should be placed under ./data/{submission,example}.txt"
          echo "This problem shares one input between two parts"
        '';
        py_pkgs = [ pkgs.python310 ];
        # lua_pkgs = [ (pkgs.lua.withPackages (luapkgs: [ luapkgs.busted luapkgs.luafilesystem ])) ];
        fennel_pkgs = [ (pkgs.lua.withPackages (luapkgs: [ luapkgs.fennel luapkgs.readline ])) ];
      in
      {
        # Jack of all trades
        devShell = pkgs.mkShell {
          nativeBuildInputs = py_pkgs ++ fennel_pkgs;
          shellHook = ''
            echo "> Default runtime. This contains both fennel and python3 env"
            echo "Run ./run-py.sh for Python's output and ./run-fnl.sh for Fennel's output"
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
          fennel = pkgs.mkShell
            {
              nativeBuildInputs = fennel_pkgs;
              shellHook = ''
                echo "> Fennel runtime"
                echo "Run ./run-fnl.sh to see output of Fennel solution"
              '' + shellHookAfter;
            };

          # nix develop ./#python
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
