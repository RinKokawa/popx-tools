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
    强制离线安装本地 Node.js（v10.24.1），若存在旧目录则覆盖。
    """
    typer.echo(f"📂 nvm 安装目录：{NVM_DIR}")
    typer.echo(f"🎯 Node 版本：{NODE_VERSION}")

    if not is_nvm_available():
        typer.secho("❌ 未检测到 nvm 命令，请先安装 nvm。", fg=typer.colors.RED)
        return

    if is_node_installed():
        typer.echo("🔍 已检测到 node 命令，但将强制重新安装。")

    if not ZIP_PATH.exists():
        typer.secho(f"❌ 缺少本地 Node 安装包: {ZIP_PATH}", fg=typer.colors.RED)
        return

    # 清除已存在的 node 版本目录（软链或旧安装）
    if VERSION_DIR.exists():
        typer.echo(f"🧹 正在删除已存在的版本目录 {VERSION_DIR} ...")
        shutil.rmtree(VERSION_DIR)

    # 1. 解压 zip 到临时目录
    temp_extract_dir = NVM_DIR / f"temp-v{NODE_VERSION}"
    if temp_extract_dir.exists():
        shutil.rmtree(temp_extract_dir)
    temp_extract_dir.mkdir(parents=True)

    typer.echo(f"📦 正在解压 Node 至临时目录 {temp_extract_dir}")
    with zipfile.ZipFile(ZIP_PATH, "r") as zip_ref:
        zip_ref.extractall(temp_extract_dir)

    # 2. 处理 zip 解压目录结构（是否多包一层）
    extracted_root = next(temp_extract_dir.iterdir())
    if extracted_root.is_dir() and "node.exe" in [f.name for f in extracted_root.iterdir()]:
        source_dir = extracted_root  # 多包一层
    else:
        source_dir = temp_extract_dir  # 无包装

    # 3. 移动到版本目录
    VERSION_DIR.mkdir(parents=True, exist_ok=True)
    for item in source_dir.iterdir():
        target_path = VERSION_DIR / item.name
        if target_path.exists():
            if target_path.is_dir():
                shutil.rmtree(target_path)
            else:
                target_path.unlink()
        shutil.move(str(item), str(target_path))

    shutil.rmtree(temp_extract_dir)

    # 4. 注册并使用
    typer.echo("🔁 使用 nvm 注册版本并切换...")
    subprocess.run(f"nvm install {NODE_VERSION}", shell=True)
    subprocess.run(f"nvm use {NODE_VERSION}", shell=True)

    # 5. 测试结果
    typer.echo("🧪 验证安装：")
    subprocess.run("node -v", shell=True)
    subprocess.run("npm -v", shell=True)
    typer.echo("✅ Node 安装并激活成功。")

if __name__ == "__main__":
    app()
