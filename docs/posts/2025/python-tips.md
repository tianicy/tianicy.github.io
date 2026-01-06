---
title: Python 开发实用技巧汇总
date: 2025-11-01
category: backends
tags: ['python']
reading_time: 10
pin: true
---

# Python 开发实用技巧汇总

整理日常开发中常用的 Python 技巧，提升编码效率和代码质量。

## 1. 列表推导式

### 基础用法

```python
# 传统方式
squares = []
for i in range(10):
    squares.append(i ** 2)

# 列表推导式
squares = [i ** 2 for i in range(10)]
```

### 带条件的推导

```python
# 筛选偶数
evens = [i for i in range(10) if i % 2 == 0]

# 三元表达式
result = [i if i % 2 == 0 else -i for i in range(10)]
```

## 2. 字典技巧

### 字典合并（Python 3.9+）

```python
dict1 = {'a': 1, 'b': 2}
dict2 = {'c': 3, 'd': 4}

# 使用 | 运算符
merged = dict1 | dict2

# 使用 |= 更新
dict1 |= dict2
```

### 默认值处理

```python
# 使用 get() 方法
value = data.get('key', 'default')

# 使用 defaultdict
from collections import defaultdict
d = defaultdict(list)
d['key'].append(1)  # 不会报错
```

## 3. 上下文管理器

### 自定义上下文管理器

```python
from contextlib import contextmanager

@contextmanager
def timing(name):
    import time
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        print(f'{name} took {end - start:.2f}s')

# 使用
with timing('operation'):
    # 你的代码
    pass
```

## 4. 装饰器模式

### 函数装饰器

```python
import functools
import time

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'{func.__name__} took {end - start:.2f}s')
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
```

### 带参数的装饰器

```python
def retry(times=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == times - 1:
                        raise
                    print(f'Retry {i + 1}/{times}')
        return wrapper
    return decorator

@retry(times=5)
def unstable_function():
    pass
```

## 5. 生成器表达式

### 节省内存

```python
# 列表推导（占用内存）
squares_list = [i ** 2 for i in range(1000000)]

# 生成器表达式（按需计算）
squares_gen = (i ** 2 for i in range(1000000))

# 使用
for square in squares_gen:
    print(square)
```

## 6. 数据类

### 使用 dataclass（Python 3.7+）

```python
from dataclasses import dataclass, field

@dataclass
class User:
    name: str
    age: int
    email: str = ''
    tags: list = field(default_factory=list)
    
    def __post_init__(self):
        if not self.email:
            self.email = f'{self.name}@example.com'

user = User('Alice', 30)
print(user)  # User(name='Alice', age=30, email='Alice@example.com', tags=[])
```

## 7. 类型提示

### 基础类型提示

```python
from typing import List, Dict, Optional, Union

def process_items(items: List[str]) -> Dict[str, int]:
    return {item: len(item) for item in items}

def get_user(user_id: int) -> Optional[Dict[str, str]]:
    # 可能返回 None
    pass
```

## 8. 路径操作

### 使用 pathlib（推荐）

```python
from pathlib import Path

# 创建路径
path = Path('data') / 'file.txt'

# 检查存在
if path.exists():
    content = path.read_text()

# 遍历目录
for file in Path('data').glob('*.txt'):
    print(file.name)
```

## 9. 并发处理

### 使用 concurrent.futures

```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# 线程池（I/O 密集型）
with ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(download_file, urls)

# 进程池（CPU 密集型）
with ProcessPoolExecutor(max_workers=4) as executor:
    results = executor.map(process_data, data_list)
```

## 10. 优雅的错误处理

### 使用 else 和 finally

```python
try:
    result = risky_operation()
except ValueError as e:
    print(f'Error: {e}')
except Exception as e:
    print(f'Unexpected error: {e}')
else:
    # 没有异常时执行
    print('Success!')
finally:
    # 总是执行
    cleanup()
```

## 总结

这些技巧可以让你的 Python 代码更加简洁、高效和 Pythonic。记住：**简单优于复杂，可读性很重要**。
