{
  description = "python shell flake";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = nixpkgs.legacyPackages.${system};
      in {
        devShells.default = pkgs.mkShell {
          venvDir = ".venv";
          packages = [pkgs.pyright pkgs.black] ++ (with pkgs.python3Packages; [pygame-ce pip venvShellHook]);

          postShellHook = ''
            pip install neat-python
            pip install pytest 
            pip install snakeviz
            # pip freeze  > requirements.txt
          '';
        };
      }
    );
}
