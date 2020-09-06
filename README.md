# Monitor 2.0.1
监控并记录玩家坐标，保存在records文件夹内

~~在玩家靠近伪和平时向全服通知~~

玩家可自主添加需要监控的坐标点

插件依赖[PlayerInfoAPI](https://github.com/TISUnion/PlayerInfoAPI)和[OnlinePlayerAPI](https://github.com/zhang-anzhi/MCDReforgedPlugins/tree/master/OnlinePlayerAPI)

使用前可先对插件进行设置：sleep = 10 ---- 每12秒记录一次玩家坐标

!!mr help  显示帮助消息

!!mr add [坐标名] [x] [y] [z] [次元]  次元：world nether end

!!mr list  显示所有已有监控

!!mr reload  重载监控坐标，联系管理员删除后操作该指令

为防止随意删除更改监控点，删除监控请在后台操作，玩家仅有添加权限

## New.

2.0.1 不再对Bot进行监控