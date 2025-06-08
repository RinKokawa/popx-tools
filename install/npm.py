import subprocess
import typer
import shutil

def install_npm():
    """
    使用 npmmirror 镜像安装 npm@6.14.12（优先使用已存在的 npm 执行升级）
    """
    typer.echo("🔧 尝试使用国内镜像安装 npm@6.14.12...")

    # 检查是否存在 npm
    npm_path = shutil.which("npm")
    if npm_path is None:
        typer.echo("⚠️ 未检测到 npm，请确认 Node.js 安装包是否附带 npm。")
        typer.echo("👉 你可以尝试先重新安装 Node.js，或使用 fallback 包手动解压 npm。")
        typer.echo("👉 或使用 PowerShell 命令手动下载:")
        typer.echo("   Invoke-WebRequest -Uri \"https://registry.npmmirror.com/npm/-/npm-6.14.12.tgz\" -OutFile \"npm-6.14.12.tgz\"")
        return

    try:
        # 使用已存在 npm 更新自身
        subprocess.run(
            ["npm", "install", "-g", "npm@6.14.12", "--registry=https://registry.npmmirror.com"],
            check=True, shell=True
        )
        npm_ver = subprocess.check_output(["npm", "-v"], text=True).strip()
        typer.echo(f"✅ npm 安装完成，当前版本: {npm_ver}")

    except subprocess.CalledProcessError:
        typer.echo("❌ npm 安装失败，请检查网络连接或权限问题。")
