import typer
from typing import List
from PIL import Image, ImageEnhance
import sys

ui_app = typer.Typer(help="图像处理工具", no_args_is_help=True)

def process_single_image(input_path: str) -> bool:
    """处理单个图像文件"""
    try:
        # 打开原始图像（保持透明度）
        original_img = Image.open(input_path).convert('RGBA')
        width, height = original_img.size
        
        # 创建透明背景的新画布（高度扩大三倍）
        new_height = height * 3
        new_img = Image.new('RGBA', (width, new_height), (0, 0, 0, 0))
        
        # 放置原始图像在上部（保持原始亮度）
        new_img.paste(original_img, (0, 0), original_img)
        
        # 创建亮度提高的版本（中间按钮）
        enhancer = ImageEnhance.Brightness(original_img)
        brighter_img = enhancer.enhance(1.5)  # 1.5表示150%亮度
        
        # 放置亮度提高的图像在中间
        new_img.paste(brighter_img, (0, height), brighter_img)
        
        # 创建亮度降低的版本（底部按钮）
        darker_img = enhancer.enhance(0.5)  # 0.5表示50%亮度
        
        # 放置亮度降低的图像在底部
        new_img.paste(darker_img, (0, height * 2), darker_img)
        
        # 生成输出路径
        if '.' in input_path:
            output_path = input_path.rsplit('.', 1)[0] + '_processed.png'
        else:
            output_path = input_path + '_processed.png'
        
        # 保存结果
        new_img.save(output_path, format='PNG')
        typer.echo(f"处理完成: {input_path} -> {output_path}")
        return True
        
    except Exception as e:
        typer.secho(f"处理图像 {input_path} 时出错: {e}", fg=typer.colors.RED)
        return False

@ui_app.command()
def process(
    image_paths: List[str] = typer.Argument(..., help="要处理的图像文件路径列表")
):
    """
    批量处理图像文件，生成包含三种亮度状态的图像
    
    示例:
    popx ui process button1.png button2.png button3.png
    """
    if not image_paths:
        typer.secho("请提供至少一个图像文件路径", fg=typer.colors.RED)
        raise typer.Exit(1)
    
    success_count = 0
    for path in image_paths:
        if process_single_image(path.strip()):  # 去除可能的空格
            success_count += 1
    
    typer.echo(f"\n批量处理完成: 共处理 {len(image_paths)} 个文件，成功 {success_count} 个")

# 确保 ui_app 被模块导出
__all__ = ["ui_app"] 