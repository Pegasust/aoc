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
        ocamlPackager = pkgs.ocaml-ng.ocamlPackages_4_14;
        ocaml_pkgs = let inherit (ocamlPackager) ocaml findlib dune_2 ocaml-lsp; in
          [ ocaml findlib dune_2 ocaml-lsp ];
        ocaml_build_pkgs = [ ocamlPackager.ocamlgraph ];
      in
      {
        # Jack of all trades
        devShell = pkgs.mkShell
          {
            nativeBuildInputs = py_pkgs ++ ocaml_pkgs;
            shellHook = ''
              echo "> Default runtime. This contains both ocaml and python3 env"
              echo "Run ./run-py.sh for Python's output and ./run-oml.sh for OCaml's output"
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
          ocaml = pkgs.mkShell
            {
              nativeBuildInputs = ocaml_pkgs;
              shellHook = ''
                echo "> OCaml runtime"
                echo "Run ./run-oml.sh to see output of OCaml solution"
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
