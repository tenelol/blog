{
  description = "Development shell for the blog";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs =
    { self, nixpkgs }:
    let
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];
      forAllSystems = f:
        nixpkgs.lib.genAttrs systems (
          system:
          f {
            pkgs = import nixpkgs { inherit system; };
          }
        );
    in
    {
      packages = forAllSystems (
        { pkgs }:
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
        { pkgs }:
        let
          blowfish-tools = self.packages.${pkgs.stdenv.hostPlatform.system}.default;
        in
        {
          default = pkgs.mkShell {
            packages = [
              pkgs.hugo
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
