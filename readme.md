# BF1 Server Data Collector

一个基于bf1客户端api的服务器数据收集工具。

```cmd
BF1 Server Data Collector/
├── src/
│   ├── api/                      # 客户端 API 工具
│   ├── modules/
│   │   ├── client_records.py     # 击杀记录类
│   │   ├── client_utils.py       # #客户端api组件类
│   │   └── ...
│   └── utils/
│       ├── weapon_dict.json      # 用于武器数据转换字典
│       ├── database/             # 数据库类待开发
│       └── ...
└── main.py                        # 入口
```

