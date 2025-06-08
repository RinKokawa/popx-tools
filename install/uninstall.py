import typer
import os
import shutil
from pathlib import Path

app = typer.Typer(help="卸载所有已安装组件")

USER_HOME = Path(os.environ["USERPROFILE"])
NVM_DIR = USER_HOME / "AppData" / "Local" / "nvm"
NODE_VERSION = "10.24.1"
NODE_DIR = NVM_DIR / f"v{NODE_VERSION}"
NODEJS_DIR = NVM_DIR / "nodejs"
NPM_POWERSHELL_PATHS = [
    NODEJS_DIR / "npm.ps1",
    NODEJS_DIR / "npm.ps1.bak"
]
SETTINGS_FILE = NVM_DIR / "settings.txt"

@app.command("all")
def uninstall_all():
    """
    卸载 nvm、node、npm 相关安装内容
    """
    # 删除 node 版本目录
    if NODE_DIR.exists():
        shutil.rmtree(NODE_DIR)
        typer.echo(f"🗑️ 已删除 Node 版本目录: {NODE_DIR}")

    # 删除 nodejs 软链接路径
    if NODEJS_DIR.exists():
        shutil.rmtree(NODEJS_DIR)
        typer.echo(f"🗑️ 已删除 nodejs 执行路径: {NODEJS_DIR}")

    # 删除 npm.ps1 拦截文件
    for ps1 in NPM_POWERSHELL_PATHS:
        if ps1.exists():
            ps1.unlink()
            typer.echo(f"🧹 已移除: {ps1}")

    # 清理 settings.txt 中的版本记录
    if SETTINGS_FILE.exists():
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            for line in lines:
                if NODE_VERSION not in line:
                    f.write(line)
        typer.echo("🧽 已清理 settings.txt 中的 node 记录")

    # 删除 nvm.exe（非强制）
    nvm_exe = NVM_DIR / "nvm.exe"
    if nvm_exe.exists():
        try:
            nvm_exe.unlink()
            typer.echo("🗑️ 已删除 nvm.exe")
        except PermissionError:
            typer.secho("⚠️ 无法删除 nvm.exe，可能在使用中", fg=typer.colors.YELLOW)

    typer.secho("✅ 卸载完成。建议手动检查路径是否清理干净。", fg=typer.colors.GREEN)
