#coding:utf8
import cPickle as pickle
import wechat
import pr
import time
gt=pr.Get_ips(10)
ips=gt.validip()
lq=gt.lq
l=[]
l.append(lq)
l.append(ips)
print len(ips),time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
if gt.check:
  wechat.w_get("http://sc.ftqq.com/SCU6677T8dbadb7d61c94c3acaf6df175948d2b858c8e9d9be2fb.send?text=刷新代理池&desp=代理池可用IP"+str(len(ips))+"个") 
if len(ips)>0:
  with open("/root/ips.pickle","wb") as f:
    pickle.dump(l,f,True)
else:
  wechat.w_get("http://sc.ftqq.com/SCU6677T8dbadb7d61c94c3acaf6df175948d2b858c8e9d9be2fb.send?text=可用IP无&desp=代理池可用IP0个")
