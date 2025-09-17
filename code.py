import board
import usb_hid
import usb_cdc
import time
import digitalio
from adafruit_hid.mouse import Mouse

# 初始化板载LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# 初始化HID鼠标
try:
    mouse = Mouse(usb_hid.devices)
except:
    mouse = None

# 全局变量
_serial = None
_serial_initialized = False

def init_serial():
    """初始化串口 - 只使用console通道"""
    global _serial, _serial_initialized
    
    if _serial_initialized:
        return _serial is not None
    
    # 直接使用console通道
    if usb_cdc.console is not None:
        if hasattr(usb_cdc.console, 'in_waiting') and hasattr(usb_cdc.console, 'write'):
            _serial = usb_cdc.console
            _serial_initialized = True
            return True
    
    return False

def get_serial():
    """获取串口对象 - 直接返回，无检查"""
    return _serial

def send_response(data):
    """发送响应数据 - 简化版本"""
    if _serial is None:
        return False
    
    try:
        _serial.write(data)
        _serial.flush()
        return True
    except:
        return False

def receive_data():
    """接收串口数据 - 简化版本"""
    if _serial is None:
        return None
    
    try:
        if _serial.in_waiting > 0:
            return _serial.read(_serial.in_waiting)
    except:
        pass
    return None

def parse_xy_data(data):
    """解析XY坐标数据 - 优化格式：数值,数值"""
    try:
        # 查找逗号位置
        comma_pos = data.find(b',')
        if comma_pos != -1:
            # 直接提取X和Y值，无前缀
            x_bytes = data[:comma_pos]
            y_bytes = data[comma_pos + 1:]
            
            # 转换为整数
            try:
                x = int(x_bytes)
                y = int(y_bytes)
                return x, y
            except ValueError:
                return None, None
        
        return None, None
            
    except:
        return None, None

def move_mouse(x, y):
    """移动鼠标 - 高性能版本，无阈值限制"""
    if mouse is None:
        return
    
    try:
        # 应用灵敏度
        move_x = int(x * 1.0)
        move_y = int(y * 1.0)
        
        # 直接移动，无阈值限制
        mouse.move(x=move_x, y=move_y)
    except:
        pass

def main_loop():
    """主功能循环 - 高性能版本"""
    while True:
        try:
            data = receive_data()
            
            if data:
                # 尝试解析为XY坐标
                x, y = parse_xy_data(data)
                if x is not None and y is not None:
                    move_mouse(x, y)
            
            # 最小延迟，提高响应速度
            time.sleep(0.001)  # 1毫秒延迟
            
        except Exception as e:
            # 错误时短暂等待，避免死循环
            time.sleep(0.01)
            print(f"错误: {e}")

def main():
    """主函数 - 直接进入主程序，无需握手"""
    # 等待USB稳定
    time.sleep(1)
    
    # 初始化串口
    if not init_serial():
        return
    
    # LED常亮，表示程序正在运行
    led.value = True
    print("Pico鼠标程序启动，LED常亮")
    
    # 直接进入主循环
    main_loop()

if __name__ == "__main__":
    main() 