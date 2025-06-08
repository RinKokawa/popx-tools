import typer
from install import install_app

app = typer.Typer(help="Popx 环境部署 CLI 工具")
app.add_typer(install_app, name="install", help="安装相关依赖")

if __name__ == "__main__":
    app()
