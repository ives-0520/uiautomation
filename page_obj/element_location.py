from config.read_config import readConf

r = readConf()
packagename = r.get_device_info()['appPackage']



class Element_Location:
    # v-demo文本元素（“v-demo”APP入口）
    v_demo = {"text": "v-demo"}
    # 权限允许按钮（系统弹窗“允许”按钮）
    permission_allow_button = {"resourceId": "com.android.permissioncontroller:id/permission_allow_button"}
    # 账号登录按钮（首页“账号登录”按钮）
    account_login_tv2 = {"resourceId": f"{packagename}:id/account_login_tv2"}
    # 用户名输入框（登录界面）
    loginf_et_username = {"resourceId": f"{packagename}:id/loginf_et_username"}
    # 密码输入框（登录界面）
    et_pwd = {"resourceId": f"{packagename}:id/et_pwd"}
    # 记住密码复选框（登录界面）
    remember_pwd_cb = {"resourceId": f"{packagename}:id/remember_pwd_cb"}
    # 登录按钮（登录界面）
    loginf_tv_login = {"resourceId": f"{packagename}:id/loginf_tv_login"}
    # 图片控件（头像图片）
    imageView = {"resourceId": f"{packagename}:id/imageView"}
    name_live = {"resourceId": f"{packagename}:id/name", "text": "LIVE"}
    btn_profile = {"xpath": f'//*[@resource-id="{packagename}:id/btn_profile"]/android.widget.LinearLayout[1]'}
    recycler_view_item = {"xpath": f'//*[@resource-id="{packagename}:id/recycler_view"]/android.widget.LinearLayout[1]'}
    et_recharge_code = {"resourceId": f"{packagename}:id/et_recharge_code"}
    recharge_code_confirm = {"resourceId": f"{packagename}:id/recharge_code_confirm"}
    btn_account_logout = {"resourceId": f"{packagename}:id/btn_account_logout"}
    btn_up = {"resourceId": f"{packagename}:id/btn_up"}
    tv_content={"resourceId": f"{packagename}:id/tv_content"}













