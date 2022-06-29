''' 
https://open.work.weixin.qq.com/help2/pc/14931  
https://developer.work.weixin.qq.com/document/path/91770
'''

import logging
import time
import hmac
import hashlib
import base64
import urllib.parse
import requests
import json
import os
import voluptuous as vol
import base64
from requests_toolbelt.multipart.encoder import MultipartEncoder

from homeassistant.components.notify import (
    ATTR_MESSAGE,
    ATTR_TITLE,
    ATTR_DATA,
    ATTR_TARGET,
    PLATFORM_SCHEMA,
    BaseNotificationService,
)
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_RESOURCE

headers = {"Content-Type": "application/json"}

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_RESOURCE): cv.url,
})

_LOGGER = logging.getLogger(__name__)
DIVIDER = "———————————"

def get_service(hass, config, discovery_info=None):
 
    resource = config.get(CONF_RESOURCE)

    return WeworkNotificationService(resource)


class WeworkNotificationService(BaseNotificationService):
    

    def __init__(self, resource):
      
        self._resource = resource        

    def send_message(self, message="", **kwargs):
        send_url = self._resource
        timestamp = str(round(time.time() * 1000))
        
        title = kwargs.get(ATTR_TITLE)
        data = kwargs.get(ATTR_DATA) or {}
        msgtype = data.get("type", "text")
        url = data.get("url")
        picurl = data.get("picurl")
        imagepath = data.get("imagepath")
        filepath = data.get("filepath")
        atmoblies = kwargs.get(ATTR_TARGET)
       
        if msgtype == "text":
            content = ""
            if title is not None:
                content += f"{title}\n{DIVIDER}\n"
            content += message
            msg = {
                "content":content,
                "mentioned_list":[],
                "mentioned_mobile_list":atmoblies
                }
        elif msgtype == "markdown":
            content = ""
            if title is not None:
                content += f"{title}\n{DIVIDER}\n"
            content += message
            msg = {"content": content}
        elif msgtype == "image":
            
            if not imagepath:
                raise TypeError("图片地址未填写，消息类型为图片卡片时此项为必填！")
                return
            #files = {"image": open(imagepath, "rb")}
            with open(imagepath, 'rb') as f:
                image_data = f.read()
                base64_data = base64.b64encode(image_data).decode('utf8')  # base64编码
                fmd5 = hashlib.md5(image_data).hexdigest()

            msg = {
                "base64": base64_data,
                "md5": fmd5
                }
        elif msgtype == "news":            
            msg = {
                "articles": [
                    {
                        "title": title,
                        "description": message,
                        "url": url,
                        "picurl": picurl,
                    }
                ]
            }
        elif msgtype == "file":
            curl = (
                "https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key="
                + self._resource.split("key=")[1]
                + "&type=file"
            )
            if filepath and os.path.isfile(filepath):
                files = {"media": open(filepath, "rb")}                
                try:
                    r = requests.post(curl, files=files, timeout=(20,180))
                    _LOGGER.debug("Uploading media " + filepath + " to WeChat servicers" + r.text)
                except requests.Timeout: 
                    _LOGGER.error("File upload timeout, please try again later.")
                    return                
                media_id = json.loads(r.text)["media_id"]
            else:
                raise TypeError("filepath未填写或文件路径不正确。消息类型为file时，filepath为必填项")
                return

            msg = {"media_id": media_id}
            
        else:
            raise TypeError("消息类型输入错误，请输入：text/markdown/image/news/file")
            return
  
        send_values = {
            "msgtype": msgtype,
			msgtype: msg,
        }        
        
        _LOGGER.debug(send_values)
        send_msges = bytes(json.dumps(send_values), "utf-8")
        response = requests.post(send_url, data=send_msges, headers = headers).json()
        if response["errcode"] != 0:
            _LOGGER.error(response)
        else:
            _LOGGER.debug(response)