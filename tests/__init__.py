"""
Interactive MCP Popup 测试套件

包含弹窗功能、对话功能和集成测试。
"""

import sys
import os
import unittest

# 添加项目路径到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def run_all_tests():
    """运行所有测试"""
    print("🧪 Interactive MCP Popup 测试套件")
    print("=" * 50)
    
    # 发现并运行所有测试
    loader = unittest.TestLoader()
    suite = loader.discover('.', pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出测试结果摘要
    print("\n" + "=" * 50)
    print("测试结果摘要:")
    print(f"运行测试: {result.testsRun}")
    print(f"成功: {result.wasSuccessful()}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    
    if result.failures:
        print("\n失败的测试:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print("\n错误的测试:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('Exception:')[-1].strip()}")
    
    return result.wasSuccessful()


def run_specific_test(test_module):
    """运行特定测试模块"""
    print(f"🧪 运行测试模块: {test_module}")
    print("=" * 50)
    
    suite = unittest.TestLoader().loadTestsFromName(test_module)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


def run_manual_tests():
    """运行需要手动交互的测试"""
    print("🧪 手动交互测试")
    print("=" * 50)
    print("注意: 这些测试需要用户交互，请按照提示操作")
    
    # 导入并运行手动测试
    try:
        from test_popup import run_manual_tests
        run_manual_tests()
        return True
    except Exception as e:
        print(f"手动测试失败: {e}")
        return False


def run_demos():
    """运行功能演示"""
    print("🚀 功能演示")
    print("=" * 50)
    
    # 弹窗演示
    try:
        from test_popup import run_manual_tests
        print("\n弹窗演示:")
        run_manual_tests()
    except Exception as e:
        print(f"弹窗演示失败: {e}")
    
    # 对话演示
    try:
        from test_conversation import run_conversation_demo
        print("\n对话演示:")
        run_conversation_demo()
    except Exception as e:
        print(f"对话演示失败: {e}")
    
    return True


def check_dependencies():
    """检查测试依赖"""
    print("🔍 检查测试依赖")
    print("=" * 50)
    
    dependencies = {
        "unittest": "Python 标准库",
        "tempfile": "Python 标准库",
        "json": "Python 标准库",
        "PySide6": "Qt GUI 框架",
    }
    
    missing_deps = []
    
    for dep, description in dependencies.items():
        try:
            __import__(dep)
            print(f"✅ {dep}: {description}")
        except ImportError:
            print(f"❌ {dep}: {description} (缺失)")
            missing_deps.append(dep)
    
    if missing_deps:
        print(f"\n缺失依赖: {', '.join(missing_deps)}")
        print("某些测试将被跳过")
        return False
    else:
        print("\n✅ 所有依赖都可用")
        return True


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Interactive MCP Popup 测试套件")
    parser.add_argument("--all", action="store_true", help="运行所有测试")
    parser.add_argument("--popup", action="store_true", help="运行弹窗测试")
    parser.add_argument("--conversation", action="store_true", help="运行对话测试")
    parser.add_argument("--manual", action="store_true", help="运行手动交互测试")
    parser.add_argument("--demo", action="store_true", help="运行功能演示")
    parser.add_argument("--check", action="store_true", help="检查测试依赖")
    
    args = parser.parse_args()
    
    if args.check:
        check_dependencies()
    elif args.all:
        run_all_tests()
    elif args.popup:
        run_specific_test("test_popup")
    elif args.conversation:
        run_specific_test("test_conversation")
    elif args.manual:
        run_manual_tests()
    elif args.demo:
        run_demos()
    else:
        # 默认运行所有测试
        print("运行所有测试...")
        success = run_all_tests()
        
        if not success:
            print("\n💡 提示:")
            print("  - 使用 --check 检查依赖")
            print("  - 使用 --demo 运行功能演示")
            print("  - 使用 --manual 运行手动测试")
            sys.exit(1)
