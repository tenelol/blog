{
  description = "Development shell for the blog";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    hugo-nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05";
  };

  outputs =
    {
      self,
      nixpkgs,
      hugo-nixpkgs,
    }:
    let
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "aarch64-darwin"
      ];
      forAllSystems = f:
        nixpkgs.lib.genAttrs systems (
          system:
          f {
            pkgs = import nixpkgs { inherit system; };
            hugoPkgs = import hugo-nixpkgs { inherit system; };
          }
        );
    in
    {
      packages = forAllSystems (
        { pkgs, ... }:
        let
          blowfish-tools-real = pkgs.writeShellApplication {
            name = "blowfish-tools-real";
            runtimeInputs = [ pkgs.nodejs ];
            text = ''
              exec npx --yes blowfish-tools "$@"
            '';
          };
          blowfish-tools = pkgs.writeShellApplication {
            name = "blowfish-tools";
            runtimeInputs = [
              pkgs.bash
              blowfish-tools-real
            ];
            text = ''
              exec env BLOG_REPO_ROOT="$PWD" ${./scripts/blowfish-tools.sh} "$@"
            '';
          };
        in
        {
          default = blowfish-tools;
        }
      );

      devShells = forAllSystems (
        { pkgs, hugoPkgs }:
        let
          blowfish-tools = self.packages.${pkgs.stdenv.hostPlatform.system}.default;
        in
        {
          default = pkgs.mkShell {
            packages = [
              hugoPkgs.hugo
              pkgs.nodejs
              blowfish-tools
            ];

            shellHook = ''
              export npm_config_cache="$PWD/.npm-cache"
              mkdir -p "$npm_config_cache"

              echo "devShell ready: hugo, blowfish-tools"
            '';
          };
        }
      );
    };
}
