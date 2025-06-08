import typer
import subprocess
import shutil
import tarfile
import os
import sys
from pathlib import Path

app = typer.Typer()

# 配置
NPM_VERSION = "6.14.12"
TAR_NAME = f"npm-{NPM_VERSION}.tgz"
TAR_PATH = Path(__file__).parent / "bin" / TAR_NAME
EXTRACT_PATH = Path(os.environ["TEMP"]) / "npm-local-install"


def is_npm_installed():
    return shutil.which("npm") is not None


@app.command("npm")
def install_npm():
    """
    离线安装本地 npm（v6.14.12），不联网拉取。
    """
    typer.echo(f"📦 安装包路径: {TAR_PATH}")
    if not TAR_PATH.exists():
        typer.secho(f"❌ 缺少 npm 包: {TAR_PATH}", fg=typer.colors.RED)
        return

    if is_npm_installed():
        try:
            current_ver = subprocess.check_output(["npm", "-v"], text=True).strip()
            if current_ver == NPM_VERSION:
                typer.echo(f"✅ 已安装 npm@{NPM_VERSION}")
                return
            else:
                typer.echo(f"🔁 当前 npm 为 {current_ver}，尝试覆盖安装为 {NPM_VERSION}")
        except Exception:
            typer.echo("⚠️ 无法判断版本，强制安装")

    if EXTRACT_PATH.exists():
        shutil.rmtree(EXTRACT_PATH)
    EXTRACT_PATH.mkdir(parents=True)

    typer.echo("📂 正在解压 npm 安装包...")
    with tarfile.open(TAR_PATH, "r:gz") as tar:
        tar.extractall(EXTRACT_PATH)

    npm_package_path = EXTRACT_PATH / "package"
    if not npm_package_path.exists():
        typer.secho("❌ 解压失败：未找到 package/ 目录", fg=typer.colors.RED)
        return

    node_path = shutil.which("node")
    if not node_path:
        typer.secho("❌ 未检测到 node，请先执行 `nvm use`。", fg=typer.colors.RED)
        return

    node_dir = Path(node_path).parent
    typer.echo(f"📁 Node 安装目录：{node_dir}")

    target_modules = node_dir / "node_modules" / "npm"
    if target_modules.exists():
        shutil.rmtree(target_modules)
    shutil.copytree(npm_package_path, target_modules)
    typer.echo(f"📦 已部署 npm 到 {target_modules}")

    for tool in ["npm", "npx"]:
        source = target_modules / "bin" / f"{tool}.cmd"
        dest = node_dir / f"{tool}.cmd"
        if dest.exists():
            dest.unlink()
        shutil.copy(source, dest)
        typer.echo(f"🛠️ 已部署 {tool}.cmd 到 Node 目录")

    ps1 = node_dir / "npm.ps1"
    if ps1.exists():
        ps1.rename(ps1.with_suffix(".ps1.bak"))
        typer.echo(f"✅ 已禁用 PowerShell 拦截: {ps1}")

    typer.echo("✅ npm 安装完成，请执行 `npm -v` 验证。")


if __name__ == "__main__":
    app()
