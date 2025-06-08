import subprocess
import typer

def install_npm():
    """
    使用 npmmirror 镜像安装 npm@6.14.12
    """
    typer.echo("🔧 正在使用国内镜像安装 npm@6.14.12...")

    try:
        subprocess.run(
            ["npm", "install", "-g", "npm@6.14.12", "--registry=https://registry.npmmirror.com"],
            check=True, shell=True
        )

        npm_ver = subprocess.check_output(["npm", "-v"], text=True).strip()
        typer.echo(f"✅ npm 安装完成，当前版本: {npm_ver}")

    except subprocess.CalledProcessError as e:
        typer.echo("❌ npm 安装失败，请确认 Node 环境是否配置完成。")
        typer.echo("👉 手动运行命令也可以：")
        typer.echo("   npm install -g npm@6.14.12 --registry=https://registry.npmmirror.com")
