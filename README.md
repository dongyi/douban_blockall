# douban_blockall


---------------------------------

- 一个爬虫，自动拉黑某个小组的全体用户
- spider to block all members in a specific group


### 使用说明：

- chrome打开豆瓣随便找个请求复制一下request header，贴到user_header.py里 例如：

  ```python
  header_txt_from_clipboard ="""
  Host: www.douban.com
  Connection: keep-alive
  Content-Length: 325
  Accept: application/json, text/javascript, */*; q=0.01
  Sec-Fetch-Dest: empty
  X-Requested-With: XMLHttpRequest
  User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36
  Content-Type: application/x-www-form-urlencoded
  Origin: https://www.douban.com
  Sec-Fetch-Site: same-origin
  Sec-Fetch-Mode: cors
  Referer: https://www.douban.com/people/[username]/
  Accept-Encoding: gzip, deflate, br
  Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6
  Cookie: 
  """
  ```
  
- 运行 `pyspider`
