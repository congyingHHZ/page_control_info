# -*- coding:utf-8 -*-
# @Time      : 2021/4/27 13:20
# @Author    : hml
# @File      : main.py
# @Software  : PyCharm
# @py_version: 3.9.1
# @desc      :获取当前运行软件的当前显示页面上的所有控件的text属性和resource_id属性

import uiautomator2 as u2

import adbutils
import re


class GetPageInfo:
    def __init__(self):
        self.dev = adbutils.adb.device_list()[0]
        self.dev_serial = self.dev.serial
        print(self.dev_serial)
        self.d = u2.connect_usb(self.dev_serial)
        self.swipe_max = 10
        self.swipe_count = 0
        self.win_size = self.d.window_size()
        self.reg = re.compile(r'text=\"(?P<text>\S*)\"\s+resource-id=\"(?P<resource_id>\S*)\"')
        self.get_package_name()
        self.session = self.d.session(self.curren_package, attach=True)

    def get_package_name(self):
        dumpsys_activity = self.dev.shell('dumpsys window')
        # print(dumpsys_activity)
        self.curren_package,self.activity = re.search(r"mCurrentFocus=Window{.+(com\.[\w\.]+)/(com\.[\w\.]+)}", dumpsys_activity).groups()
        # print(self.curren_package)
        # print(self.activity)

    def get_page_info(self):
        find_nodes = []
        print(self.curren_package)
        xml = self.session.dump_hierarchy()
        with open(f"xml{self.swipe_count}.txt","w+") as out_file:
            out_file.write(xml)
        dump_line = xml.split("\n")

        for line in dump_line:
            node = self.reg.search(line)
            if node and (node.group("text") or node.group("resource_id")):
                find_nodes.append(f"text='{node.group('text')}', resource_id='{node.group('resource_id')}')")

        self.session.swipe(self.win_size[0]/2,self.win_size[1]*2/3,self.win_size[0]/2,self.win_size[1]*1/3)

        self.swipe_count += 1

        xml_next = self.session.dump_hierarchy()
        if xml != xml_next and self.swipe_count < self.swipe_max:
            self.get_page_info()
        else:
            with open("node.txt","w+") as final_f:
                for i in sorted(set(find_nodes),key=find_nodes.index):
                    final_f.write(f"{i}\n")


if __name__ == '__main__':
    GetPageInfo().get_page_info()

