import subprocess
import shutil
import typer
from pathlib import Path

REQUIRED_NODE_VERSION = "v10.24.1"
REQUIRED_NPM_VERSION = "6.14.12"


def get_command_output(cmd: list[str]) -> str:
    try:
        if cmd[0] == "npm":
            # 显式使用 npm.cmd 以绕过 PowerShell 的 alias 和拦截
            node_path = shutil.which("node")
            if not node_path:
                return ""
            node_dir = Path(node_path).parent
            npm_cmd = node_dir / "npm.cmd"
            if npm_cmd.exists():
                cmd[0] = str(npm_cmd)
        return subprocess.check_output(cmd, text=True).strip()
    except Exception as e:
        typer.echo(f"⚠️ 执行命令失败：{' '.join(cmd)} -> {e}")
        return ""


def check_versions() -> bool:
    node_ver = get_command_output(["node", "-v"])
    npm_ver = get_command_output(["npm", "-v"])

    typer.echo(f"🔍 当前 node 版本: {node_ver or '[未检测到]'}")
    typer.echo(f"🔍 当前 npm 版本: {npm_ver or '[未检测到]'}")

    if node_ver != REQUIRED_NODE_VERSION:
        typer.secho(f"❌ Node 版本错误，应为 {REQUIRED_NODE_VERSION}，当前为 {node_ver}", fg=typer.colors.RED)
        return False

    if npm_ver != REQUIRED_NPM_VERSION:
        typer.secho(f"❌ NPM 版本错误，应为 {REQUIRED_NPM_VERSION}，当前为 {npm_ver}", fg=typer.colors.RED)
        return False

    return True


def has_laya_file(path: Path) -> bool:
    return any(path.rglob("*.laya"))


def install_popxcmd():
    """
    安装 popxcmd：需满足 node/npm 版本正确，且当前路径或子路径中包含 .laya 文件
    """
    typer.echo("📦 正在准备安装 popxcmd...")

    if not check_versions():
        typer.secho("🚫 版本验证失败，终止安装。", fg=typer.colors.RED)
        return

    cwd = Path.cwd()
    if not has_laya_file(cwd):
        typer.secho("❌ 当前目录或子目录中未找到 .laya 文件，请确认路径是否为游戏主目录。", fg=typer.colors.RED)
        return

    typer.echo("🚀 执行命令：npm install -g popxcmd --registry=https://registry.popx.com")
    subprocess.run([
        "npm", "install", "-g", "popxcmd", "--registry=https://registry.popx.com"
    ], shell=True)

    typer.echo("✅ popxcmd 安装完成。")
