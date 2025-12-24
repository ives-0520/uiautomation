import 'dotenv/config';
import { AndroidAgent, AndroidDevice, getConnectedDevices } from '@midscene/android';




const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));
Promise.resolve(
  (async () => {
    const devices = await getConnectedDevices();
    if (!devices || devices.length === 0) {
      console.error('未检测到连接的设备，请通过 adb 连接设备后重试。');
      process.exit(1);
    }
    const page = new AndroidDevice(devices[0].udid);

    // 👀 初始化 Midscene agent
    const agent = new AndroidAgent(page,{
      
        
   
    });
    await page.connect();

    // 👀 打开浏览器并导航到 ebay.com（请确保当前页面有浏览器 App 喔）
    await agent.aiAction(
   `1. 点击首页的“doozy tv”入口。
    2. 在弹出的权限请求窗口，点击“允许”按钮。
    3. 点击“账号登录”按钮，进入登录界面。
    4. 点击用户名输入框，输入账号“becky.lin@bitkernel.tech”。
    5. 点击密码输入框，输入密码“Aa123456”。
    6. 点击“记住密码”复选框。
    7. 点击“登录”按钮，提交账号密码。
    8. 登录成功后，点击头像图片进入个人中心。`);

    // 👀 用 AI 断言
    await agent.aiAssert("判断是否登录成功");
    
  })()
);