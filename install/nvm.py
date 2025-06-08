import typer
import subprocess
import os

def install_nvm():
    """
    使用 PowerShell 命令下载并启动 nvm-setup.exe 安装程序
    """
    typer.echo("🔽 正在下载 nvm-windows 安装程序...")

    powershell_script = '''
    Invoke-WebRequest -Uri "https://github.com/coreybutler/nvm-windows/releases/latest/download/nvm-setup.exe" -OutFile "$env:TEMP\\nvm-setup.exe"
    Start-Process "$env:TEMP\\nvm-setup.exe"
    '''

    try:
        subprocess.run(["powershell", "-Command", powershell_script], check=True)
        typer.echo("✅ 安装程序已启动，请按指引完成安装。")
    except subprocess.CalledProcessError as e:
        typer.echo("❌ 安装失败，请手动访问链接下载：")
        typer.echo("👉 https://github.com/coreybutler/nvm-windows/releases")
