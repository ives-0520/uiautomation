# coding: utf-8
#
import uiautomator2 as u2

d = u2.connect()

d(text="v-demo").click()
d(resourceId="com.android.permissioncontroller:id/permission_allow_button").click()
d(resourceId="tech.gtt.frontapp.stb.demo:id/account_login_tv2").click()
d(resourceId="tech.gtt.frontapp.stb.demo:id/loginf_et_username").click()
d.send_keys("0609@ipwangxin.cn", clear=True)
d(resourceId="tech.gtt.frontapp.stb.demo:id/et_pwd").click()
d.send_keys("123456", clear=True)
d(resourceId="tech.gtt.frontapp.stb.demo:id/remember_pwd_cb").click()
d(resourceId="tech.gtt.frontapp.stb.demo:id/loginf_tv_login").click()
d(resourceId="tech.gtt.frontapp.stb.demo:id/imageView").click()