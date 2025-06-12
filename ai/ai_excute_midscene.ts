import 'dotenv/config';
import { AndroidAgent, AndroidDevice, getConnectedDevices } from '@midscene/android';


process.env.OPENAI_API_KEY = '0decd078-73bf-4043-a1e7-0108c3c34785';


const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
Promise.resolve(
  (async () => {
    const devices = await getConnectedDevices();
    const page = new AndroidDevice(devices[0].udid);

    // 👀 初始化 Midscene agent
    const agent = new AndroidAgent(page,{
      
        
   
    });
    await page.connect();

    // 👀 打开浏览器并导航到 ebay.com（请确保当前页面有浏览器 App 喔）
    await agent.aiAction(
   `1. 点击首页的“v-demo”入口。
    2. 在弹出的权限请求窗口，点击“允许”按钮。
    3. 点击“账号登录”按钮，进入登录界面。
    4. 点击用户名输入框，输入账号“0609@ipwangxin.cn”。
    5. 点击密码输入框，输入密码“123456”。
    6. 点击“记住密码”复选框。
    7. 点击“登录”按钮，提交账号密码。
    8. 登录成功后，点击头像图片进入个人中心。`);

    // await sleep(5000);

    // // 👀 输入关键词，执行搜索
    // await agent.aiAction('在搜索框输入 "Headphones" ，敲回车');

    // // 👀 等待加载完成
    // await agent.aiWaitFor("页面中至少有一个耳机商品");
    // // 或者你也可以使用一个普通的 sleep:
    // // await sleep(5000);

    // // 👀 理解页面内容，提取数据
    // const items = await agent.aiQuery(
    //   "{itemTitle: string, price: Number}[], 找到列表里的商品标题和价格"
    // );
    // console.log("耳机商品信息", items);

    // 👀 用 AI 断言
    await agent.aiAssert("登录成功");
    // 或者你也可以使用一个普通的 sleep:
  })()
);