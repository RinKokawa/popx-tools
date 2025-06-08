import typer
import subprocess
import os
import shutil
from pathlib import Path
import zipfile

NODE_VERSION = "10.24.1"
ZIP_NAME = f"node-v{NODE_VERSION}-win-x64.zip"
NVM_DIR = Path(os.environ["USERPROFILE"]) / "AppData" / "Local" / "nvm"
VERSION_DIR = NVM_DIR / f"v{NODE_VERSION}"
ZIP_PATH = Path(__file__).parent / "bin" / ZIP_NAME


def is_node_installed():
    return shutil.which("node") is not None


def install_node():
    """
    安装本地 Node.js（v10.24.1），并用 nvm 切换
    """
    if is_node_installed():
        typer.echo("✅ 已检测到 node 命令，无需安装。")
        return

    if VERSION_DIR.exists() and (VERSION_DIR / "node.exe").exists():
        typer.echo("🔍 本地版本目录已存在，尝试切换 nvm use...")
        subprocess.run(f"nvm use {NODE_VERSION}", shell=True)
        typer.echo("✅ 已完成 node 切换。")
        return

    if not ZIP_PATH.exists():
        typer.secho(f"❌ 缺少本地 Node 安装包: {ZIP_PATH}", fg=typer.colors.RED)
        return

    typer.echo(f"📦 正在解压 Node 至 {VERSION_DIR}")
    VERSION_DIR.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ZIP_PATH, "r") as zip_ref:
        zip_ref.extractall(VERSION_DIR)

    typer.echo("🔁 注册版本并切换...")
    settings_path = NVM_DIR / "settings.txt"
    with open(settings_path, "a", encoding="utf-8") as f:
        f.write(f"\n{NODE_VERSION} 64")

    subprocess.run(f"nvm use {NODE_VERSION}", shell=True)
    typer.echo("✅ Node 安装完成并切换成功。")
