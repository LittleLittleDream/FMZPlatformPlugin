import sublime
import sublime_plugin
import re
import os

funcDict = {}

def plugin_loaded():
    global funcDict
    funcDict = {
        "Chart(...)": "\n```Chart(...)```，自定义图表，画图函数。\n\n",
        "CommandRobot(...)": "\n```CommandRobot(RobotId, Cmd)```函数向指定ID的机器人发送命令（由策略中调用的```GetCommand()``` API捕获）。\n",
        "DeleteNode(Nid)": "\n```DeleteNode(Nid)```删除托管者节点。\n",
        "DeleteRobot(...)": "\n```DeleteRobot(RobotId, DeleteLogs)```删除机器人。\n",
        "Dial(...)": "\n```Dial(Address, Timeout)```，原始的Socket访问,支持**tcp**,**udp**,**tls**,**unix**协议。参数值：```Address```为string类型，填入地址，```TimeOut```为超时时间，超时，```Dial(...)```函数返回空值，单位：秒。\n",
        "EnableLog()": "\n```EnableLog(IsEnable)```，打开或者关闭订单信息的日志记录。参数值：**isEnable**为**bool**类型。**IsEnable**设置为**false**则不打印订单日志，不写入机器人数据库。\n",
        "GetAccount()": "\n```GetAccount()```返回发明者量化交易平台账户信息。\n",
        "GetCommand()": "\n```GetCommand()```，获取交互命令(utf-8)。获取策略交互界面发来的命令并清空,没有命令则返回null,返回的命令格式为“按钮名称:参数”,如果没有参数,则命令就是按钮名称。\n",
        "GetExchangeList()": "\n```GetExchangeList()```返回支持的交易所列表以及需要的配置信息。\n",
        "GetLastError()": "\n```GetLastError()```，获取最近一次出错信息,一般无需使用,因为程序会把出错信息自动上传到日志系统。返回值：string类型。调用```GetLastError()```函数后，会清除这个错误缓存，再次调用时，不会再返回上次记录的错误信息。\n",
        "GetNodeList()": "```GetNodeList()```返回托管者列表。\n\n",
        "GetOS()": "\n```GetOS()```，返回托管者所在系统的信息。\n",
        "GetPid()": "\n```GetPid()```，返回机器人进程ID。返回值：string类型。\n",
        "GetPlatformList()": "```GetPlatformList()```返回已添加的交易所列表。\n\n",
        "GetRobotDetail(RobotId)": "\n```GetRobotDetail(RobotId)```获取指定ID的机器人详细信息。\n",
        "GetRobotList(...)": "\n```GetRobotList(offset, length, robotStatus, label)```返回机器人列表。\n",
        "GetRobotLogs(...)": "\n```GetRobotLogs(robotId, logMinId, logMaxId, logOffset, logLimit, profitMinId, profitMaxId, profitOffset, profitLimit, chartMinId, chartMaxId, chartOffset, chartLimit, chartUpdateBaseId, chartUpdateDate, summaryLimit)```获取指定ID机器人的日志信息。\n",
        "GetStrategyList()": "\n```GetStrategyList()```获取策略列表。\n",
        "HMAC(...)": "\n```HMAC(Algo, OutputAlgo, Data, Key)```，支持**md5**/**sha256**/**sha512**/**sha1**的HMAC加密计算,只支持实盘。参数值：都为string类型。\n",
        "Hash(...)": "\n```Hash(Algo, OutputAlgo, Data)```，支持**md5**/**sha256**/**sha512**/**sha1**的哈希计算,只支持实盘。参数值：都为string类型。\n",
        "HttpQuery(...)": "\n```HttpQuery(Url, PostData, Cookies, Headers, IsReturnHeader)```，网络URL访问。参数值：都为string类型。\n",
        "IsVirtual()": "  \n```IsVirtual()```，判断是否是模拟回测。返回值：**bool**类型。\n",
        "Log(...)": "\n```Log(message)```，保存一条信息到日志列表。参数值：message可以是任意类型。\n",
        "LogProfit(Profit)": "\n```LogProfit(Profit)```，记录盈利值，这个为总盈利的值，打印收益数值，并根据收益数值绘制收益曲线，参数值：**Profit**为**number**类型。\n",
        "LogProfitReset()": "  \n```LogProfitReset()```，清空所有收益日志,可以带一个数字参数,指定保留的条数。\n",
        "LogReset()": "\n```LogReset()```，清除日志，可以传入一个参数，指定保留最近日志条数，清除其余日志。每次启动的启动日志算一条，所以如果不传入参数，并且策略起始时没有日志输出，就会完全不显示日志，等待托管者日志回传（并非异常情况）。无返回值。\n",
        "LogStatus(Msg)": "\n```LogStatus(Msg)```，此信息不保存到日志列表里,只更新当前机器人的状态信息,在日志上方显示,可多次调用,更新状态。参数值：Msg可以为任意类型。\n",
        "LogVacuum()": "\n```LogVacuum()```，回收**SQLite**删除数据时，占用的空间。\n",
        "MD5(String)": "\n```MD5(String)```，参数值：**string**类型。\n",
        "Mail(...)": "\n```Mail(smtpServer, smtpUsername, smtpPassword, mailTo, title, body)```，发送邮件函数。\n",
        "NewRobot(Settings)": "\n```NewRobot(Settings)```根据参数设置创建一个新的机器人。\n",
        "PluginRun(Settings)": "\n```PluginRun(Settings)```使用扩展API调用**调试工具**。\n",
        "RestartRobot(...)": "\n```RestartRobot(RobotId, Settings)```重启指定ID的机器人。\n",
        "SetErrorFilter(...)": "\n```SetErrorFilter(RegEx)```，错误信息过滤。参数值：string类型。\n",
        "Sleep(Millisecond)": "\n```Sleep(Millisecond)```，休眠函数，使程序暂停一段时间。参数值：**Millisecond**为**number**类型。\n",
        "StopRobot(RobotId)": "\n```StopRobot(RobotId)```停止指定ID的机器人。\n",
        "StrDecode()": "\n```StrDecode()```，商品期货CTP协议中的汉字是GBK编码可用此函数解码。\n",
        "Unix()": "\n```Unix()```，返回秒级别时间戳。\n",
        "UnixNano()": "\n```UnixNano()```，返回纳秒级时间戳，如果需要获取毫秒级时间戳，可以使用如下代码:\n",
        "Version()": "\n```Version()```，返回系统当前版本号，字符串值，如3.0。返回值：string类型。\n",
        "_C(...)": "\n```_C(function, args...)```，重试函数。\n",
        "_Cross(Arr1, Arr2)": "\n```_Cross(Arr1, Arr2)```，返回数组**arr1**与**arr2**的交叉周期数。正数为上穿周期，负数表示下穿的周期，0指当前价格一样。参数值：**number**数组。\n",
        "_D(Timestamp, Fmt)": "\n```_D(Timestamp, Fmt)```，返回指定时间戳。参数值：**Timestamp**为数值类型，毫秒数。**Fmt**为string类型，**Fmt**默认为：```yyyy-MM-dd hh:mm:ss```，返回值：**string**类型。\n",
        "_G(K, V)": "\n```_G(K, V)```，可保存的全局字典，回测和实盘均支持，回测结束后，保存的数据被清除。\n",
        "_N(Num, Precision)": "\n```_N(Num, Precision)```，格式化一个浮点数。参数值，**Num**为**number**类型，**Precision**为整型**number**。返回值：number类型。\n",
        "exchange.Buy(Price, Amount)": "\n```exchange.Buy(Price, Amount)```，下买单,返回一个订单ID。参数值：price为订单价格，number类型，Amount为订单数量，number类型。返回值：string类型或数值类型（具体类型根据各个交易所返回类型而定）。\n",
        "exchange.CancelOrder(Id)": "\n```exchange.CancelOrder(orderId)```，取消某个订单，参数值：**orderid**为订单编号，string类型或数值类型（具体类型根据各个交易所下单时返回类型而定），返回值：bool类型。\n",
        "exchange.GetAccount()": "\n```exchange.GetAccount()```，将返回交易所账户信息。返回值:```Account```结构结构体。\n",
        "exchange.GetContractType()": "\n```exchange.GetContractType()```，返回交易所对象（```exchange```）当前设置的合约ID，返回值：字符串。\n",
        "exchange.GetCurrency()": "\n```exchange.GetCurrency()```，返回交易所操作的货币对名称如LTC_BTC，传统期货CTP返回的固定为STOCK。返回值:string类型。\n",
        "exchange.GetData(Source)": "\n```exchange.GetData(Source)```函数用于获取```exchange.SetData(Key,Value)```函数加载的数据或外部链接提供的数据，支持回测系统中使用。回测时一次性获取数据，实盘时缓存一分钟的数据。\n",
        "exchange.GetDepth()": "\n```exchange.GetDepth()```，获取交易所订单薄。返回值:```Depth```结构体。\n",
        "exchange.GetLabel()": "\n```exchange.GetLabel()```，返回交易所自定义的标签。返回值:string类型。\n",
        "exchange.GetName()": "\n```exchange.GetName()```，返回交易所名称。返回值:string类型。\n",
        "exchange.GetOrder(Id)": "\n```exchange.GetOrder(orderId)```，根据订单号获取订单详情，参数值:**orderid**为要获取的订单号，string类型或数值类型。（具体类型根据各个交易所返回类型而定）返回值:```Order```结构体。\n",
        "exchange.GetOrders()": "\n```exchange.GetOrders()```，获取所有未完成的订单。返回值:```Order```结构体数组。\n",
        "exchange.GetPeriod()": "\n```exchange.GetPeriod()```函数返回在**回测**、**实盘**运行策略时在发明者量化交易平台网站页面上设置的K线周期。返回值为整数，单位为秒。返回值:number类型。\n",
        "exchange.GetPosition()": "\n```exchange.GetPosition()```，获取当前持仓信息，可以传入一个参数，指定要获取的合约类型。返回值：```position```结构体数组。\n",
        "exchange.GetRate()": "\n```exchange.GetRate()```，返回交易所使用的流通货币与当前显示的计价货币的汇率, 返回1表示禁用汇率转换。返回值:number类型。\n",
        "exchange.GetRawJSON()": "\n```exchange.GetRawJSON()```，返回最后一次**REST API**请求返回的原始内容(字符串),可以用来自己解析扩展信息。返回值:string类型，只在数字货币策略实盘环境下有效。\n",
        "exchange.GetRecords()": "\n```exchange.GetRecords(Period)```，返回一个K线历史,K线周期在创建机器人时指定，如果在调用```exchange.GetRecords()```函数时指定了参数，获取的就是按照该参数周期的K线数据，如果没有参数，按照机器人参数上设置的K线周期或者回测页面设置的K线周期返回K线数据。参数值:**PERIOD_M1**指1分钟,**PERIOD_M5**指5分钟,**PERIOD_M15**指15分钟,**PERIOD_M30**指30分钟,**PERIOD_H1**指1小时,**PERIOD_D1**指一天。返回值:Record结构体数组。K线数据，会随时间累积，最多累积到2000根，然后会更新加入一根，同时删除一根最早时间的K线柱（如队列进出）。部分交易所没有提供K线接口，托管者实时收集数据生成K线。\n",
        "exchange.GetTicker()": "\n```exchange.GetTicker()```，获取市场当前行情，返回值:```Ticker```结构体。\n",
        "exchange.GetTrades()": "\n```exchange.GetTrades()```，获取交易所交易历史（非自己）。返回值:```Trade```结构体数组。部分交易所不支持，具体返回的数据是多少范围内的成交记录，因交易所而定，需要根据具体情况处理。\n",
        "exchange.GetUSDCNY()": "\n```exchange.GetUSDCNY()```，返回美元最新汇率(yahoo提供的数据源)或OKEX期货合约使用的美元汇率，返回值:number类型。\n",
        "exchange.Go(...)": "\n```exchange.Go(Method, Args…)```，多线程异步支持函数,可以把所有支持的函数的操作变成异步并发的.(只支持数字货币交易平台)。参数值：Method为string类型，函数名。\n",
        "exchange.HMAC(...)": "\n```exchange.HMAC(Algo, OutputAlgo, Data, Key)```，支持**md5**/**sha256**/**sha512**/**sha1**的**HMAC**加密计算，只支持实盘。\n",
        "exchange.IO(...)": "\n```exchange.IO(\"api\", httpMethod, resource, params, raw)```，调用交易所其它功能接口。参数值：httpMehod为string类型，填入请求类型\"POST\"或者\"GET\",resource为string类型,填入路径,params为string类型，填入交互参数。raw为原始JSON字符串参数，可以不传。```exchange.IO(\"api\", httpMethod, resource, params, raw)```函数调用会访问交易所接口，发生错误，调用失败时，返回空值（发生网络请求的函数例如```GetTicker()```、```GetAccount()```等，调用失败时，返回空值）。\n",
        "exchange.Log(...)": "\n```exchange.Log(LogType, Price, Amount)```，不下单, 只记录交易信息。\n",
        "exchange.Sell(Price, Amount)": "\n```exchange.Sell(Price, Amount)```，下卖单，返回一个订单ID。参数值：price为订单价格，number类型，Amount为订单数量，number类型。返回值：string类型或数值类型（具体类型根据各个交易所返回类型而定）。\n",
        "exchange.SetBase(Base)": "```exchange.SetBase(Base)```函数用于切换交易所API基地址，例如切换为```OKEX```国内域名```https://www.okex.me```。兼容```exchange.IO(\"base\", \"https://xxx.xxx.xxx\")```切换方式。回测系统中不支持切换交易所API基地址。\n\n",
        "exchange.SetContractType(...)": "\n```exchange.SetContractType(ContractType)```，设置合约类型。参数值：string类型。\n",
        "exchange.SetCurrency(...)": "\n```exchange.SetCurrency(Symbol)```函数用于切换交易所对象当前的交易对。兼容```exchange.IO(\"currency\", \"BTC_USDT\")```切换方式，支持回测系统中切换交易对，回测系统中切换交易对时```计价币```名称不能改变（例如BTC_USDT可以切换为LTC_USDT，不能切换为LTC_BTC），切换为非回测页面初始设置的交易对后，```交易币```的数量为0（例如回测时，回测页面上初始设置的交易对为BTC_USDT，BTC数量为3个，USDT数量为10000，此时立即切换为LTC_USDT，切换后交易币数量为0，即账户中LTC数量为0，切换的交易对共享USDT数量，数量为10000）。\n",
        "exchange.SetData(Key,Value)": "\n```exchange.SetData(Key,Value)```函数用于设置策略运行时加载的数据，可以是任何经济指标、行业数据、相关指数等。用于交易策略量化考核所有可量化的信息，支持回测系统中使用。\n",
        "exchange.SetDirection(...)": "\n```exchange.SetDirection(Direction)```，设置Buy或者Sell下单类型。参数值：string类型。\n",
        "exchange.SetMarginLevel(...)": "\n```exchange.SetMarginLevel(MarginLevel)```，设置杆杠大小。参数值：number 类型。\n",
        "exchange.SetMaxBarLen(Len)": "\n```exchange.SetMaxBarLen(Len)```函数对于数字货币策略运行时影响两个方面：\n",
        "exchange.SetPrecision(...)": "\n```exchange.SetPrecision(PricePrecision, AmountPrecision)```，设置价格与品种下单量的小数位精度,设置后会自动截断，参数值：PricePrecision为number类型，用来控制价格后面的小数点位，AmountPrecision为number类型，用来控制数量后面的小数点位。PricePrecision和AmountPrecision都必须是整型number。\n",
        "exchange.SetProxy(...)": "\n```exchange.SetProxy(...)```，切换为代理服务器访问交易所。该函数无返回值（用变量获取，获取的是undefined），如果代理设置失败，在调用接口时，会返回空值。仅限**rest**协议。\n",
        "exchange.SetRate(Rate)": "\n```exchange.SetRate(Rate)```，设置交易所的流通货币的汇率，参数值：```Rate```为```number```类型。返回值：为```number```类型。\n",
        "exchange.SetTimeout(...)": "\n```exchange.SetTimeout(...)```，参数**Millisecond**为毫秒数值。\n",
        "init()": "\n```init()```，用户实现初始化函数```init()```，会在策略开始时自动执行```init()```函数，完成初始化任务。\n",
        "onerror()": "\n```onerror()```，发生异常时，会触发```onerror()```函数执行。\n",
        "onexit()": "\n```onexit()```，处理扫尾工作，最长执行5分钟，由用户实现。\n"
    }

def query(key):
    completion_data = []
    descLen = 50
    for funcName in funcDict:
        if re.match(key, funcName):
            desc = funcDict[funcName]
            if len(desc) > descLen:
                desc = desc[:descLen] + "..."
            completion_data.append(['{}/{}\tMethod'.format(key, desc), funcName])
        elif re.match(".*\." + key, funcName):
            arr = funcName.split(".", 1)
            desc = funcDict[funcName]
            if len(desc) > descLen:
                desc = desc[:descLen] + "..."
            completion_data.append(['{}/{}\tMethod'.format(key, desc), arr[1]])
    return completion_data

class FMZCodeEditTips(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        if not view.match_selector(locations[0], "source.python") and not view.match_selector(locations[0], "source.js") and not view.match_selector(locations[0], "source.c++"):
            return []

        point = locations[0] - len(prefix) - 1
        letter = view.substr(point)

        if letter == ':':
            pass 
        else :
            if re.match('^[0-9a-zA-Z_]+$', prefix) and len(prefix) > 1:
                return query(prefix)
        return ([], sublime.INHIBIT_EXPLICIT_COMPLETIONS)
