# coding=utf-8

import requests
import time
import logging
import config
import sys


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
    r = requests.post('https://maker.ifttt.com/trigger/%s/with/key/%s' % (config.ifttt_event, config.ifttt_key), json=data,
                      headers={'Connection': 'close'}, timeout=180)
    logger.info(r.headers)
    logger.info(r.content)