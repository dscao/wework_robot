# Wework_Robot
HomeAssistant 企业微信群机器人消息推送

如何设置群机器人 \
https://open.work.weixin.qq.com/help2/pc/14931?person_id=1 \
企业微信群机器人配置说明： \
https://developer.work.weixin.qq.com/document/path/91770




## 安装

* 将 custom_component 文件夹中的内容拷贝至自己的相应目录

或者
* 将此 repo ([https://github.com/dscao/wework_robot](https://github.com/dscao/wework_robot)) 添加到 [HACS](https://hacs.xyz/)，然后添加“Wework Robot”

## 配置
```yaml
notify:
  - platform: wework_robot
    name: wework_robot
    resource: https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx #自己的机器人地址
```

## 使用
```yaml
service: notify.wework_robot  #调用服务
data:
  message: 消息内容（仅发送文本消息时at手机号才有效）
  target:
    - at的手机号1
    - at的手机号2
    - at的手机号3


service: notify.wework_robot
data:
  message: 发送纯文本消息，当前时间：{{now().strftime('%Y-%m-%d %H:%M:%S')}}


service: notify.wework_robot
data:
  message: 发送带标题和分隔线的纯文本消息
  title: 这是标题
  

service: notify.wework_robot
data:
  message: "实时新增用户反馈<font color=\"warning\">132例</font>，请相关同事注意。\n >类型:<font color=\"comment\">用户反馈</font>\n >普通用户反馈:<font color=\"comment\">117例</font>\n >VIP用户反馈:<font color=\"comment\">15例</font>"
  title: 这是标题
  data:
    type: markdown


service: notify.wework_robot
data:
  message: 发送图片，标题和消息都不显示
  data:
    type: image
    imagepath: /config/www/1.jpg

service: notify.wework_robot
data:
  message: 发送带标题、内容和头图的链接卡片
  title: 这是标题
  data:
    type: news
    url: 'http://www.sogou.com'
    picurl: 'https://bbs.hassbian.com/static/image/common/logo.png'


service: notify.wework_robot
data:
  message: 发送图片文件，标题和消息都不显示
  data:
    type: file
    filepath: /config/www/1.jpg


service: notify.wework_robot
data:
  message: 发送mp3文件，标题和消息都不显示
  data:
    type: file
    filepath: /config/www/1.mp3


service: notify.wework_robot
data:
  message: 发送mp4文件，标题和消息都不显示
  data:
    type: file
    filepath: /config/www/1.mp4


```

## 示例
```yaml   
service: notify.wework_robot
data:
  title: 小汽车当前位置：{{states('sensor.mycar_loc')}}[dshass]
  message: >-
    小汽车当前位置：{{states('sensor.mycar_loc')}} {{"\n\n"}}
    状态刷新时间：{{"\n\n"}}{{state_attr('device_tracker.gddr_gooddriver',
    'querytime')}} {{"\n\n"}}
    车辆状态：{{state_attr('device_tracker.gddr_gooddriver', 'status')}} {{"\n\n"}}
    到达位置时间：{{"\n\n"}}{{state_attr('device_tracker.gddr_gooddriver',
    'updatetime')}}
    {{"\n\n"}}停车时长：{{state_attr('device_tracker.gddr_gooddriver',
    'parking_time')}}{{"\n\n"}}当前速度：{{state_attr('device_tracker.gddr_gooddriver',
    'speed') |round(1)
    }}km/h{{"\n\n"}}[查看地图](https://uri.amap.com/marker?position={{state_attr('device_tracker.gddr_gooddriver',
    'longitude')+0.00555}},{{state_attr('device_tracker.gddr_gooddriver',
    'latitude')-0.00240}})![https://restapi.amap.com/v3/staticmap?zoom=14&size=1024*512&markers=large,,A:{{state_attr('device_tracker.gddr_gooddriver',
    'longitude')+0.00555}},{{state_attr('device_tracker.gddr_gooddriver',
    'latitude')-0.00240}}&key=819c47ccf5602b3a5e97161836e1176f](https://restapi.amap.com/v3/staticmap?zoom=14&size=1024*512&markers=large,,A:{{state_attr('device_tracker.gddr_gooddriver',
    'longitude')+0.00555}},{{state_attr('device_tracker.gddr_gooddriver',
    'latitude')-0.00240}}&key=81xxxxxxxxxxxxxxxxxxx)
  date: 
    type: markdown


```



