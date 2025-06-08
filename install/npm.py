import subprocess
import typer
import shutil

def install_npm():
    """
    使用 npmmirror 镜像安装 npm@6.14.12
    """
    typer.echo("🔧 尝试使用国内镜像安装 npm@6.14.12...")

    # 检查是否已存在 npm
    if shutil.which("npm") is None:
        typer.echo("⚠️ 未检测到 npm，请确认 Node.js 安装包是否附带 npm。")
        typer.echo("👉 你可以尝试用 nvm 重新安装 Node，或手动添加 npm。")
        return

    try:
        subprocess.run(
            ["npm", "install", "-g", "npm@6.14.12", "--registry=https://registry.npmmirror.com"],
            check=True, shell=True
        )
        npm_ver = subprocess.check_output(["npm", "-v"], text=True).strip()
        typer.echo(f"✅ npm 安装完成，当前版本: {npm_ver}")

    except subprocess.CalledProcessError:
        typer.echo("❌ npm 安装失败，请检查网络或 npm 权限问题。")
