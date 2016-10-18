#coding:utf-8
import urllib2

def url_user_agent(url):
    #设置使用代理
    proxy = {'http':'27.24.158.155:84'}
    proxy_support = urllib2.ProxyHandler(proxy)
    # opener = urllib2.build_opener(proxy_support,urllib2.HTTPHandler(debuglevel=1))
    opener = urllib2.build_opener(proxy_support)
    urllib2.install_opener(opener)

    #添加头信息，模仿浏览器抓取网页，对付返回403禁止访问的问题
    # i_headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    i_headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48'}
    req = urllib2.Request(url,headers=i_headers)
    html = urllib2.urlopen(req)
    print html.text
    if url == html.geturl():
        doc = html.read()
        return doc
    return

url = 'http://baike.baidu.com/view/21087.htm'
doc = url_user_agent(url)
print doc