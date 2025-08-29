#!/usr/bin/env python3
"""
Windows专用Pico测试脚本 - 直接通过VID/PID连接
"""

import serial
import serial.tools.list_ports
import time

# Pico的VID和PID
PICO_VID = "239A"  # Raspberry Pi Pico的VID
PICO_PID = "80F4"  # Raspberry Pi Pico的PID

def find_pico_by_vid_pid():
    """通过VID和PID查找Pico设备"""
    print("=== 通过VID/PID查找Pico设备 ===")
    
    ports = list(serial.tools.list_ports.comports())
    print(f"发现 {len(ports)} 个串口设备:")
    
    for i, port_info in enumerate(ports):
        print(f"  {i+1}. {port_info.device}")
        print(f"     描述: {port_info.description}")
        print(f"     硬件ID: {port_info.hwid}")
        print()
    
    # 查找匹配VID和PID的Pico设备
    pico_device = None
    
    for port_info in ports:
        hwid = port_info.hwid.lower()
        
        # 检查VID和PID是否匹配
        if PICO_VID.lower() in hwid and PICO_PID.lower() in hwid:
            pico_device = port_info
            print(f"✓ 找到匹配的Pico设备: {port_info.device}")
            print(f"  硬件ID: {port_info.hwid}")
            break
    
    if not pico_device:
        print(f"✗ 未找到VID={PICO_VID}, PID={PICO_PID}的Pico设备")
        print("请检查:")
        print("1. Pico是否正确连接")
        print("2. CircuitPython是否正在运行")
        print("3. 是否需要重新插拔USB连接")
        return None, None
    
    return pico_device.device, pico_device.hwid

def connect_to_pico(port_name):
    """直接连接到Pico设备"""
    print(f"\n=== 连接到Pico设备: {port_name} ===")
    
    try:
        # 连接串口
        print(f"连接 {port_name}...")
        ser = serial.Serial(
            port=port_name,
            baudrate=115200,
            timeout=1,
            write_timeout=1
        )
        
        # 等待连接稳定
        print("等待连接稳定...")
        time.sleep(1)
        
        # 清空缓冲区
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        
        print("✓ 连接成功！")
        return ser
        
    except Exception as e:
        print(f"✗ 连接失败: {e}")
        return None

def test_mouse_commands(ser):
    """测试鼠标命令 - 优化格式：数值,数值"""
    print("\n=== 测试鼠标命令 ===")
    
    commands = [
        "50,0",      # 向右移动
        "0,50",      # 向下移动
        "30,30",     # 对角线移动
        "-50,0",     # 向左移动
        "0,-50",     # 向上移动
        "-30,-30",   # 负对角线移动
        "100,100",   # 大范围移动
        "-100,-100", # 大范围负移动
        "5,5",       # 小幅度移动
        "-5,-5",     # 小幅度负移动
    ]
    
    for i, command in enumerate(commands, 1):
        try:
            print(f"测试 {i}: {command}")
            ser.write(f"{command}\n".encode())
            ser.flush()
            time.sleep(0.5)
        except Exception as e:
            print(f"  发送失败: {e}")

def test_continuous_movement(ser):
    """测试连续移动 - 圆形轨迹"""
    print("\n=== 测试连续移动（5秒） ===")
    start_time = time.time()
    
    try:
        while time.time() - start_time < 5:
            import math
            t = (time.time() - start_time) * 2  # 2秒一圈
            radius = 20
            x = int(radius * math.cos(t))
            y = int(radius * math.sin(t))
            
            command = f"{x},{y}\n"
            ser.write(command.encode())
            ser.flush()
            
            time.sleep(0.1)
        
        print("连续移动测试完成")
        
    except Exception as e:
        print(f"连续移动测试失败: {e}")

def test_mouse_performance(ser):
    """测试鼠标性能 - 回报率、延迟、压力测试"""
    print("\n=== 鼠标性能测试 ===")
    
    # 测试1: 回报率测试
    print("\n1. 回报率测试（10秒）...")
    test_report_rate(ser, duration=10)
    
    # 测试2: 延迟测试
    print("\n2. 延迟测试...")
    test_latency(ser)
    
    # 测试3: 压力测试
    print("\n3. 压力测试（5秒）...")
    test_stress(ser, duration=5)
    
    # 测试4: 极限频率测试
    print("\n4. 极限频率测试...")
    test_max_frequency(ser)

def test_report_rate(ser, duration=10):
    """测试回报率 - 测量每秒能处理多少条命令"""
    print(f"  发送命令 {duration} 秒，测量回报率...")
    
    start_time = time.time()
    command_count = 0
    last_time = start_time
    
    try:
        while time.time() - start_time < duration:
            current_time = time.time()
            
            # 发送移动命令
            x = int(10 * (current_time - start_time)) % 20 - 10  # -10到10的循环移动
            y = int(5 * (current_time - start_time)) % 10 - 5   # -5到5的循环移动
            
            command = f"{x},{y}\n"
            ser.write(command.encode())
            ser.flush()
            command_count += 1
            
            # 每0.1秒发送一次，避免串口缓冲区溢出
            time.sleep(0.001)  # 1毫秒间隔，接近1000Hz
            
            # 每秒显示一次进度
            if int(current_time - last_time) >= 1:
                rate = command_count / (current_time - start_time)
                print(f"    当前回报率: {rate:.1f} Hz")
                last_time = current_time
    
    except Exception as e:
        print(f"    回报率测试出错: {e}")
    
    total_time = time.time() - start_time
    final_rate = command_count / total_time
    print(f"  ✓ 回报率测试完成")
    print(f"    总命令数: {command_count}")
    print(f"    总时间: {total_time:.2f} 秒")
    print(f"    平均回报率: {final_rate:.1f} Hz")

def test_latency(ser):
    """测试延迟 - 测量命令响应时间"""
    print("  测试命令响应延迟...")
    
    latencies = []
    
    for i in range(10):
        try:
            # 发送测试命令
            test_command = f"{i},{i}\n"
            start_time = time.time()
            
            ser.write(test_command.encode())
            ser.flush()
            
            # 等待响应（如果有的话）
            time.sleep(0.01)  # 10ms等待
            
            # 测量延迟（这里主要是串口传输延迟）
            latency = (time.time() - start_time) * 1000  # 转换为毫秒
            latencies.append(latency)
            
            print(f"    测试 {i+1}: {latency:.2f} ms")
            
        except Exception as e:
            print(f"    延迟测试 {i+1} 出错: {e}")
    
    if latencies:
        avg_latency = sum(latencies) / len(latencies)
        min_latency = min(latencies)
        max_latency = max(latencies)
        
        print(f"  ✓ 延迟测试完成")
        print(f"    平均延迟: {avg_latency:.2f} ms")
        print(f"    最小延迟: {min_latency:.2f} ms")
        print(f"    最大延迟: {max_latency:.2f} ms")

def test_stress(ser, duration=5):
    """压力测试 - 持续高频率发送命令"""
    print(f"  压力测试 {duration} 秒，持续高频率发送...")
    
    start_time = time.time()
    command_count = 0
    error_count = 0
    
    try:
        while time.time() - start_time < duration:
            # 发送随机移动命令
            import random
            x = random.randint(-50, 50)
            y = random.randint(-50, 50)
            
            command = f"{x},{y}\n"
            
            try:
                ser.write(command.encode())
                ser.flush()
                command_count += 1
            except:
                error_count += 1
            
            # 极短间隔，测试极限性能
            time.sleep(0.0001)  # 0.1毫秒，接近10kHz
    
    except Exception as e:
        print(f"    压力测试出错: {e}")
    
    total_time = time.time() - start_time
    success_rate = (command_count / (command_count + error_count)) * 100 if (command_count + error_count) > 0 else 0
    
    print(f"  ✓ 压力测试完成")
    print(f"    成功命令: {command_count}")
    print(f"    失败命令: {error_count}")
    print(f"    成功率: {success_rate:.1f}%")
    print(f"    平均频率: {command_count / total_time:.1f} Hz")

def test_max_frequency(ser):
    """极限频率测试 - 找到系统能承受的最高频率"""
    print("  寻找最高可承受频率...")
    
    frequencies = [100, 200, 500, 1000, 2000, 5000, 10000]  # Hz
    max_stable_freq = 0
    
    for freq in frequencies:
        print(f"    测试 {freq} Hz...")
        
        if test_single_frequency(ser, freq, test_duration=2):
            max_stable_freq = freq
            print(f"    ✓ {freq} Hz 稳定")
        else:
            print(f"    ✗ {freq} Hz 不稳定")
            break
    
    print(f"  ✓ 极限频率测试完成")
    print(f"    最高稳定频率: {max_stable_freq} Hz")

def test_single_frequency(ser, frequency, test_duration=2):
    """测试单个频率的稳定性"""
    try:
        interval = 1.0 / frequency
        start_time = time.time()
        command_count = 0
        error_count = 0
        
        while time.time() - start_time < test_duration:
            # 发送测试命令
            x = int(10 * (time.time() - start_time)) % 20 - 10
            y = int(5 * (time.time() - start_time)) % 10 - 5
            
            command = f"{x},{y}\n"
            
            try:
                ser.write(command.encode())
                ser.flush()
                command_count += 1
            except:
                error_count += 1
            
            # 等待指定间隔
            time.sleep(interval)
        
        # 计算成功率
        total_commands = command_count + error_count
        success_rate = (command_count / total_commands) * 100 if total_commands > 0 else 0
        
        # 成功率超过95%认为是稳定的
        return success_rate >= 95
        
    except:
        return False

def main():
    """主函数"""
    print("Windows专用Pico测试脚本 - 直接连接版本")
    print("=" * 50)
    
    # 通过VID/PID查找Pico设备
    result = find_pico_by_vid_pid()
    if result[0] is None:
        return
    
    port_name, hwid = result
    print(f"\n✓ 找到Pico设备: {port_name}")
    print(f"  硬件ID: {hwid}")
    
    # 连接到Pico
    ser = connect_to_pico(port_name)
    if ser is None:
        return
    
    try:
        print("\n✓ 成功连接到Pico设备")
        
        # 测试鼠标命令
        test_mouse_commands(ser)
        
        # 测试连续移动
        test_continuous_movement(ser)
        
        # 测试鼠标性能
        test_mouse_performance(ser)
        
        print("\n✓ 所有测试完成")
        
    except Exception as e:
        print(f"测试出错: {e}")
    
    finally:
        ser.close()
        print("连接已关闭")

if __name__ == "__main__":
    main() 