import typer
import os
import subprocess
from pathlib import Path
import shutil
from importlib.resources import files

app = typer.Typer()

NVM_DIR = Path(os.environ["USERPROFILE"]) / "AppData" / "Local" / "nvm"
NVM_EXE = NVM_DIR / "nvm.exe"
NODEJS_DIR = NVM_DIR / "nodejs"
LOCAL_INSTALLER = files("install.bin").joinpath("nvm-setup.exe")  # 本地 bin 中的安装器路径


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
    自动检测并安装 nvm（默认使用内置安装器）。
    """
    if is_nvm_available():
        typer.echo("✅ 已检测到 nvm 命令可用，无需安装。")
        return

    if NVM_EXE.exists():
        typer.echo("🔍 检测到本地存在 nvm.exe，但未加入 PATH，正在修复...")
        write_path_env()
        typer.echo("✅ 修复完成，请重新打开终端后再试。")
        return

    # 改为本地安装器
    typer.echo("📦 开始使用本地安装器安装 nvm...")
    try:
        fallback_path = Path(os.environ["TEMP"]) / "nvm-setup-fallback.exe"
        with LOCAL_INSTALLER.open("rb") as src, open(fallback_path, "wb") as dst:
            dst.write(src.read())

        typer.echo("✅ 本地安装器已准备，启动安装程序...")
        subprocess.Popen([str(fallback_path)], shell=True)

    except Exception as fallback_error:
        typer.secho(f"❌ 启动本地安装失败: {fallback_error}", fg=typer.colors.RED)
        typer.echo("👉 请确认 install/bin/nvm-setup.exe 是否存在。")


if __name__ == "__main__":
    app()
