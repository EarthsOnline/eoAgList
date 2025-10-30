# eoAgList
这些规则目前可能正在被维护。

### eoAgList
eoAgList 旨在过滤掉一些令人不适的内容。  
欢迎您根据自己的需要进行选择或提交 Issue。  

### 现有的过滤规则
* eoAgList_strict
  * illegal_filters
  * strict
    * Baidu_filters
    * Bilibili_filters
    * doc88_filters
    * Souhu_filters

  
|List|Raw|
|:-|:-|
|eoAgList_strict|https://raw.githubusercontent.com/EarthsOnline/eoAgList/refs/heads/main/eoAgList/eoAgList_strict.txt|

#### 过滤列表的使用方法
在 “添加自定义过滤器” 页面输入以 **raw** 开头的纯文本格式的规则列表。  
需要更新过滤器时，请删除对应的过滤器并重新添加。

#### 哪些内容可能会被过滤
* 悬浮式的界面

  * 比如 Bilibili 显示在右下角的登录提示

* 一些通常使用不到的选项卡
* 毫无价值的推送

#### 哪些内容一定会被过滤
此类内容 **不支持** 通过提交 Issue 来取消过滤。

* 完全不符合 **正常人** 价值观的网站
* DNS 劫持
* 经常被用于进行 DNS 劫持的域名停靠网站

  * 比如 Dragon Parking

* 已被证实有欺诈/捆绑行为的网站

  * 比如 Steam Big 和 Reasons Lab

#### 投诉
如果您的网站不知道为什么出现在了这里，并且您确定您的网站不符合 “哪些内容一定会被封锁” 的标准：  
* 欢迎您提交 Issuse，也许有人会去检查一下。  
* eoAgList 欢迎进行友好的讨论。

#### 提交策略
eoAgList 会尽量仿照 [EasyList](https://github.com/easylist/easylist/?tab=readme-ov-file#commit-policy) 的方式标记提交的修改：  
* A：增加了一个新的选择器
* M：去除过时/失效的选择器
* P：修改/删除了一个选择器来解决一个 Issue
