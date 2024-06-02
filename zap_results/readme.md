导出的三个文件意义解释：

1. **`zap_https_{pkgName}_{timestamp}.har` 文件**：
   - **HAR 文件（HTTP Archive 格式）**：记录了测试期间所有 HTTP/HTTPS 请求和响应的详细信息。包括请求的 URL、HTTP 方法、请求头、响应头、响应体、状态码、加载时间等(最近似fiddler的har)。

2. **`zap_alerts__{pkgName}_{timestamp}.json` 文件**：
   - **警报 JSON 文件**：记录了 ZAP 在扫描过程中发现的所有安全警报的详细信息。这些警报包括发现的漏洞、风险等级、置信度、漏洞描述、解决方案建议、参考资料等。

3. **`zap_sitelog__{pkgName}_{timestamp}.json` 文件**：
   - **站点日志 JSON 文件**：记录了每个站点的详细扫描日志，包括每个站点的警报总结和实例，提供了每个站点的安全状态概述。