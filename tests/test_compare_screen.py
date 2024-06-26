import sys 
sys.path.append("..")
from utils.ScreenCompareUtils import *


str1 = "   旧设备扫码验证支付宝验证发送短信验证人工申诉 联系客服"
str2 = "   旧设备扫码验证支付宝验证发送短信验证人工申诉 联系客服"
ratio = get_text_similarity(str1, str2)
print(ratio*100, "%")


str1 = "   旧设备扫码验证发送短信验证人工申诉 联系客服 "
str2 = "   旧设备扫码验证发送短信验证人工申诉 联系客服 我知道了"
ratio = get_text_similarity(str2, str1)
print(ratio*100, "%")

str1 = "+8118033138368 请输入密码 登录忘记密码 我已阅读并同意服务协议, 隐私权政策 专属帐号 注册帐号 更多选项 加入会议"
str2 = "+8618033138368 请输入密码 登录忘记密码 我已阅读并同意服务协议, 隐私权政策 专属帐号 注册帐号 更多选项 加入会议"
ratio = get_text_similarity(str1, str2)
print(ratio*100, "%")

str1 = "-- 61 162--12306账号管理 540 162-- 88 322--12306账号 237 321-- 1011 321--常用购票人 240 481--出票更快 664 481-- 1011 481--12306会员 237 619--积分兑换车票 661 619-- 1011 619--个人资料 125 778-- 1011 778--修改绑定手机号 188 916-11 1053--修改密码 125 1191-- 1011 1191--注册账号 125 1328-- 1011 1328--身份核验须知 167 1487-- 1011 1487--铁路畅行会员 167 1625-- 1011 1625-- 66 162--注册12306账户 540 162--极速注册 270 291--推荐 403 267--普通注册 810 291--二代1--1 请输入港澳居民来往内地通行证号码 673 581--姓   名 98 722-- 182 724-- 182 724--2 请输入您的真实姓名 673 722--手机号码 125 863--(+86) 317 859--3 请填写您的手机号码 732 863--手机号码格式错误 391 924--下一步 540 1124-- 56 1276--号注册及进一步人证的便捷服务，更多请查看《账户授权协议》 570 1276"
str2 = "-- 61 162--12306账号管理 540 162-- 88 322--12306账号 237 321-- 1011 321--常用购票人 240 481--出票更快 664 481-- 1011 481--12306会员 237 619--积分兑换车票 661 619-- 1011 619--个人资料 125 778-- 1011 778--修改绑定手机号 188 916-11 1053--修改密码 125 1191-- 1011 1191--注册账号 125 1328-- 1011 1328--身份核验须知 167 1487-- 1011 1487--铁路畅行会员 167 1625-- 1011 1625-- 66 162--注册12306账户 540 162--极速注册 270 291--推荐 403 267--普通注册 810 291--港澳 581--1 请输入港澳台居民居住证号码 673 581--姓   名 98 722-- 182 724-- 182 724--2 请输入您的真实姓名 673 722--手机号码 125 863--(+86) 317 859--3 请填写您的手机号码 748 863--手机号码格式错误 391 924--下一步 540 1124-- 56 1276--您提号注册及进一步人证的便捷服务，更多请查看《账户授权协议》 570 1276"
ratio = get_text_similarity(str1, str2)
print(ratio*100, "%")

str3 = "-- 61 162--12306账号管理 540 162-- 88 322--12306账号 237 321-- 1011 321--常用购票人 240 481--出票更快 664 481-- 1011 481--12306会员 237 619--积分兑换车票 661 619-- 1011 619--个人资料 125 778-- 1011 778--修改绑定手机号 188 916-11 1053--修改密码 125 1191-- 1011 1191--注册账号 125 1328-- 1011 1328--身份核验须知 167 1487-- 1011 1487--铁路畅行会员 167 1625-- 1011 1625-- 66 162--注册12306账户 540 162--极速注册 270 291--推荐 403 267--普通注册 810 291--外国25 581--1 请输入外国人永久居留身份证号码 673 581--姓   名 98 722-- 182 724-- 182 724--2 请输入您的真实姓名 673 722-- 343 862--男 406 862-- 509 862--女 572 862-- 1019 999--手机号码 125 1138--(+86) 317 1134--3 请填写您的手机号码 27 1330-- 1019 1330--下一步 540 1537-- 56 1689--您提供的姓名、手机号、身份证号等信息将用于办理12306账号注册及进一步人证的便捷服务，更多请查看《账户授权协议》 570 1689"
ratio = get_text_similarity(str1, str3)
print(ratio*100, "%")

str4 = "-- 61 162--12306账号管理 540 162-- 88 322--12306账号 237 321-- 1011 321--常用购票人 240 481--出票更快 664 481-- 1011 481--12306会员 237 619--积分兑换车票 661 619-- 1011 619--个人资料 125 778-- 1011 778--修改绑定手机号 188 916-11 1053--修改密码 125 1191-- 1011 1191--注册账号 125 1328-- 1011 1328--身份核验须知 167 1487-- 1011 1487--铁路畅行会员 167 1625-- 1011 1625-- 66 162--注册12306账户 540 162--极速注册 270 291--推荐 403 267--普通注册 810 291--港澳125 581--1 请输入港澳居民来往内地通行证号码 673 581--姓   名 98 722-- 182 724-- 182 724--2 请输入您的真实姓名 673 722-- 343 862--男 406 862-- 509 862--女 572 862-- 1019 999--手机号码 125 1138--(+86) 317 1134--3 请填写您的手机号 627 1330-- 1019 1330--下一步 540 1537-- 56 1689--您提供的姓名、手机号、身份证号等信息将用于办理12306账号注册及进一步人证的便捷服务，更多请查看《账户授权协议》 570 1689"
ratio = get_text_similarity(str3, str4)
print(ratio*100, "%")

str5 = "--中国(+86) 540 1841--中国香港(+852) 540 1979--中国澳门(+853) 540 2116--中国台湾(+886) 540 2244"
ratio = get_text_similarity(str5, str1)
print(ratio*100, "%")