import typer
import webbrowser

def install_laya():
    """安装 Laya 编辑器"""
    url = "https://ldc2.layabox.com/layadownload/?type=layaairide-LayaAir%20IDE%202.13.1"
    typer.echo("🌐 正在打开 Laya 编辑器下载页面...")
    webbrowser.open(url)
