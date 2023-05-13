from uiautomator2 import Device
import xml.etree.ElementTree as ET
import time
import hashlib
import re

system_view = [
    "com.android.systemui",
    "com.android.launcher",
    "com.google.android.apps.nexuslauncher",
    "com.android.settings",
    "com.google.android.googlequicksearchbox",
    "com.google.android.gms",
    "com.google.android.inputmethod.latin",
    "com.android.chrome"
]


# 获取当前界面所有的可点击组件的文本内容，如果该节点可点但没有文本
# 那大概率文本存在其子节点上
def get_screen_all_text(d):
    text = ""
    xml = d.dump_hierarchy()
    root = ET.fromstring(xml)   
    for element in root.findall('.//node'):
        if element.get('clickable') == 'true':
            if element.get("package") not in system_view:
                temp_text = element.get("text")
                if temp_text:
                    text += temp_text + " "
                    # print(temp_text)
                else:
                    text += traverse_tree(element)
    return text

def get_screen_all_text_from_dict(clickable_eles, ele_uid_map):
    text = ""
    for ele_uid in clickable_eles:
        ele_dict = ele_uid_map[ele_uid]
        text += ele_dict.get("text")
    return text

# 递归遍历节点的所有子节点
def traverse_tree(node):
    text = ""
    if node is None:
        return text
    if node.get("text"):
        text += node.get("text")
        # print(node.get("text"))
        return text
    for child in node:
        text += traverse_tree(child)
    return text

# screen_info = package_name + activity_name + screen_all_text
def get_screen_info(d) :
    current_screen = d.current_app()
    pkg_name = current_screen['package']
    act_name = current_screen['activity']
    all_text = get_screen_all_text(d)
    all_info = pkg_name + '\n' + act_name + '\n' + all_text
    return pkg_name, act_name, all_text, all_info


# 从screen_map里得到取出和screen_text满足相似度阈值且相似度最高的screen_node
def get_screennode_from_screenmap(screen_map:dict, screen_text:str, screen_compare_strategy):
    if screen_map.get(screen_text, False) is False:
        # 如果没有,则遍历找满足相似度阈值的 
        max_similarity = 0
        res_node = None
        for candidate_screen_text in screen_map.keys():
            simi_flag, cur_similarity = screen_compare_strategy.compare_screen(screen_text, candidate_screen_text)
            if simi_flag is True:
                if cur_similarity > max_similarity:
                    max_similarity = cur_similarity
                    res_node = screen_map.get(candidate_screen_text)
        # 返回的要么是None, 要么是相似性最大的screen_node
        return res_node

    # 说明该节点之前存在screen_map
    else:
        return screen_map.get(screen_text)

# def get_screennode_from_diffmap(diff_map: dict, screen_map, screen_compare_strategy):
#     for screen_text in diff_map.keys():
#         res = get_screennode_from_screenmap(screen_map, screen_text, screen_compare_strategy)
#         if res is not None:
#             return res
#     return None

# # 对screen_info进行sha256签名,生成消息摘要
# def get_signature(screen_info):
#     signature = hashlib.sha256(screen_info.encode()).hexdigest()
#     return signature

# 获取当前界面所有可点击的组件
def get_clickable_elements(d, ele_uid_map, activity_name):
    xml = d.dump_hierarchy()
    root = ET.fromstring(xml)
    clickable_elements = []
    # cnt = 0
    for element in root.findall('.//node'):
        if element.get('clickable') == 'true':
            if element.get("package") not in system_view:
                # cnt +=1
                # uid = get_unique_id(d, element, activity_name)
                # ele_uid_map[uid] = element
                clickable_ele_dict = get_dict_clickable_ele(d, element, activity_name)
                uid = get_unique_id(d, clickable_ele_dict, activity_name)
                ele_uid_map[uid] = clickable_ele_dict

                # 把有隐私的组件增加到前面
                if is_privacy_information_in_ele_dict(clickable_ele_dict):
                    clickable_elements.insert(0, uid)
                else:
                    clickable_elements.append(uid)
    return clickable_elements

def is_privacy_information_in_ele_dict(clickable_ele_dict):
    text = clickable_ele_dict["text"]
    single_word_privacy_information = ["我", "我的", "编辑资料", "编辑材料"]
    for sip_info in single_word_privacy_information:
        if sip_info == text:
            return True

    privacy_information = ["设置", "账号", "个人"]
    for p_info in privacy_information:
        if p_info in text:
            return True
    return False

# 优化: 若clickable_eles中存在连续k个相同的ele,合并为1个,不用每个都点击
def merge_same_clickable_elements(k, clickable_eles:list, ele_uid_map) -> list:
    l = 0
    r = 0
    cnt = 0
    res = []
    while l < len(clickable_eles):
        cnt = 1
        r = l + 1
        while r < len(clickable_eles):
            if is_same_two_clickable_eles(clickable_eles[l], clickable_eles[r], ele_uid_map):
                cnt +=1
                r +=1
            else:
                break
        if cnt > k:
            res.append(clickable_eles[l])
        else:
            for i in range(cnt):
                res.append(clickable_eles[l])
                l+=1
        l = r
    return res

# 进行合并,对于选择国家和地区的场景,进行优化
def get_merged_clickable_elements(d, ele_uid_map, activity_name):
    clickable_eles = get_clickable_elements(d, ele_uid_map, activity_name)

    pre_len = len(clickable_eles)
    k = 6
    if len(clickable_eles) < 6:
        return clickable_eles, 0
    merged_clickable_eles = merge_same_clickable_elements(k, clickable_eles, ele_uid_map)
    after_len = len(merged_clickable_eles)

    return merged_clickable_eles, pre_len - after_len


def is_same_two_clickable_eles(ele1_uid, ele2_uid, ele_uid_map) -> bool:
    if isinstance(ele1_uid, int) and isinstance(ele2_uid, int):
        return ele1_uid == ele2_uid
    else:
        ele1_dict = ele_uid_map[ele1_uid]
        ele2_dict = ele_uid_map[ele2_uid]

        class_name1 = ele1_dict.get("class")
        res_id1 = ele1_dict.get("resource-id")
        pkg_name1 = ele1_dict.get("package")

        class_name2 = ele2_dict.get("class")
        res_id2 = ele2_dict.get("resource-id")
        pkg_name2 = ele2_dict.get("package")

        if class_name1 == class_name2 and \
            res_id1 == res_id2 and pkg_name1 == pkg_name2:
            return True
        else:
            return False

# uid
# activity + pkg + class + resourceId + text
# get uid from element(object)
# def get_unique_id(d, ele, activity_name):
#     class_name = ele.get("class")
#     res_id = ele.get("resource-id")
#     pkg_name = ele.get("package")
#     text = ""
#     temp_text = ele.get("text")
#     if temp_text:
#         text = temp_text
#     else:
#         text = traverse_tree(ele)
#
#     loc_x, loc_y = get_location(ele)
#     uid = activity_name + "-" +pkg_name + "-" + class_name + "-" +res_id + "-" + "(" + str(loc_x) + "," + str(loc_y) + ")" + "-" + text
#     return uid

# get uid from element(dict)
def get_unique_id(d, ele_dict, activity_name):
    class_name = ele_dict.get("class")
    res_id = ele_dict.get("resource-id")
    pkg_name = ele_dict.get("package")
    text = ele_dict.get("text")
    loc_x, loc_y = get_location(ele_dict)
    uid = activity_name + "-" +pkg_name + "-" + class_name + "-" +res_id + "-" + "(" + str(loc_x) + "," + str(loc_y) + ")" + "-" + text
    return uid

def get_dict_clickable_ele(d, clickable_ele, activity_name):
    clickable_ele_dict = {}
    clickable_ele_dict["class"] = clickable_ele.get("class")
    clickable_ele_dict["resource-id"] = clickable_ele.get("resource-id")
    clickable_ele_dict["package"] = clickable_ele.get("package")

    temp_text = clickable_ele.get("text")
    if temp_text:
        clickable_ele_dict["text"] = temp_text
    else:
        temp_text = traverse_tree(clickable_ele)
        clickable_ele_dict["text"] = temp_text
    clickable_ele_dict["bounds"] = clickable_ele.get('bounds')
    return clickable_ele_dict

# def get_uid(ele, d, umap, cur_activity):
#     uid = get_unique_id(ele, d, cur_activity)
#     cnt = umap.get(uid)
#     uid = uid + "&&&" + str(cnt)
#     return uid

# def get_uid_cnt(uid):
#     # print(uid)
#     start = uid.find("&&&")
#     res = ""
#     if start != -1:
#         res = uid[start+3 : ]
#     return int(res)

#获取页面的坐标
def get_location(ele_dict):
    bounds = ele_dict.get('bounds')
    left, top, right, bottom = map(int, bounds[1:-1].split('][')[0].split(',') + bounds[1:-1].split('][')[1].split(','))
    x = (left + right) // 2
    y = (top + bottom) // 2
    return x, y


#不全，没有resoure-id
def print_current_window_all_clickable_elements(d):
    clickable_elements = d(clickable=True)
    for ele in clickable_elements:
        print(ele.info.get('text'))

#com.alibaba.android.rimet
def get_current_window_package(d):
    current_app = d.current_app()
    return current_app['package']

def get_current_activity(d):
    current_app = d.current_app()
    return current_app["activity"]



def get_top_activity(d):
    output = d.shell("dumpsys window | grep mCurrentFocus").output
    pattern = r"{(.*)}"
    # Using re.search() to find the first occurrence of the pattern in the string
    match = re.search(pattern, output)

    # If a match is found, print the matched substring
    if match:
        return match.group(1)
    else:
        return None


def print_current_window_detailed_elements(d):
    xml = d.dump_hierarchy()
    root = ET.fromstring(xml)
    clickable_elements = []
    for element in root.findall('.//node'):
        if element.get('clickable') == 'true':
            if element.get("package") not in system_view:
                clickable_elements.append(element)
    for element in clickable_elements:
        print(ET.tostring(element))
        print("*"*100)
    print("*"*100)
    print(len(clickable_elements))
    bounds = element.get('bounds')
    left, top, right, bottom = map(int, bounds[1:-1].split('][')[0].split(',') + bounds[1:-1].split('][')[1].split(','))
    x = (left + right) // 2
    y = (top + bottom) // 2