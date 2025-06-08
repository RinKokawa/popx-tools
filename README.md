# Popx Tools

Popx 环境部署 CLI 工具集，提供环境安装、卸载和图像处理功能。

## 功能特性

- **环境管理**: 安装和卸载 Node.js、npm、nvm 等开发环境
- **图像处理**: 批量处理图像，生成包含三种亮度状态的图像文件
- **简单易用**: 基于 Typer 的命令行界面，支持帮助文档

## 安装

```bash
pip install popx-tools
```

## 使用方法

### 查看帮助

```bash
popx --help
```

### 环境安装

```bash
# 查看安装选项
popx install --help

# 一键安装所有环境
popx install all

# 安装特定组件
popx install nvm
popx install node
popx install npm
```

### 环境卸载

```bash
# 查看卸载选项
popx uninstall --help

# 卸载所有组件（包括清除快捷方式）
popx uninstall all

# 仅卸载 Node.js 和 npm
popx uninstall node

# 仅卸载 nvm（并清除快捷方式）
popx uninstall nvm
```

### 图像处理

```bash
# 查看图像处理选项
popx ui --help

# 批量处理图像
popx ui process image1.png image2.png image3.png
```

## 开发

本项目使用 Python 开发，基于以下主要依赖：

- typer: 命令行界面框架
- Pillow: 图像处理库
- rich: 终端输出美化

## 许可证

MIT License
