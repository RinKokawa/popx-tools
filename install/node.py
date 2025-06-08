import typer
import subprocess
import os
import shutil
import zipfile
import winreg
from pathlib import Path

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


def write_node_path_env():
    """
    将 nvm\nodejs 添加到用户 PATH 环境变量
    """
    nodejs_path = str(NVM_DIR / "nodejs")
    current_path = os.environ.get("PATH", "")
    if nodejs_path in current_path:
        typer.echo("✅ PATH 已包含 nvm 的 nodejs 路径。")
        return

    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_SET_VALUE) as key:
        new_path = current_path + ";" + nodejs_path
        winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
        typer.echo(f"🔧 已添加 {nodejs_path} 到用户 PATH，请重启终端或执行 `refreshenv`。")


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

    if not ZIP_PATH.exists():
        typer.secho(f"❌ 缺少本地 Node 安装包: {ZIP_PATH}", fg=typer.colors.RED)
        return

    # 清除旧版本目录
    if VERSION_DIR.exists():
        typer.echo(f"🧹 正在删除旧版本目录 {VERSION_DIR} ...")
        shutil.rmtree(VERSION_DIR)

    # 解压到临时目录
    temp_extract_dir = NVM_DIR / f"temp-v{NODE_VERSION}"
    if temp_extract_dir.exists():
        shutil.rmtree(temp_extract_dir)
    temp_extract_dir.mkdir(parents=True)

    typer.echo(f"📦 正在解压 Node 至 {temp_extract_dir}")
    with zipfile.ZipFile(ZIP_PATH, "r") as zip_ref:
        zip_ref.extractall(temp_extract_dir)

    # 判断结构：是否多包一层
    extracted_root = next(temp_extract_dir.iterdir())
    source_dir = extracted_root if extracted_root.is_dir() else temp_extract_dir

    # 移动文件
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

    # 注册并启用
    typer.echo("🔁 正在注册并切换 Node 版本...")
    subprocess.run(f"nvm install {NODE_VERSION}", shell=True)
    subprocess.run(f"nvm use {NODE_VERSION}", shell=True)

    write_node_path_env()

    typer.echo("🧪 正在验证...")
    subprocess.run("node -v", shell=True)
    subprocess.run("npm -v", shell=True)
    typer.echo("✅ Node 安装完成！")


if __name__ == "__main__":
    app()
