# Pico Mouse - 树莓派Pico USB鼠标模拟器

一个基于树莓派Pico和CircuitPython的USB鼠标模拟器项目，支持通过串口通信控制鼠标移动。

## 🚀 项目特性

- **USB HID鼠标模拟**: 将Pico模拟为USB鼠标设备
- **串口通信控制**: 通过串口接收坐标数据控制鼠标移动
- **高性能响应**: 优化的代码结构，提供快速响应
- **跨平台支持**: 支持Windows、macOS和Linux系统
- **简单易用**: 简洁的命令格式，易于集成

## 📋 硬件要求

- 树莓派Pico (Raspberry Pi Pico)
- USB Type-C数据线
- 电脑（支持USB HID设备）

## 🛠️ 软件要求

- CircuitPython 9.2.8 或更高版本
- Python 3.6+ (用于测试脚本)

## 📁 项目结构

```
pico-mouse/
├── boot.py                    # USB配置和初始化
├── code.py                    # 主程序逻辑
├── test_windows.py            # Windows测试脚本
├── lib/                       # CircuitPython库文件
│   └── adafruit_hid/         # HID设备支持库
└── README.md                  # 项目说明文档
```

## 🔧 安装步骤

### 1. 刷入CircuitPython

1. 下载 [CircuitPython固件](https://circuitpython.org/board/raspberry_pi_pico/)
2. 按住Pico上的BOOTSEL按钮并插入USB
3. 将下载的`.uf2`文件复制到出现的RPI-RP2驱动器
4. Pico将自动重启并运行CircuitPython

### 2. 安装依赖库

1. 下载 [Adafruit HID库](https://github.com/adafruit/Adafruit_CircuitPython_HID)
2. 将库文件复制到Pico的`lib/`目录

### 3. 部署项目文件

1. 将`boot.py`和`code.py`复制到Pico的根目录
2. 将`test_windows.py`复制到您的电脑上用于测试

## 📖 使用方法

### 基本操作

1. 将Pico连接到电脑
2. Pico将自动识别为USB鼠标设备
3. 通过串口发送坐标数据控制鼠标移动

### 命令格式

鼠标移动命令采用简单的格式：`X,Y`

- `X`: X轴移动距离（正数向右，负数向左）
- `Y`: Y轴移动距离（正数向下，负数向上）
- 示例：
  - `50,0` - 向右移动50像素
  - `0,50` - 向下移动50像素
  - `-30,-30` - 向左上移动30像素

### 测试鼠标功能

使用提供的测试脚本：

```bash
python test_windows.py
```

脚本将：
1. 自动检测Pico设备
2. 建立串口连接
3. 执行一系列鼠标移动测试
4. 显示测试结果

## ⚙️ 配置说明

### boot.py 配置

- 禁用USB存储设备
- 启用USB HID鼠标功能
- 启用CDC串口通信（仅console通道）
- 禁用文件系统写入

### code.py 功能

- 串口通信初始化
- 坐标数据解析
- 鼠标移动控制
- 错误处理和恢复

## 🔍 故障排除

### 常见问题

1. **设备未识别**
   - 检查USB连接
   - 确认CircuitPython已正确刷入
   - 重新插拔USB连接

2. **串口连接失败**
   - 检查串口号设置
   - 确认波特率设置为115200
   - 关闭其他可能占用串口的程序

3. **鼠标移动异常**
   - 检查坐标数据格式
   - 确认HID库正确安装
   - 重启Pico设备

### 调试信息

程序运行时会输出调试信息：
- USB配置状态
- 串口连接状态
- 错误信息（如有）

## 📝 开发说明

### 代码结构

- **模块化设计**: 功能分离，易于维护
- **错误处理**: 完善的异常处理机制
- **性能优化**: 最小化延迟，提高响应速度

### 扩展功能

可以轻松添加的功能：
- 鼠标点击支持
- 滚轮控制
- 键盘模拟
- 自定义灵敏度设置

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进项目！

## 📄 许可证

本项目采用MIT许可证。

## 🙏 致谢

- [CircuitPython](https://circuitpython.org/) - 优秀的Python嵌入式平台
- [Adafruit](https://www.adafruit.com/) - HID库支持
- [树莓派基金会](https://www.raspberrypi.org/) - Pico硬件平台

## 📞 联系方式

如有问题或建议，请通过GitHub Issues联系。

---

**注意**: 本项目仅供学习和研究使用，请遵守相关法律法规。 