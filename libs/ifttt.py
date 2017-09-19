# coding=utf-8

import time
import logging
import config
import sys
import json

from tornado import httpclient
from tornado.httpclient import AsyncHTTPClient, HTTPClient

reload(sys)
sys.setdefaultencoding('utf8')

logger = logging.getLogger('qiandao.worker')

def notify_web(task, tpl, err = None):
    if not config.ifttt_key:
        return
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    msg = "%s%s %s" % (tpl['sitename'], task['note'], "签到成功" if err is None else ("签到失败:%s" % unicode(err)) )
    data = {"value1": msg, "value2": localtime}
    logger.info("notify itfff msg %s " % msg)
    # r = requests.post('https://maker.ifttt.com/trigger/%s/with/key/%s' % (config.ifttt_event, config.ifttt_key), json=data,
    #                   headers={'Connection': 'close'}, timeout=180)
    # logger.info(r.headers)
    # logger.info(r.content)
    AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")
    http_client = AsyncHTTPClient()
    req = httpclient.HTTPRequest(
        method='POST',
        url='https://maker.ifttt.com/trigger/%s/with/key/%s' % (config.ifttt_event, config.ifttt_key),
        headers={'Content-Type': 'application/json','Connection': 'close'},
        body=json.dumps(data)
    )
    http_client.fetch(req)