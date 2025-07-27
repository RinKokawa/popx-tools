import typer
import subprocess
import os
import sys
import time
from typing import Optional


def get_current_node_version() -> Optional[str]:
    """获取当前使用的 Node.js 版本"""
    try:
        # 在 Windows 上使用 nvm list 命令获取当前版本
        result = subprocess.run(
            ["nvm", "list"], 
            capture_output=True, 
            text=True, 
            shell=True,
            check=True
        )
        
        # 解析输出找到当前版本
        output = result.stdout
        lines = output.split('\n')
        
        for line in lines:
            # 查找带有 * 标记的行，表示当前使用的版本
            if '*' in line and 'Currently using' in line:
                # 提取版本号 - 更简单的方法
                parts = line.split()
                for i, part in enumerate(parts):
                    if part == '*':
                        # 下一个部分应该是版本号
                        if i + 1 < len(parts):
                            version = parts[i + 1]
                            # 确保是版本号格式
                            if version.replace('.', '').isdigit():
                                return version
                        break
            # 兼容旧格式，查找带有 -> 的行
            elif '->' in line and 'v' in line:
                # 提取版本号
                version_start = line.find('v') + 1
                version_end = line.find(' ', version_start)
                if version_end == -1:
                    version_end = line.find('\t', version_start)
                if version_end == -1:
                    version_end = len(line)
                return line[version_start:version_end]
        
        return None
    except subprocess.CalledProcessError:
        typer.secho("❌ 无法获取当前 Node.js 版本", fg=typer.colors.RED)
        return None
    except Exception as e:
        typer.secho(f"❌ 检查 Node.js 版本时出错: {e}", fg=typer.colors.RED)
        return None


def verify_node_version(target_version: str, max_retries: int = 3) -> bool:
    """验证当前 Node.js 版本是否为指定版本，支持重试"""
    for attempt in range(max_retries):
        # 等待一小段时间让版本切换生效
        time.sleep(1)
        
        current_version = get_current_node_version()
        if current_version == target_version:
            return True
        
        if attempt < max_retries - 1:
            typer.secho(f"⚠️  版本验证失败 (尝试 {attempt + 1}/{max_retries})，当前版本: {current_version}，目标版本: {target_version}", fg=typer.colors.YELLOW)
            time.sleep(2)  # 等待更长时间后重试
    
    typer.secho(f"❌ 版本验证失败，当前版本: {current_version}，目标版本: {target_version}", fg=typer.colors.RED)
    return False


def switch_to_node_version(version: str) -> bool:
    """切换到指定的 Node.js 版本"""
    try:
        typer.echo(f"🔄 切换到 Node.js {version}...")
        
        # 尝试使用更简单的方法：直接调用 nvm 并假设成功
        # 因为 nvm 切换版本通常不需要确认，除非有特殊情况
        result = subprocess.run(
            f'nvm use {version}', 
            capture_output=True, 
            text=True, 
            shell=True,
            check=False  # 不检查退出码，因为可能有确认提示
        )
        
        # 检查输出中是否包含成功信息
        output = result.stdout.lower()
        if "now using" in output or "正在使用" in output or f"v{version}" in output:
            typer.secho(f"✅ 已切换到 Node.js {version}", fg=typer.colors.GREEN)
            return True
        else:
            # 如果没有成功信息，但也没有错误，可能是需要确认
            # 在这种情况下，我们假设切换成功，因为 nvm 通常会自动处理
            if result.returncode == 0 or "请确认" not in result.stdout:
                typer.secho(f"✅ 已切换到 Node.js {version} (假设成功)", fg=typer.colors.GREEN)
                return True
            else:
                typer.secho(f"⚠️  切换到 Node.js {version} 需要手动确认", fg=typer.colors.YELLOW)
                typer.echo(f"请手动运行: nvm use {version}")
                return False
            
    except subprocess.CalledProcessError as e:
        typer.secho(f"❌ 切换到 Node.js {version} 失败: {e.stderr}", fg=typer.colors.RED)
        return False
    except Exception as e:
        typer.secho(f"❌ 切换 Node.js 版本时出错: {e}", fg=typer.colors.RED)
        return False


def switch_to_node_version_with_retry(version: str, max_retries: int = 3) -> bool:
    """切换到指定的 Node.js 版本，带重试和验证机制"""
    for attempt in range(max_retries):
        if attempt > 0:
            typer.secho(f"🔄 重试切换到 Node.js {version} (尝试 {attempt + 1}/{max_retries})...", fg=typer.colors.YELLOW)
        
        # 执行版本切换
        if switch_to_node_version(version):
            # 验证切换是否成功
            if verify_node_version(version):
                return True
            else:
                typer.secho(f"⚠️  版本切换命令成功但验证失败 (尝试 {attempt + 1}/{max_retries})", fg=typer.colors.YELLOW)
        else:
            typer.secho(f"⚠️  版本切换命令失败 (尝试 {attempt + 1}/{max_retries})", fg=typer.colors.YELLOW)
        
        # 如果不是最后一次尝试，等待后重试
        if attempt < max_retries - 1:
            time.sleep(3)
    
    return False


def run_npm_command(command: str) -> bool:
    """运行 npm 命令"""
    try:
        typer.echo(f"🚀 执行: npm run {command}")
        
        # 在 Windows 上，nvm 切换版本后需要重新设置环境变量
        # 使用 PowerShell 的 & 操作符来确保在新的环境中执行
        result = subprocess.run(
            f'powershell -Command "& npm run {command}"', 
            shell=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        typer.secho(f"❌ npm run {command} 执行失败", fg=typer.colors.RED)
        return False
    except Exception as e:
        typer.secho(f"❌ 执行 npm 命令时出错: {e}", fg=typer.colors.RED)
        return False
    finally:
        # 确保在函数结束时输出调试信息
        typer.echo(f"🔍 npm run {command} 执行完成，准备恢复版本")


def run_command(command: str):
    """运行指定的命令（ui 或 build）"""
    target_version = "10.24.1"
    restore_version = "22.15.0"
    
    # 检查当前 Node.js 版本
    current_version = get_current_node_version()
    
    if current_version is None:
        typer.secho("❌ 无法确定当前 Node.js 版本，请确保 nvm 已正确安装", fg=typer.colors.RED)
        sys.exit(1)
    
    typer.echo(f"📋 当前 Node.js 版本: {current_version}")
    
    # 记录原始版本，用于后续恢复
    original_version = current_version
    
    # 如果版本不匹配，则切换版本
    if current_version != target_version:
        typer.echo(f"⚠️  需要 Node.js {target_version}，当前版本为 {current_version}")
        if not switch_to_node_version_with_retry(target_version):
            typer.secho("❌ 版本切换失败，无法继续执行", fg=typer.colors.RED)
            sys.exit(1)
    else:
        typer.echo(f"✅ 当前版本 {current_version} 符合要求")
    
    # 执行 npm 命令
    success = False
    try:
        success = run_npm_command(command)
        if not success:
            sys.exit(1)
        
        typer.secho(f"🎉 {command} 命令执行完成！", fg=typer.colors.GREEN)
        
    except Exception as e:
        typer.secho(f"❌ 执行 {command} 命令时出错: {e}", fg=typer.colors.RED)
        success = False
    finally:
        # 无论命令是否成功，都尝试恢复到原始版本或 22.15.0
        typer.echo(f"🔍 开始恢复版本，原始版本: {original_version}, 目标版本: {restore_version}")
        try:
            if original_version != restore_version:
                typer.echo(f"🔄 正在切换回 Node.js {restore_version}...")
                if switch_to_node_version_with_retry(restore_version):
                    typer.secho(f"✅ 已成功切换回 Node.js {restore_version}", fg=typer.colors.GREEN)
                else:
                    typer.secho(f"❌ 切换回 Node.js {restore_version} 失败，请手动切换", fg=typer.colors.RED)
                    typer.secho(f"请手动运行: nvm use {restore_version}", fg=typer.colors.YELLOW)
            else:
                typer.echo(f"✅ 当前版本 {original_version} 已经是目标版本，无需切换")
        except Exception as e:
            typer.secho(f"❌ 恢复版本时出错: {e}", fg=typer.colors.RED)
            typer.secho(f"请手动运行: nvm use {restore_version}", fg=typer.colors.YELLOW) 