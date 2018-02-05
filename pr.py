#coding:utf-8
import re
import wechat
import requests
import cPickle as pickle
from bs4 import BeautifulSoup
import threading
import time
import Queue
class Get_ips():
    def __init__(self,page):
        with open("/root/ips.pickle","rb") as f:
            pk=pickle.load(f)
        self.ips=pk[1]
        self.urls=[]
        self.check=False
        for i in range(page):
            self.urls.append("http://www.xicidaili.com/nn/" + str(i))
            self.urls.append("http://www.xicidaili.com/nt/" + str(i))
        self.header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,zh-CN;q=0.8,zh;q=0.6,en;q=0.4",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    }
        #self.file=open("ips",'w')
        self.q=Queue.Queue()
        self.lq=pk[0]
        self.Lock=threading.Lock()
    def get_ips(self):
        if len(self.ips)>5:
            for l in self.lq:
                self.q.put(l)
        else:
            print "--------------------Refreshing the IP pound -----------------------"
            for url in self.urls:
                time.sleep(2)
                try:
                  res = requests.get(url, headers=self.header,timeout=4)
                except:
                  continue
                soup = BeautifulSoup(res.text, 'lxml')
                ips = soup.find_all('tr')
                lq=[]
                for i in range(1, len(ips)):
                    ip = ips[i]
                    tds = ip.find_all("td")
                    ip_temp = "http://" + tds[1].contents[0] + ":" + tds[2].contents[0]
                    # print str(ip_temp)
                    self.q.put(str(ip_temp))
                    self.lq.append(str(ip_temp))
            self.lq=list(set(self.lq))
            self.check=True
    def review_ips(self):
        self.ips=[]
        while not self.q.empty():
            try:
                ip=self.q.get(False)
                proxy={"http": ip}
                res = requests.get("http://www.haitaobei.com", headers=self.header,proxies=proxy,timeout=2,allow_redirects=False)
                time.sleep(1)
                res1= requests.get("http://www.haitaobei.com", headers=self.header,proxies=proxy,timeout=2,allow_redirects=False)
                #time.sleep(2)
                #res2=requests.get("http://www.baidu.com", proxies=proxy,timeout=5,allow_redirects=False)
                bs=BeautifulSoup(res.content,"lxml")
                test=re.search(u"海淘贝",bs.title.string)
                if res.status_code == 200  and res1.status_code==200 and test<>None:
                    self.Lock.acquire()
                    self.ips.append(ip)
#                    print ip
                    self.Lock.release()
            except Exception:
                pass
                #print 'error'
    def validip(self):
        self.get_ips()
        threads=[]
        for i in range(60):
            threads.append(threading.Thread(target=self.review_ips,args=[]))
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        return self.ips
