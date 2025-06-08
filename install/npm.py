import typer
import subprocess
import shutil
import tarfile
import os
from pathlib import Path

app = typer.Typer()

NPM_VERSION = "6.14.12"
TAR_NAME = f"npm-{NPM_VERSION}.tgz"
TAR_PATH = Path(__file__).parent / "install" / "bin" / TAR_NAME  # ✅ 修正路径
EXTRACT_PATH = Path(os.environ["TEMP"]) / "npm-local-install"


def is_npm_installed():
    return shutil.which("npm") is not None


@app.command("npm")
def install_npm():
    """
    离线安装本地 npm（v6.14.12），不联网拉取。
    """
    if is_npm_installed():
        try:
            current_ver = subprocess.check_output(["npm", "-v"], text=True).strip()
            if current_ver == NPM_VERSION:
                typer.echo(f"✅ 已安装 npm@{NPM_VERSION}")
                return
            else:
                typer.echo(f"🔁 当前 npm 为 {current_ver}，尝试离线覆盖安装为 {NPM_VERSION}")
        except Exception:
            typer.echo("⚠️ 无法判断 npm 版本，继续安装。")

    if not TAR_PATH.exists():
        typer.secho(f"❌ 缺少本地 npm 安装包: {TAR_PATH}", fg=typer.colors.RED)
        return

    if EXTRACT_PATH.exists():
        shutil.rmtree(EXTRACT_PATH)
    EXTRACT_PATH.mkdir(parents=True, exist_ok=True)

    typer.echo("📂 正在解压 npm 安装包...")
    with tarfile.open(TAR_PATH, "r:gz") as tar:
        tar.extractall(path=EXTRACT_PATH)

    npm_package_path = EXTRACT_PATH / "package"
    cli_js = npm_package_path / "bin" / "npm-cli.js"

    # 定位 Node 安装路径
    node_path = shutil.which("node")
    if not node_path:
        typer.secho("❌ 未检测到 node 命令，无法继续安装 npm。请先执行 `nvm use 10.24.1`。", fg=typer.colors.RED)
        return

    node_dir = Path(node_path).parent
    typer.echo(f"📁 Node 安装目录：{node_dir}")

    # 安装 npm 到 node_modules/npm
    target_modules = node_dir / "node_modules" / "npm"
    if target_modules.exists():
        shutil.rmtree(target_modules)
    shutil.copytree(npm_package_path, target_modules)
    typer.echo(f"📦 npm 核心已复制到 {target_modules}")

    # 安装可执行文件
    for tool in ["npm", "npx"]:
        source = target_modules / "bin" / f"{tool}.cmd"
        dest = node_dir / f"{tool}.cmd"
        if dest.exists():
            dest.unlink()
        shutil.copy(source, dest)
        typer.echo(f"🛠️ 已部署 {tool}.cmd 到 Node 目录")

    # 禁用 PowerShell 的 npm.ps1 拦截
    ps1_file = node_dir / "npm.ps1"
    if ps1_file.exists():
        ps1_file.rename(ps1_file.with_suffix(".ps1.bak"))
        typer.echo(f"✅ 已禁用 PowerShell 拦截: {ps1_file}")

    typer.echo("✅ npm 离线安装完成！请执行 `npm -v` 验证版本。")


if __name__ == "__main__":
    app()
