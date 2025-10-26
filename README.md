# eoAgList
这些规则目前可能正在被维护。

### eoAgList
eoAgList (EarthsOnline's Adguard List) 旨在过滤掉一些常见的中文网站上令人恼火的元素。  
值得注意的是 eoAgList 具有很强的主观性， 且会对部分网站造成严重的破坏。  
因此，未来可能会创建更温和的过滤规则。  
欢迎您根据自己的需要进行选择或提交 Issue！  

#### 现有的过滤规则
* Combine List
  * Bilibili_filters
  * Baidu_filters

#### 过滤列表的使用方法
请您阅读这些 [图片](Guides/step_1.png) 获取更多的信息。  
其中，请在 URL 里填写纯文本格式 —— 以 raw 开头的地址。

### 哪些内容可能会被过滤
* 悬浮式的界面
  * 比如 Bilibili 显示在右下角的登录提示
* 一些通常使用不到的选项卡
* 毫无价值的推送

### 哪些内容一定会被过滤
这一部分内容不支持通过提交 Issue 来取消过滤。

* 完全不符合正常人价值观的网站
* DNS 劫持
* DNS 劫持的载体
  * 比如 DragonParking

### 投诉
如果您的网站不知道为什么出现在了这里，并且您确定您的网站不符合 “哪些内容一定会被封锁” 的标准：  
* 欢迎您提交 Issuse，也许有人会去检查一下。  
* eoAgList 欢迎进行友好的讨论。

### 提交策略
eoAgList 会尽量仿照 [EasyList](https://github.com/easylist/easylist/?tab=readme-ov-file#commit-policy) 的方式标记提交的修改：  
* A：增加了一个新的选择器
* M：去除过时/失效的选择器
* P：修改/删除了一个选择器来解决一个 Issue
