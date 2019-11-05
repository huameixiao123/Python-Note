
import pyautogui as gui
import time

find_window = gui.getWindowsAt(0 , 0)
print(find_window)


# 体程序句柄对象的字典，key为窗体程序title，value为hwnd对象
# gui.Window(gui.getWindows().get('Python数据分析交流群')).set_foreground()
# Window使用hwnd对象创建window对象，对窗体程序进行控制
# 这一部分在提供的官方api文档里并没有提到，这是作者故意没有提及的窗体程序句柄处理，才对win api封装了几个功能
# for i in range(10):
#     gui.typewrite(time.asctime() + ' : ' + str(i))  # typewrite可以参考文档，实际是模拟键盘输入，所以当这里的内容换成中文时，是无效的
#     gui.hotkey('ctrl', 'enter')  # hotkey模拟组合键
#     time.sleep(10)


