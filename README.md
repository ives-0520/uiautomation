# APP UI自动化框架

本框架基于weditor录制，生成uiautomator2格式的python自动化脚本，并通过AI分析和提示词工程（Prompt Engineering）驱动AI自动生成可维护的自动化代码。框架集成了AI能力，支持AI视觉元素定位、AI断言、自然语言用例生成等功能，适用于Android APP的UI自动化测试。

# 特色功能

- **AI视觉元素定位**：集成大模型（如“doubao-1-5-thinking-vision-pro”），支持通过APP截图+自然语言描述，自动识别并定位UI元素。AI返回元素文本、类型、相对坐标、置信度、与其他组件关系等丰富信息，极大提升自动化脚本的健壮性和适应性。
- **AI断言与结果判断**：通过AI模型对页面截图进行语义理解，自动判断操作结果（如充值是否成功），支持自然语言断言和失败原因分析，提升自动化验证的智能化水平。
- **传统与AI混合定位**：支持传统元素定位与AI视觉定位的无缝切换，传统定位失败时自动调用AI兜底，显著提升自动化用例的鲁棒性和适配能力。
- **AI驱动的元素库自动维护**：AI识别的元素定位结果可自动合并到主元素库，实现元素库的动态扩展和自我进化，减少人工维护成本。
- **AI辅助用例生成与自然语言脚本**：支持基于AI的自然语言用例描述、自动生成异常场景测试用例，推动自动化测试向“零代码”与“智能化”演进。
- **AI执行自然语言脚本**：支持AI直接运行自然语言脚本，并输出测试报告
- **AI分析日志**：支持AI分析pytest测试用例执行的日志，溯源报错原因并给出解决方案

## 查看测试报告
allure open report\allure-report

## 自然语言测试用例的执行方法
command prompt
1. 进入AI目录：
   ```bash
   cd ai
   ```
2. 执行自然语言测试用例：
   ```bash
   npx tsx ai_excute_midscene.ts
   ```

# 大模型管理平台
https://console.volcengine.com/ark/region:ark+cn-beijing/usageTracking

## 项目结构

```
APP_UI_AUTO\
│
├── ai\                        # AI相关工具
│   ├── .env                   # 环境变量配置
│   ├── ai_locator.py          # AI元素定位实现
│   ├── ai_excute_midscene.ts  # AI执行中间场景脚本
│   ├── midscene_run\          # AI中间场景运行目录
│   │   └── output\            # 输出结果目录
│   └── nature_lan_scripts\    # 自然语言脚本
│       ├── nature_login.py    # 登录自然语言脚本
│       └── nature_recharge.py # 充值自然语言脚本
├── config\                    # 配置文件目录
│   ├── config.ini            # 配置文件
│   └── read_config.py        # 配置读取工具
├── device\                    # 设备管理
│   ├── adbOperation.py       # ADB操作封装
│   └── device_init.py        # 设备初始化
├── element_manage\            # 元素管理模块，含元素定位、操作、管理等核心代码
│   ├── ElementLocatorSchema.py # 元素定位数据结构
│   ├── element_locator_manager.py # 元素定位器管理类
│   ├── elementOption.py      # 元素操作方法封装
│   └── element_locators.json # 元素库
├── page_obj\                  # 页面对象类
│   ├── obj_login.py          # 登录页面对象
│   └── obj_recharge.py       # 充值页面对象
├── record\                    # 录制脚本目录
│   ├── record.py             # 录制工具
│   └── record_scripts\       # 录制脚本存放目录
│       ├── record_login.py   # 登录录制脚本
│       └── record_recharge.py # 充值录制脚本
├── report\                    # 测试报告
│   ├── allure-report\        # allure测试报告
│   └── allure-results\       # allure原始测试结果
├── testCase\                  # 测试用例目录
│   └── testApp\              # APP测试用例
│       ├── conftest.py       # pytest配置和钩子
│       ├── login\            # 登录测试用例
│       │   └── test_obj_login.py # 登录测试用例
│       └── recharge\         # 充值测试用例
│           └── test_obj_recharge.py # 充值测试用例
├── utils\                     # 工具类
│   └── account_generate.py   # 账号生成工具
├── .gitignore                # Git忽略文件
├── pytest.ini               # pytest配置文件
└── README.md                # 项目说明文档
```
## 分层设计架构与POM模式

本框架采用分层设计架构，结合POM（Page Object Model，页面对象模型）模式，提升自动化测试的可维护性和可扩展性。

- **分层设计**：
  - 元素定位层（element_locators.json）：统一管理所有页面元素的定位信息。
  - 元素操作层（elementOption.py）：封装通用的元素操作方法。
  - 页面对象层（page_obj/obj_xxx.py）：每个页面或功能对应一个对象类，继承元素定位和操作层，将业务操作步骤方法化。
  - 测试用例层（testCase/testApp/）：组织具体的pytest测试用例，调用页面对象类实现业务流程测试。


- **POM模式**：
  - 每个页面或功能模块对应一个页面对象类，页面元素和操作分离，测试用例只关注业务流程调用，降低维护成本。

## 使用说明

1. 使用weditor录制操作，生成uiautomator2脚本至`record/`目录。
2. 运行AI分析工具，自动提取元素定位、生成页面对象类和测试用例。
3. 在pytest环境下运行`testCase/testApp/`下的测试用例文件。

## 自动化流程说明

1. **录制操作**：通过运行`record/start_record.py`开启录制，生成uiautomator2格式的自动化脚本。

**说明：** 以下所有流程均通过`提示词工程（Prompt Engineering）`驱动AI自动完成，无需手动编写脚本。**在使用提示词工程时，请将提示词中的文件名或方法名修改为你实际想要操作的名字，以确保生成的代码符合你的需求。**

2. **元素定位提取与管理**
   - 从`record/record_xxx.py`中提取所有元素定位信息。
   - 以`"account_login_tv2": {
        "v1": {
            "traditional": {
                "description": "账号登录按钮（首页‘账号登录’按钮）",
                "locator": {
                    "resourceId": "{packagename}:id/account_login_tv2"
                }
            }
        }
    }`的格式组织，版本默认为v1，类型默认为traditional。
   - 将这些元素定位信息增量地添加进`element_locators.json`中，添加后进行去重，确保所有元素定位唯一且无重复，便于统一管理和复用。

3. **元素操作方法映射与补全**：将录制脚本中的元素操作与ElementOption类中已定义的方法进行映射，自动检查ElementOption类是否包含所有所需的预定义方法，如有缺失则自动发现并补全缺失的方法，确保操作方法的完整性和一致性。

4. **步骤分析与自然语言描述**
   - 分析如`record_xxx.py`等脚本内容，自动生成自然语言描述的测试步骤`nature_xxx.py`，并将该文件放在`nature_lan_scripts`文件夹下，便于理解和维护。

5. **页面对象类自动生成**
   - **类的创建**：在`page_obj`目录下创建如`obj_xxx.py`的新文件，新建`obj_xxx`类，继承自`ElementOption`，使用ElementLocatorManager类的get_locator方法动态加载元素。
   - **方法的添加**：将`record/record_xxx.py`中的操作步骤封装为`obj_xxx`类中的方法，添加方法时，直接将record_xxx.py的步骤封装为类中的方法，元素定位从元素库动态加载和元素操作调用父类方法。

6. **pytest测试用例生成**
   - **新建测试用例文件**：在`testCase/testApp/`目录下创建如`test_obj_xxx.py`的新文件。
   - **添加测试用例**：将需要测试的流程或方法，逐步封装为`test_obj_xxx.py`中的pytest测试方法，实现对`obj_xxx`类xxx方法的基本流程测试。

7. **异常场景测试用例生成**
   - **自然语言用例生成**：根据`nature_xxx.py`中的自然语言描述，自动生成异常场景的自然语言测试用例，异常用例的步骤参照正向用例，补充在该文档中，并按照顺序组织起来，提升测试覆盖率和健壮性。
   
   - **pytest用例生成**：根据`nature_xxx.py`中的异常测试用例，自动生成对应的pytest方法，并添加到`testCase/testApp/test_obj_xxx.py`中。所有元素定位和操作方法均调用`page_obj/obj_xxx.py`中的内容，实现异常场景的自动化验证。


