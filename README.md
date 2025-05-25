# LUTF (LeetCode Universal Test Framework)

> For Python3

一个无感的、通用的 LeetCode 题目测试框架，支持自动化测试各种类型的 LeetCode 解题方案。

<img width="1214" alt="image" src="https://github.com/user-attachments/assets/0d101707-7986-45bd-906f-c278255a53c6" />


## ✨ 特性

- 🚀 **通用测试框架**：支持函数类和设计类题目
- 🌈 **彩色输出**：美观的测试结果显示（支持 colorama）
- ⏱️ **性能测量**：精确的执行时间统计
- 🔍 **智能 Diff**：详细的期望值与实际值对比
- 🌳 **数据结构支持**：自动处理二叉树、链表等复杂数据结构
- 📁 **智能文件查找**：自动在解决方案目录查找测试文件
- 📊 **详细统计**：完整的测试通过率和性能报告

## 📦 安装依赖

```bash
# 基础依赖（Python 标准库）
pip install colorama  # 可选，用于彩色输出
```

## 🚀 使用方法

### 基本用法

```bash
# 方式1：自动查找测试文件（推荐）
python leetcode_tester.py solution.py

# 方式2：指定输入文件，自动查找输出文件
python leetcode_tester.py solution.py input.txt

# 方式3：指定所有文件
python leetcode_tester.py solution.py input.txt output.txt
```

### 文件结构

```
your_problem_folder/
├── solution.py      # 你的解决方案
├── input.txt        # 测试输入数据
└── output.txt       # 期望输出结果
```

## 📝 文件格式

### solution.py
```python
# 标准 LeetCode 解决方案格式
class Solution:
    def yourMethod(self, param1, param2):
        # 你的解决方案
        return result
```

### input.txt
```
# 每行一个输入参数，空行分割测试用例
[1,2,3]
"hello"

[4,5,6]
"world"
```

### output.txt
```
# 每行一个期望输出，空行分割测试用例
6

10
```

## 🌟 支持的数据类型

- ✅ **基本类型**：整数、浮点数、字符串、布尔值
- ✅ **容器类型**：列表、字典、元组
- ✅ **二叉树**：自动转换列表格式 `[1,2,3,null,null,4,5]`
- ✅ **链表**：自动转换数组格式 `[1,2,3,4,5]`
- ✅ **设计类题目**：如 `MedianFinder`、`LRUCache` 等

## 🎨 输出示例

```
🔧 LeetCode Universal Test Framework
Solution: /path/to/solution.py
Input: /path/to/input.txt
Output: /path/to/output.txt

✓ Solution file loaded
✓ Solution template parsed
✓ Test cases loaded: 3 cases

🚀 Running 3 test cases...
------------------------------------------------------------

Test Case 1:
Input: [[1, 2, 3, null, null, 4, 5]]
Output: 6
Time: 0.12ms
Result: ✓ PASS

Test Case 2:
Input: [[1, -2, 3]]
Output: 3
Time: 0.08ms
Result: ✓ PASS

Test Case 3:
Input: [[-10]]
Output: -10
Time: 0.05ms
Result: ✓ PASS

============================================================
🎉 All tests passed! (3/3)
============================================================
```

## 🔧 高级功能

### 自动类型推断
框架会根据参数名自动推断数据类型：
- 包含 `tree`、`root` 的参数 → 二叉树
- 包含 `list` 的参数 → 可能是链表
- 其他参数 → 保持原始类型

### 设计类题目支持
```python
# 输入格式
[["MedianFinder", "addNum", "addNum", "findMedian"], [[], [1], [2], []]]

# 输出格式
[null, null, null, 1.5]
```

### 性能监控
- 🟢 绿色：< 1ms（优秀）
- 🟡 黄色：1-10ms（良好）
- 🔴 红色：> 10ms（需要优化）

## 🛠️ 配置选项

### 环境变量
```bash
# 禁用彩色输出
export NO_COLOR=1

# 设置时区
export TZ=Asia/Shanghai
```

### 自定义颜色主题
可以通过修改 `color_map` 来自定义颜色方案。

## 📋 支持的题目类型

| 题目类型 | 支持状态 | 示例 |
|---------|---------|------|
| 数组/字符串 | ✅ 完全支持 | Two Sum, Reverse String |
| 链表 | ✅ 完全支持 | Add Two Numbers, Merge Lists |
| 二叉树 | ✅ 完全支持 | Binary Tree Traversal |
| 图算法 | ✅ 完全支持 | Course Schedule |
| 动态规划 | ✅ 完全支持 | Climbing Stairs |
| 设计类 | ✅ 完全支持 | LRU Cache, Trie |

## 🐛 故障排除

### 常见问题

1. **找不到测试文件**
   ```
   ❌ Input file not found: input.txt
   💡 Create input.txt in the solution directory
   ```

2. **解析错误**
   ```
   ❌ Failed to parse solution template
   ```
   检查 Python 语法是否正确

3. **导入错误**
   ```
   💡 Tip: Install colorama for colored output
   ```

### 调试模式
在代码中添加调试信息：
```python
# 在 solution.py 开头添加
import sys
print(f"Debug: {sys.argv}", file=sys.stderr)
```

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 项目
2. 创建特性分支
3. 提交变更
4. 推送到分支
5. 创建 Pull Request

## 📄 许可证

MIT License - 详见 LICENSE 文件

## 🙏 致谢

- [LeetCode](https://leetcode.com/) - 提供优质的算法题目
- [colorama](https://pypi.org/project/colorama/) - 跨平台彩色终端输出
- Python 社区 - 强大的标准库支持

---

**Happy Coding! 🎉**
