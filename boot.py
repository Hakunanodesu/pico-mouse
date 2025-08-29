# boot.py -- 配置USB功能
import usb_hid
import usb_cdc
import storage

# 隐藏USB存储设备（不显示盘符）
storage.disable_usb_drive()

# 启用USB HID设备（鼠标）
usb_hid.enable((usb_hid.Device.MOUSE,))

# 启用USB CDC串口通信 - 只启用console通道
usb_cdc.enable(console=True, data=False)

# 完全禁用文件系统写入，进一步隐藏设备
storage.remount("/", True)

print("USB配置完成：HID鼠标 + CDC console")
print(f"CDC console: {usb_cdc.console}")
print(f"CDC data: {usb_cdc.data}") 