import typer
import subprocess
import shutil
import tarfile
import os
from pathlib import Path

NPM_VERSION = "6.14.12"
TAR_NAME = f"npm-{NPM_VERSION}.tgz"
TAR_PATH = Path(__file__).parent / "bin" / TAR_NAME
EXTRACT_PATH = Path(os.environ["TEMP"]) / "npm-local-install"


def is_npm_installed():
    return shutil.which("npm") is not None


def install_npm():
    """
    安装本地 npm（v6.14.12）
    """
    if is_npm_installed():
        try:
            current_ver = subprocess.check_output(["npm", "-v"], text=True).strip()
            if current_ver == NPM_VERSION:
                typer.echo(f"✅ 已安装 npm@{NPM_VERSION}")
                return
            else:
                typer.echo(f"🔁 当前版本为 {current_ver}，尝试升级至 {NPM_VERSION}")
        except Exception:
            typer.echo("⚠️ 无法判断 npm 版本，继续执行安装。")

    if not TAR_PATH.exists():
        typer.secho(f"❌ 缺少本地 npm 安装包: {TAR_PATH}", fg=typer.colors.RED)
        return

    if EXTRACT_PATH.exists():
        shutil.rmtree(EXTRACT_PATH)
    EXTRACT_PATH.mkdir(parents=True, exist_ok=True)

    typer.echo("📂 正在解压 npm...")
    with tarfile.open(TAR_PATH, "r:gz") as tar:
        tar.extractall(path=EXTRACT_PATH)

    cli_path = EXTRACT_PATH / "package" / "bin" / "npm-cli.js"

    node_path = shutil.which("node")
    if not node_path:
        typer.secho("❌ 未检测到 node 命令，无法继续安装 npm。请先执行 `nvm use 10.24.1`。", fg=typer.colors.RED)
        return

    typer.echo("🚀 正在安装 npm...")
    subprocess.run([
        node_path, str(cli_path), "install", "-g", f"npm@{NPM_VERSION}",
        "--registry=https://registry.npmmirror.com"
    ], check=True)

    # 防止 PowerShell 拦截
    for npm_root in [
        Path("C:/nvm4w/nodejs"),
        Path.home() / "AppData/Local/nvm/nodejs"
    ]:
        ps1 = npm_root / "npm.ps1"
        if ps1.exists():
            ps1.rename(ps1.with_suffix(".ps1.bak"))
            typer.echo(f"✅ 已禁用 PowerShell 拦截文件: {ps1}")

    typer.echo("✅ npm 安装完成，请重新打开终端验证。")
