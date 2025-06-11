from config.read_config import readConf

r = readConf()
packagename = r.get_device_info()['appPackage']



class Element_Location:
    loginf_tv_login = {"resourceId": f"{packagename}:id/loginf_tv_login"}
    name_live = {"resourceId": f"{packagename}:id/name", "text": "LIVE"}
    btn_profile = {"xpath": f'//*[@resource-id="{packagename}:id/btn_profile"]/android.widget.LinearLayout[1]'}
    recycler_view_item = {"xpath": f'//*[@resource-id="{packagename}:id/recycler_view"]/android.widget.LinearLayout[1]'}
    et_recharge_code = {"resourceId": f"{packagename}:id/et_recharge_code"}
    recharge_code_confirm = {"resourceId": f"{packagename}:id/recharge_code_confirm"}
    btn_account_logout = {"resourceId": f"{packagename}:id/btn_account_logout"}
    btn_up = {"resourceId": f"{packagename}:id/btn_up"}
    v_demo = {"text": "v-demo"}
    permission_allow_button = {"resourceId": "com.android.permissioncontroller:id/permission_allow_button"}
    account_login_tv2 = {"resourceId": f"{packagename}:id/account_login_tv2"}
    loginf_et_username = {"resourceId": f"{packagename}:id/loginf_et_username"}
    et_pwd = {"resourceId": f"{packagename}:id/et_pwd"}
    remember_pwd_cb = {"resourceId": f"{packagename}:id/remember_pwd_cb"}
    imageView = {"resourceId": f"{packagename}:id/imageView"}
    tv_content={"resourceId": f"{packagename}:id/tv_content"}













