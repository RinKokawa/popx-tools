import typer
import os
import shutil
import subprocess
from pathlib import Path

uninstall_app = typer.Typer(help="卸载所有已安装组件", no_args_is_help=True)

USER_HOME = Path(os.environ["USERPROFILE"])
NVM_DIR = USER_HOME / "AppData" / "Local" / "nvm"
NODE_VERSION = "10.24.1"
NODE_DIR = NVM_DIR / f"v{NODE_VERSION}"
NODEJS_DIR = NVM_DIR / "nodejs"
NPM_POWERSHELL_PATHS = [
    NODEJS_DIR / "npm.ps1",
    NODEJS_DIR / "npm.ps1.bak"
]
SETTINGS_FILE = NVM_DIR / "settings.txt"

def remove_desktop_shortcuts():
    """清除桌面上的node/npm/nvm相关快捷方式"""
    desktop = USER_HOME / "Desktop"
    shortcuts_to_remove = [
        "Node.js.lnk",
        "Node.js command prompt.lnk", 
        "npm.lnk",
        "nvm.lnk"
    ]
    
    removed_count = 0
    for shortcut in shortcuts_to_remove:
        shortcut_path = desktop / shortcut
        if shortcut_path.exists():
            try:
                shortcut_path.unlink()
                typer.echo(f"🧹 已移除桌面快捷方式: {shortcut}")
                removed_count += 1
            except Exception as e:
                typer.secho(f"⚠️ 无法删除快捷方式 {shortcut}: {e}", fg=typer.colors.YELLOW)
    
    if removed_count == 0:
        typer.echo("ℹ️ 未发现需要清理的桌面快捷方式")

def remove_start_menu_shortcuts():
    """清除开始菜单中的node/npm/nvm相关快捷方式"""
    start_menu_paths = [
        USER_HOME / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs",
        Path("C:") / "ProgramData" / "Microsoft" / "Windows" / "Start Menu" / "Programs"
    ]
    
    shortcuts_patterns = ["*node*", "*npm*", "*nvm*"]
    removed_count = 0
    
    for start_menu in start_menu_paths:
        if start_menu.exists():
            for pattern in shortcuts_patterns:
                for shortcut in start_menu.rglob(pattern):
                    if shortcut.suffix.lower() in ['.lnk', '.url']:
                        try:
                            shortcut.unlink()
                            typer.echo(f"🧹 已移除开始菜单快捷方式: {shortcut.name}")
                            removed_count += 1
                        except Exception as e:
                            typer.secho(f"⚠️ 无法删除快捷方式 {shortcut.name}: {e}", fg=typer.colors.YELLOW)
    
    if removed_count == 0:
        typer.echo("ℹ️ 未发现需要清理的开始菜单快捷方式")

def clean_path_environment():
    """清理PATH环境变量中的nvm和node路径"""
    try:
        # 使用PowerShell清理用户PATH环境变量
        powershell_script = f"""
        $userPath = [Environment]::GetEnvironmentVariable('Path', 'User')
        $pathsToRemove = @('{NVM_DIR}', '{NODEJS_DIR}')
        $newPath = ($userPath -split ';' | Where-Object {{ $_ -notin $pathsToRemove }}) -join ';'
        [Environment]::SetEnvironmentVariable('Path', $newPath, 'User')
        """
        
        subprocess.run([
            "powershell", "-Command", powershell_script
        ], check=True, capture_output=True)
        
        typer.echo("🔧 已清理 PATH 环境变量中的 nvm/node 路径")
    except Exception as e:
        typer.secho(f"⚠️ 清理PATH环境变量时出错: {e}", fg=typer.colors.YELLOW)

@uninstall_app.command("node")
def uninstall_node():
    """
    卸载 Node.js 和 npm
    """
    typer.echo("🗑️ 开始卸载 Node.js 和 npm...")
    
    # 删除 node 版本目录
    if NODE_DIR.exists():
        shutil.rmtree(NODE_DIR)
        typer.echo(f"🗑️ 已删除 Node 版本目录: {NODE_DIR}")

    # 删除 nodejs 软链接路径
    if NODEJS_DIR.exists():
        shutil.rmtree(NODEJS_DIR)
        typer.echo(f"🗑️ 已删除 nodejs 执行路径: {NODEJS_DIR}")

    # 删除 npm.ps1 拦截文件
    for ps1 in NPM_POWERSHELL_PATHS:
        if ps1.exists():
            ps1.unlink()
            typer.echo(f"🧹 已移除: {ps1}")

    # 清理 settings.txt 中的版本记录
    if SETTINGS_FILE.exists():
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            for line in lines:
                if NODE_VERSION not in line:
                    f.write(line)
        typer.echo("🧽 已清理 settings.txt 中的 node 记录")

    typer.secho("✅ Node.js 和 npm 卸载完成。", fg=typer.colors.GREEN)

@uninstall_app.command("nvm")
def uninstall_nvm():
    """
    卸载 nvm 并清除所有相关快捷方式
    """
    typer.echo("🗑️ 开始卸载 nvm...")
    
    # 删除 nvm.exe（非强制）
    nvm_exe = NVM_DIR / "nvm.exe"
    if nvm_exe.exists():
        try:
            nvm_exe.unlink()
            typer.echo("🗑️ 已删除 nvm.exe")
        except PermissionError:
            typer.secho("⚠️ 无法删除 nvm.exe，可能在使用中", fg=typer.colors.YELLOW)

    # 删除整个nvm目录（如果存在且为空）
    if NVM_DIR.exists():
        try:
            # 检查目录是否为空或只包含我们要删除的内容
            remaining_files = list(NVM_DIR.rglob('*'))
            if not remaining_files or all(f.name in ['settings.txt'] for f in remaining_files if f.is_file()):
                shutil.rmtree(NVM_DIR)
                typer.echo(f"🗑️ 已删除 nvm 目录: {NVM_DIR}")
            else:
                typer.echo(f"ℹ️ nvm 目录包含其他文件，保留目录: {NVM_DIR}")
        except Exception as e:
            typer.secho(f"⚠️ 无法完全删除 nvm 目录: {e}", fg=typer.colors.YELLOW)

    # 清除桌面快捷方式
    remove_desktop_shortcuts()
    
    # 清除开始菜单快捷方式
    remove_start_menu_shortcuts()
    
    # 清理PATH环境变量
    clean_path_environment()

    typer.secho("✅ nvm 卸载完成，已清除相关快捷方式。", fg=typer.colors.GREEN)

@uninstall_app.command("all")
def uninstall_all():
    """
    卸载所有组件：nvm、node、npm，并清除快捷方式
    """
    typer.echo("🗑️ 开始卸载所有组件...")
    
    # 先卸载node和npm
    uninstall_node()
    
    # 再卸载nvm和清除快捷方式
    uninstall_nvm()

    typer.secho("✅ 全部卸载完成。建议重新启动终端或注销重新登录。", fg=typer.colors.GREEN)

# 确保 uninstall_app 被模块导出
__all__ = ["uninstall_app"] 