{ pkgs, ... }: {
  channel = "stable-24.05";
  packages = [
    pkgs.python311
    pkgs.sqlite
    pkgs.python311Packages.pip
    pkgs.python311Packages.pytest
  ];
  env = {};
  idx = {
    extensions = [
      "google.gemini-cli-vscode-ide-companion"
      "ms-azuretools.vscode-sqlite"
      "ms-python.debugpy"
      "ms-python.python"
    ];
    previews = {
      enable = true;
      previews = {
        web = {
          command = ["uvicorn" "main:app" "--host" "0.0.0.0" "--port" "$PORT"];
          manager = "web";
        };
      };
    };
    workspace = {
      onCreate = {
        install-deps = "pip install -r requirements.txt";
      };
      onStart = {
        "start-server" = "uvicorn main:app --host 0.0.0.0 --port $PORT";
      };
    };
  };
}
