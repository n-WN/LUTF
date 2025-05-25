#!/usr/bin/env python3
import sys
import json
import re
import ast
import time
import os
from typing import List, Optional, Dict, Any
from collections import defaultdict, deque
import heapq
import difflib

# Try to import colorama, fallback to no colors if not available
try:
    from colorama import Fore, Back, Style, init
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    # Fallback: no colors
    class MockColor:
        def __getattr__(self, name):
            return ""
    
    Fore = Back = Style = MockColor()
    COLORS_AVAILABLE = False
    
    def init(autoreset=True):
        pass

# 定义TreeNode类（如果题目需要）
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"TreeNode({self.val})"

# 定义ListNode类（如果题目需要）
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    
    def __repr__(self):
        return f"ListNode({self.val})"

class LeetCodeTester:
    def __init__(self):
        self.solution_code = ""
        self.solution_class = None
        self.test_cases = []
        self.expected_outputs = []
        
    def colorize_text(self, text: str, color: str) -> str:
        """给文本添加颜色"""
        if not COLORS_AVAILABLE:
            return text
            
        color_map = {
            'red': Fore.RED,
            'green': Fore.GREEN,
            'yellow': Fore.YELLOW,
            'blue': Fore.BLUE,
            'magenta': Fore.MAGENTA,
            'cyan': Fore.CYAN,
            'white': Fore.WHITE,
            'bright_red': Fore.LIGHTRED_EX,
            'bright_green': Fore.LIGHTGREEN_EX,
            'bright_yellow': Fore.LIGHTYELLOW_EX,
        }
        return f"{color_map.get(color, '')}{text}{Style.RESET_ALL}"
    
    def format_value(self, value: Any) -> str:
        """格式化值为字符串，支持美化输出"""
        if isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value, list):
            if len(value) <= 20:  # 短数组在一行显示
                return str(value)
            else:  # 长数组分行显示
                return "[\n  " + ",\n  ".join(str(item) for item in value) + "\n]"
        else:
            return str(value)
    
    def create_colored_diff(self, expected: Any, actual: Any) -> str:
        """创建带颜色的diff输出"""
        expected_str = self.format_value(expected)
        actual_str = self.format_value(actual)
        
        if expected_str == actual_str:
            return self.colorize_text(expected_str, 'green')
        
        # 如果字符串较短，使用字符级diff
        if len(expected_str) <= 100 and len(actual_str) <= 100:
            return self.create_inline_diff(expected_str, actual_str)
        
        # 较长字符串使用行级diff
        expected_lines = expected_str.splitlines()
        actual_lines = actual_str.splitlines()
        
        diff_lines = []
        diff_lines.append(self.colorize_text("Expected:", 'cyan'))
        for line in expected_lines:
            diff_lines.append(self.colorize_text(f"  {line}", 'green'))
        
        diff_lines.append(self.colorize_text("Actual:", 'cyan'))
        for line in actual_lines:
            diff_lines.append(self.colorize_text(f"  {line}", 'red'))
        
        return "\n".join(diff_lines)
    
    def create_inline_diff(self, expected: str, actual: str) -> str:
        """创建内联字符级diff"""
        diff_result = []
        
        # 使用difflib进行字符级比较
        matcher = difflib.SequenceMatcher(None, expected, actual)
        
        diff_result.append(self.colorize_text("Expected: ", 'cyan'))
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                diff_result.append(expected[i1:i2])
            elif tag == 'delete':
                diff_result.append(self.colorize_text(expected[i1:i2], 'green'))
            elif tag == 'insert':
                pass  # 在expected中不显示插入的部分
            elif tag == 'replace':
                diff_result.append(self.colorize_text(expected[i1:i2], 'green'))
        
        diff_result.append("\n")
        diff_result.append(self.colorize_text("Actual:   ", 'cyan'))
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                diff_result.append(actual[j1:j2])
            elif tag == 'delete':
                pass  # 在actual中不显示删除的部分
            elif tag == 'insert':
                diff_result.append(self.colorize_text(actual[j1:j2], 'red'))
            elif tag == 'replace':
                diff_result.append(self.colorize_text(actual[j1:j2], 'red'))
        
        return "".join(diff_result)
    
    def print_test_result(self, case_num: int, case_data: List, expected: Any, 
                         actual: Any, success: bool, execution_time: float):
        """打印带颜色的测试结果"""
        print(f"\n{self.colorize_text(f'Test Case {case_num}:', 'bright_yellow')}")
        print(f"{self.colorize_text('Input:', 'cyan')} {self.format_value(case_data)}")
        
        # 格式化执行时间
        if execution_time < 1:
            time_str = f"{execution_time * 1000:.2f}ms"
            time_color = 'green' if execution_time < 0.001 else 'yellow' if execution_time < 0.01 else 'red'
        else:
            time_str = f"{execution_time:.3f}s"
            time_color = 'red'
        
        if success:
            print(f"{self.colorize_text('Output:', 'cyan')} {self.colorize_text(self.format_value(actual), 'green')}")
            print(f"{self.colorize_text('Time:', 'cyan')} {self.colorize_text(time_str, time_color)}")
            print(f"{self.colorize_text('Result:', 'bright_green')} {self.colorize_text('✓ PASS', 'bright_green')}")
        else:
            print(f"{self.colorize_text('Diff:', 'cyan')}")
            print(self.create_colored_diff(expected, actual))
            print(f"{self.colorize_text('Time:', 'cyan')} {self.colorize_text(time_str, time_color)}")
            print(f"{self.colorize_text('Result:', 'bright_red')} {self.colorize_text('✗ FAIL', 'bright_red')}")
    
    def print_summary(self, passed: int, total: int):
        """打印带颜色的总结"""
        print("\n" + "=" * 60)
        if passed == total:
            print(f"{self.colorize_text('🎉 All tests passed!', 'bright_green')} "
                  f"{self.colorize_text(f'({passed}/{total})', 'green')}")
        else:
            failed = total - passed
            print(f"{self.colorize_text('Test Summary:', 'bright_yellow')}")
            print(f"  {self.colorize_text('✓ Passed:', 'green')} {passed}")
            print(f"  {self.colorize_text('✗ Failed:', 'red')} {failed}")
            print(f"  {self.colorize_text('Total:', 'cyan')} {total}")
            
            success_rate = (passed / total) * 100
            if success_rate >= 80:
                color = 'green'
            elif success_rate >= 50:
                color = 'yellow'
            else:
                color = 'red'
            print(f"  {self.colorize_text('Success Rate:', 'cyan')} "
                  f"{self.colorize_text(f'{success_rate:.1f}%', color)}")
        print("=" * 60)
        
    def parse_solution_template(self, template_code: str):
        """解析题目模板，识别类型和方法"""
        self.solution_code = template_code
        
        # 编译解决方案代码
        try:
            exec(self.solution_code, globals())
            if 'Solution' in globals():
                self.solution_class = globals()['Solution']
            else:
                # 查找其他类名（如MedianFinder等）
                for name, obj in globals().items():
                    if isinstance(obj, type) and name != 'TreeNode' and name != 'ListNode':
                        self.solution_class = obj
                        break
        except Exception as e:
            print(f"Error compiling solution: {e}")
            return False
        
        return True
    
    def parse_input_file(self, input_file: str):
        """解析输入文件"""
        self.test_cases = []
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            current_case = []
            for line in lines:
                line = line.strip()
                if not line:  # 空行，分割测试用例
                    if current_case:
                        self.test_cases.append(current_case)
                        current_case = []
                else:
                    current_case.append(self.parse_input_line(line))
            
            # 添加最后一个测试用例
            if current_case:
                self.test_cases.append(current_case)
                
        except Exception as e:
            print(f"Error reading input file: {e}")
    
    def parse_output_file(self, output_file: str):
        """解析期望输出文件"""
        self.expected_outputs = []
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            for line in lines:
                line = line.strip()
                if line:  # 非空行
                    self.expected_outputs.append(self.parse_input_line(line))
                    
        except Exception as e:
            print(f"Error reading output file: {e}")
    
    def parse_input_line(self, line: str):
        """解析单行输入，支持各种数据类型"""
        line = line.strip()
        
        # 处理null
        line = line.replace('null', 'None')
        line = line.replace('true', 'True')
        line = line.replace('false', 'False')
        
        try:
            # 尝试直接解析为Python对象
            return ast.literal_eval(line)
        except:
            # 如果失败，尝试作为字符串处理
            if line.startswith('"') and line.endswith('"'):
                return line[1:-1]
            elif line.startswith("'") and line.endswith("'"):
                return line[1:-1]
            else:
                return line
    
    def build_tree_from_list(self, nodes: List):
        """从列表构建二叉树"""
        if not nodes or nodes[0] is None:
            return None
        
        root = TreeNode(nodes[0])
        queue = deque([root])
        i = 1
        
        while queue and i < len(nodes):
            node = queue.popleft()
            
            # 添加左子节点
            if i < len(nodes) and nodes[i] is not None:
                node.left = TreeNode(nodes[i])
                queue.append(node.left)
            i += 1
            
            # 添加右子节点
            if i < len(nodes) and nodes[i] is not None:
                node.right = TreeNode(nodes[i])
                queue.append(node.right)
            i += 1
        
        return root
    
    def build_list_from_array(self, arr: List):
        """从数组构建链表"""
        if not arr:
            return None
        
        head = ListNode(arr[0])
        current = head
        for val in arr[1:]:
            current.next = ListNode(val)
            current = current.next
        
        return head
    
    def tree_to_list(self, root: TreeNode):
        """将二叉树转换为列表（层序遍历）"""
        if not root:
            return []
        
        result = []
        queue = deque([root])
        
        while queue:
            node = queue.popleft()
            if node:
                result.append(node.val)
                queue.append(node.left)
                queue.append(node.right)
            else:
                result.append(None)
        
        # 移除末尾的None
        while result and result[-1] is None:
            result.pop()
        
        return result
    
    def list_to_array(self, head: ListNode):
        """将链表转换为数组"""
        result = []
        current = head
        while current:
            result.append(current.val)
            current = current.next
        return result
    
    def detect_method_signature(self):
        """检测解决方案的方法签名"""
        if not self.solution_class:
            return None, []
            
        methods = [method for method in dir(self.solution_class) 
                  if not method.startswith('_')]
        
        if not methods:
            return None, []
        
        # 获取第一个非私有方法
        method_name = methods[0]
        method = getattr(self.solution_class, method_name)
        
        # 获取方法参数（排除self）
        import inspect
        sig = inspect.signature(method)
        params = list(sig.parameters.keys())[1:]  # 排除self
        
        return method_name, params
    
    def run_test_case(self, case_data: List, expected: Any):
        """运行单个测试用例"""
        if not self.solution_class:
            return False, "No solution class found", 0.0
        
        try:
            # 记录开始时间
            start_time = time.perf_counter()
            
            # 检测是否是设计类题目（如MedianFinder）
            if hasattr(self.solution_class, '__init__') and len(case_data) > 1:
                success, result = self.run_design_class_test(case_data, expected)
            else:
                success, result = self.run_function_test(case_data, expected)
            
            # 记录结束时间
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            
            return success, result, execution_time
                
        except Exception as e:
            end_time = time.perf_counter()
            execution_time = end_time - start_time if 'start_time' in locals() else 0.0
            return False, f"Runtime error: {str(e)}", execution_time
    
    def run_function_test(self, case_data: List, expected: Any):
        """运行函数类型的测试"""
        solution = self.solution_class()
        method_name, params = self.detect_method_signature()
        
        if not method_name:
            return False, "No method found"
        
        method = getattr(solution, method_name)
        
        # 准备参数
        args = []
        for i, param_data in enumerate(case_data):
            # 根据参数名推断数据类型
            if i < len(params):
                param_name = params[i]
                if 'tree' in param_name.lower() or 'root' in param_name.lower():
                    args.append(self.build_tree_from_list(param_data))
                elif 'list' in param_name.lower() and isinstance(param_data, list) and param_data and isinstance(param_data[0], int):
                    # 可能是链表
                    args.append(self.build_list_from_array(param_data))
                else:
                    args.append(param_data)
            else:
                args.append(param_data)
        
        # 执行方法
        result = method(*args)
        
        # 特殊处理：如果方法返回None但修改了输入参数（如moveZeroes）
        if result is None and args:
            # 检查第一个参数是否被修改（通常是数组）
            if isinstance(args[0], list):
                result = args[0]
        
        # 处理结果
        processed_result = self.process_result(result)
        processed_expected = self.process_result(expected)
        
        return processed_result == processed_expected, processed_result
    
    def run_design_class_test(self, case_data: List, expected: Any):
        """运行设计类的测试"""
        if len(case_data) < 2:
            return False, "Invalid design class test case"
        
        methods = case_data[0]
        params_list = case_data[1]
        
        if not isinstance(methods, list) or not isinstance(params_list, list):
            return False, "Invalid design class test format"
        
        results = []
        obj = None
        
        for i, (method_name, params) in enumerate(zip(methods, params_list)):
            if method_name == self.solution_class.__name__:
                # 构造函数
                obj = self.solution_class(*params)
                results.append(None)
            else:
                if obj is None:
                    return False, "Object not initialized"
                
                method = getattr(obj, method_name)
                result = method(*params)
                results.append(result)
        
        # 过滤掉None结果（构造函数）
        filtered_results = [r for r in results if r is not None]
        
        if isinstance(expected, list):
            expected_filtered = [e for e in expected if e is not None]
            return filtered_results == expected_filtered, filtered_results
        else:
            return filtered_results == [expected], filtered_results
    
    def process_result(self, result):
        """处理结果，转换特殊对象为可比较的格式"""
        if isinstance(result, TreeNode):
            return self.tree_to_list(result)
        elif isinstance(result, ListNode):
            return self.list_to_array(result)
        else:
            return result
    
    def run_all_tests(self):
        """运行所有测试用例"""
        if len(self.test_cases) != len(self.expected_outputs):
            print(self.colorize_text(
                f"❌ Mismatch: {len(self.test_cases)} test cases, "
                f"{len(self.expected_outputs)} expected outputs", 'red'))
            return False
        
        passed = 0
        total = len(self.test_cases)
        
        print(self.colorize_text(f"🚀 Running {total} test cases...", 'bright_yellow'))
        print("-" * 60)
        
        for i, (case_data, expected) in enumerate(zip(self.test_cases, self.expected_outputs)):
            success, result, execution_time = self.run_test_case(case_data, expected)
            self.print_test_result(i + 1, case_data, expected, result, success, execution_time)
            
            if success:
                passed += 1
        
        self.print_summary(passed, total)
        return passed == total

def main():
    # 检查参数数量
    if len(sys.argv) < 2:
        color_code = Fore.RED if COLORS_AVAILABLE else ""
        reset_code = Style.RESET_ALL if COLORS_AVAILABLE else ""
        print(f"{color_code}Usage: python leetcode_tester.py <solution.py> [input.txt] [output.txt]{reset_code}")
        print("If input.txt and output.txt are not specified, will look for them in the solution directory")
        sys.exit(1)
    
    solution_file = sys.argv[1]
    
    # 检查solution文件是否存在
    if not os.path.exists(solution_file):
        print(f"❌ Solution file not found: {solution_file}")
        sys.exit(1)
    
    # 获取solution文件所在目录
    solution_dir = os.path.dirname(os.path.abspath(solution_file))
    
    # 确定input和output文件路径
    if len(sys.argv) >= 3:
        input_file = sys.argv[2]
    else:
        input_file = os.path.join(solution_dir, "input.txt")
        if not os.path.exists(input_file):
            print(f"❌ Input file not found: {input_file}")
            print("💡 Create input.txt in the solution directory or specify input file path")
            sys.exit(1)
    
    if len(sys.argv) >= 4:
        output_file = sys.argv[3]
    else:
        output_file = os.path.join(solution_dir, "output.txt")
        if not os.path.exists(output_file):
            print(f"❌ Output file not found: {output_file}")
            print("💡 Create output.txt in the solution directory or specify output file path")
            sys.exit(1)
    
    # 提示安装colorama以获得更好的体验
    if not COLORS_AVAILABLE:
        print("💡 Tip: Install colorama for colored output: pip install colorama")
        print()
    
    print("🔧 LeetCode Universal Test Framework")
    print(f"Solution: {solution_file}")
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    print()
    
    tester = LeetCodeTester()
    
    # 读取解决方案代码
    try:
        with open(solution_file, 'r', encoding='utf-8') as f:
            solution_code = f.read()
        print("✓ Solution file loaded")
    except Exception as e:
        print(f"❌ Error reading solution file: {e}")
        sys.exit(1)
    
    # 解析解决方案
    if not tester.parse_solution_template(solution_code):
        print("❌ Failed to parse solution template")
        sys.exit(1)
    print("✓ Solution template parsed")
    
    # 解析测试用例
    tester.parse_input_file(input_file)
    tester.parse_output_file(output_file)
    print(f"✓ Test cases loaded: {len(tester.test_cases)} cases")
    
    # 运行测试
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()