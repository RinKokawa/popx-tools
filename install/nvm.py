import requests
from tqdm import tqdm
import typer
import os
import subprocess
from importlib.resources import files
from pathlib import Path
import shutil

app = typer.Typer()

NVM_DIR = Path(os.environ["USERPROFILE"]) / "AppData" / "Local" / "nvm"
NVM_EXE = NVM_DIR / "nvm.exe"
NODEJS_DIR = NVM_DIR / "nodejs"


def is_nvm_available():
    return shutil.which("nvm") is not None


def write_path_env():
    """确保 nvm 和 nodejs 路径已写入 PATH（用户环境变量）"""
    current = os.environ.get("PATH", "")
    parts = current.split(";")
    updated = False

    paths_to_add = [str(NVM_DIR), str(NODEJS_DIR)]
    for p in paths_to_add:
        if p not in parts:
            parts.append(p)
            updated = True

    if updated:
        new_path = ";".join(parts)
        # 修改用户环境变量（永久生效）
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
        typer.echo("🔧 已将 nvm 相关路径添加到用户 PATH 环境变量。")
    else:
        typer.echo("✅ PATH 中已包含 nvm 路径，无需修改。")


@app.command("install-nvm")
def install_nvm():
    """
    自动检测并安装 nvm，如果已存在则自动修复环境变量。
    """
    if is_nvm_available():
        typer.echo("✅ 已检测到 nvm 命令可用，无需安装。")
        return

    if NVM_EXE.exists():
        typer.echo("🔍 检测到本地存在 nvm.exe，但未加入 PATH，正在修复...")
        write_path_env()
        typer.echo("✅ 修复完成，请重新打开终端后再试。")
        return

    typer.echo("📦 未检测到 nvm，开始下载安装...")

    url = "https://github.com/coreybutler/nvm-windows/releases/latest/download/nvm-setup.exe"
    temp_path = os.path.join(os.environ["TEMP"], "nvm-setup.exe")
    typer.echo("🔽 正在尝试从 GitHub 下载 nvm 安装程序...")

    try:
        with requests.get(url, stream=True, timeout=30) as r:
            r.raise_for_status()
            total = int(r.headers.get('Content-Length', 0))
            with open(temp_path, 'wb') as f, tqdm(
                total=total, unit='B', unit_scale=True, desc="📦 下载进度"
            ) as bar:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        bar.update(len(chunk))

        typer.echo("✅ 下载完成，启动安装程序...")
        typer.echo("✅ 安装时请确保勾选“Add to PATH”。")
        subprocess.Popen([temp_path], shell=True)

    except Exception as e:
        typer.echo(f"❌ 下载失败: {e}")
        typer.echo("👉 正在尝试使用内置安装包继续安装...")
        install_nvm_local()


@app.command("install-nvm-local")
def install_nvm_local():
    """
    使用内置安装器安装 nvm。
    """
    try:
        resource = files("install.bin").joinpath("nvm-setup.exe")
        fallback_path = Path(os.environ["TEMP"]) / "nvm-setup-fallback.exe"

        with resource.open("rb") as src, open(fallback_path, "wb") as dst:
            dst.write(src.read())

        typer.echo("✅ 内置安装包已准备，启动安装程序...")
        typer.echo("✅ 安装时请确保勾选“Add to PATH”。")
        subprocess.Popen([str(fallback_path)], shell=True)

    except Exception as fallback_error:
        typer.echo(f"❌ 内置安装失败: {fallback_error}")
        typer.echo("👉 手动下载地址：https://github.com/coreybutler/nvm-windows/releases")


if __name__ == "__main__":
    app()
