import configparser
import signal
import subprocess
import platform
import traceback
import re
from stop_and_run_uiautomator import rerun_uiautomator2

def get_OS_type():
    sys_platform = platform.platform().lower()
    os_type = ''
    if "windows" in sys_platform:
        os_type = 'win'
    elif "darwin" in sys_platform or 'mac' in sys_platform:
        os_type = 'mac'
    elif "linux" in sys_platform:
        os_type = 'linux'
    else:
        print('Unknown OS,regard as linux...')
        os_type = 'linux'
    return os_type


def clear_app_cache(app_package_name):
    print('正在清除应用包名为{}的数据。。。'.format(app_package_name))
    execute_cmd_with_timeout('adb shell pm clear {}'.format(app_package_name))
    print('清除完毕。')


def execute_cmd_with_timeout(cmd, timeout=600):
    p = subprocess.Popen(cmd, stderr=subprocess.STDOUT, shell=True)
    try:
        p.wait(timeout)
    except subprocess.TimeoutExpired:
        p.send_signal(signal.SIGINT)
        p.wait()


def get_config_settings(config_file):
    config = configparser.ConfigParser()
    config.read(config_file, encoding='utf-8')
    pairs = []
    for section in config.sections():
        pairs.extend(config.items(section))
    dic = {}
    for key, value in pairs:
        dic[key] = value
    return dic


if __name__ == '__main__':
    config_settings = get_config_settings('config.ini')

    with open('apk_pkgName.txt', 'r', encoding='utf-8') as f:
        content = f.readlines()
    pkgName_appName_list = [item.rstrip('\n') for item in content]
    os_type = get_OS_type()
    # 运行之前，kill掉所有的后台程序,先弃用该逻辑
    # if os_type == 'win':
    #     execute_cmd_with_timeout("powershell.exe .\\kill_all_background_apps.ps1")
    # elif os_type in ['linux','mac']:
    #     execute_cmd_with_timeout("sed -i 's/\r$//' kill_all_background_apps.sh")
    #     execute_cmd_with_timeout("bash kill_all_background_apps.sh")
    for pkgName_appName in pkgName_appName_list:
        # print(pkgName_appName)
        if pkgName_appName.startswith('#'):
            print(pkgName_appName + 'is ignored,continue...')
            continue
        if len(pkgName_appName) < 3:
            continue
        try:
            print('content of pkgName_appName',pkgName_appName)
            pkgName, appName = pkgName_appName.split(' | ')
            appName = appName.strip('\'')
            if config_settings['clear_cache'] == 'true':
                clear_app_cache(pkgName)
            if config_settings['rerun_uiautomator2'] == 'true':
                rerun_uiautomator2()
            print('analysis {} : {}now...'.format(pkgName, appName))
            if os_type in ['linux', 'mac']:
                execute_cmd_with_timeout(
                    'python3 run.py {} {} {} {} {} {}'.format(pkgName, appName, config_settings['dynamic_ui_depth'],
                    config_settings['dynamic_run_time'],config_settings['searchprivacypolicy'],
                    config_settings['screenuidrep']),timeout=int(config_settings['dynamic_run_time']) + 120)
                # kill current app
            elif os_type == 'win':
                    execute_cmd_with_timeout(
                    'python run.py {} {} {} {} {} {}'.format(pkgName, appName, config_settings['dynamic_ui_depth'],
                    config_settings['dynamic_run_time'],config_settings['searchprivacypolicy'],
                    config_settings['screenuidrep']),timeout=int(config_settings['dynamic_run_time']) + 120)
            print(f'kill {pkgName} in try...')
            execute_cmd_with_timeout(f'adb shell am force-stop {pkgName}')

        except Exception as e:
            print(e)
            # 打印详细的异常信息
            traceback.print_exc()
            print('error occurred, continue...')
            print(f'kill {pkgName} in exception...')
            execute_cmd_with_timeout(f'adb shell am force-stop {pkgName}')
