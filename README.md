### 项目结构图

```plaintext
Zap-with-AppUIAutomator2Navigation/
 ...
├── zap/ # zap_api调用
├── zap_results/ # zap结果导出
 ...
├── all_pkg_testfile.txt # 测试包名参考
├── apk_pkgName.txt # 要测试的包名
├── config.ini # 自动点击配置
 ...
├── run_config.py # 原项目运行入口，无ZAP
├── run_config_with_zap.py # 加了ZAP后的项目运行入口
└── ...
```

### Zap API参考

[Zap API Documentation](https://www.zaproxy.org/docs/api/#introduction)

[Zap API Py Github](https://github.com/zaproxy/zap-api-python?tab=readme-ov-file)

目前只做到了自动抓包，未实现截获重放的api调用

### 后续思路：

1. create_flitter.py: 对抓包结果进行跨域/跨境流量分析，返回有问题的新json，先基于IP过滤，人工观察一些跨境流量是否有IP以外的特征适合检测（比如一些参数、域名特征等）。
   - 人工理解了所需特征后再设计引入大模型（能否通过手动识别几个跨域例子来作为LLM的prompt，在这里接上LLM让其帮助实现跨域问题的识别，或者说能否我们规定一个我们想检测的有问题的请求响应的模版，用户可以填这个模版作为给LLM的prompt，从而实现自定义的问题流量识别）。
2. flitter.py: 能读取1. 中的有问题的Json作为场景重现重放识别的过滤器，实现有问题场景的截获重放（ZAP API有截获重放等接口）
