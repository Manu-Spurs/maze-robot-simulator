#!/usr/bin/env python3
"""
Maze Robot Simulator Quick Start
迷宫机器人模拟器快速启动
"""

import sys
import os

def main():
    """快速启动主程序"""
    print("启动迷宫机器人模拟器...")
    print("Starting Maze Robot Simulator...")
    
    # 检查主程序文件是否存在
    main_file = "Maze_Simulation_v1.py"
    if not os.path.exists(main_file):
        print(f"错误: 找不到主程序文件 {main_file}")
        print(f"Error: Main program file {main_file} not found")
        return False
    
    try:
        # 导入并运行主程序
        import Maze_Simulation_v1
        Maze_Simulation_v1.main()
    except ImportError as e:
        print(f"导入错误: {e}")
        print(f"Import error: {e}")
        print("请确保已安装所有依赖: pip install -r requirements.txt")
        print("Please install dependencies: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"运行错误: {e}")
        print(f"Runtime error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        input("按回车键退出...")
        sys.exit(1)
