import typer
import subprocess
import os
import shutil
from pathlib import Path
import zipfile

app = typer.Typer()

# 配置
NODE_VERSION = "10.24.1"
ZIP_NAME = f"node-v{NODE_VERSION}-win-x64.zip"
NVM_DIR = Path(os.environ["USERPROFILE"]) / "AppData" / "Local" / "nvm"
VERSION_DIR = NVM_DIR / f"v{NODE_VERSION}"
ZIP_PATH = Path(__file__).parent / "bin" / ZIP_NAME


def is_node_installed():
    return shutil.which("node") is not None


def is_nvm_available():
    return shutil.which("nvm") is not None


@app.command("install")
def install_node():
    """
    安装本地 Node.js（v10.24.1），并用 nvm 注册切换。
    """
    typer.echo(f"📂 nvm 安装目录：{NVM_DIR}")
    typer.echo(f"🎯 Node 版本：{NODE_VERSION}")

    if not is_nvm_available():
        typer.secho("❌ 未检测到 nvm 命令，请先安装 nvm。", fg=typer.colors.RED)
        return

    if is_node_installed():
        typer.echo("✅ 已检测到 node 命令，无需安装。")
        return

    if VERSION_DIR.exists() and (VERSION_DIR / "node.exe").exists():
        typer.echo("🔍 本地版本目录已存在，尝试执行 nvm use...")
        subprocess.run(f"nvm use {NODE_VERSION}", shell=True)
        typer.echo("✅ Node 已切换。")
        return

    if not ZIP_PATH.exists():
        typer.secho(f"❌ 缺少本地 Node 安装包: {ZIP_PATH}", fg=typer.colors.RED)
        return

    # 1. 解压到临时目录
    temp_extract_dir = NVM_DIR / f"temp-v{NODE_VERSION}"
    if temp_extract_dir.exists():
        shutil.rmtree(temp_extract_dir)
    temp_extract_dir.mkdir(parents=True)

    typer.echo(f"📦 正在解压 Node 至临时目录 {temp_extract_dir}")
    with zipfile.ZipFile(ZIP_PATH, "r") as zip_ref:
        zip_ref.extractall(temp_extract_dir)

    # 2. 复制文件到目标版本目录
    VERSION_DIR.mkdir(parents=True, exist_ok=True)
    for file in temp_extract_dir.iterdir():
        shutil.move(str(file), str(VERSION_DIR))

    # 3. 删除临时目录
    shutil.rmtree(temp_extract_dir)

    # 4. 注册并启用该版本
    typer.echo("🔁 使用 nvm 注册版本并切换...")
    subprocess.run(f"nvm install {NODE_VERSION}", shell=True)
    subprocess.run(f"nvm use {NODE_VERSION}", shell=True)

    # 5. 测试是否成功
    typer.echo("🧪 验证安装：")
    subprocess.run("node -v", shell=True)
    subprocess.run("npm -v", shell=True)
    typer.echo("✅ Node 安装并激活成功。")


if __name__ == "__main__":
    app()
