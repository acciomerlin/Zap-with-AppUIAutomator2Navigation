import json
import os
import subprocess
import time
from zapv2 import ZAPv2
from datetime import datetime


class ZapApi(object):
    def __init__(self):
        self.zap = None  # an instance of the ZAP api client.
        self.zap_path = r"C:\Program Files\ZAP\Zed Attack Proxy\zap.bat"  # 换成自己的 ZAP 安装路径
        self.apikey = r'ig5oq0c6amjo4s62okbjl2nbfb'  # Change to match the API key set in ZAP, or use None if the API key is disabled

    def start(self):
        """
        启动 ZAP 应用程序
        """
        subprocess.Popen([self.zap_path], cwd=os.path.dirname(self.zap_path))
        # 等待 ZAP 完全启动并监听代理端口
        time.sleep(12)  # 根据你的系统调整这个时间
        self.zap = ZAPv2(apikey=self.apikey, proxies={'http': 'http://192.168.1.222:9999'})

    def stop_without_save(self):
        """
        关闭ZAP，不保存结果
        """
        if self.zap:
            self.zap.core.shutdown()
            print("ZAP 已关闭。")

    def stop_with_save(self, pkgName=''):
        """
        关闭ZAP，保存结果
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        result_dir = 'zap_results/'
        os.makedirs(result_dir, exist_ok=True)

        # 获取所有警报, 并将警报保存到 JSON 文件
        try:
            alerts = self.zap.core.alerts()
            alerts_file_path = os.path.join(result_dir, f'zap_alerts_{pkgName}_{timestamp}.json')
            with open(alerts_file_path, 'w') as json_file:
                json.dump(alerts, json_file, indent=4)
            print(f"所有警报已保存到 '{alerts_file_path}' 文件中。")
        except Exception as e:
            print(f"导出警报 JSON 文件时出错: {e}\n")

        # 导出 对各站点警报总结 JSON 文件
        try:
            json_report = self.zap.core.jsonreport()
            json_file_path = os.path.join(result_dir, f'zap_sitelog_{pkgName}_{timestamp}.json')
            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                json_file.write(json_report)
            print(f"所有对各站点警报总结数据已保存到 '{json_file_path}' 文件中。")
        except Exception as e:
            print(f"导出各站点 JSON 文件时出错: {e}\n")

        # 导出 HTTP/HTTPS 请求与响应的 HAR 文件
        try:
            har_content = self.zap.core.messages_har()
            har_file_path = os.path.join(result_dir, f'zap_https_{pkgName}_{timestamp}.har')
            with open(har_file_path, 'w', encoding='utf-8') as har_file:
                har_file.write(har_content)
            print(f"所有HTTP/HTTPS 请求与响应数据已保存到 '{har_file_path}' 文件中。")
        except Exception as e:
            print(f"导出 HAR 文件时出错: {e}\n")

        if self.zap:
            self.zap.core.shutdown()
            print("ZAP 已关闭。")


# test
if __name__ == '__main__':
    zap_api = ZapApi()
    zap_api.start()
    # browserTest
    firefox_path = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'  # Firefox 安装路径
    os.startfile(firefox_path)
    time.sleep(7)
    zap_api.stop_with_save('firefox')
