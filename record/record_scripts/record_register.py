#
import uiautomator2 as u2

d = u2.connect()
d(text="eng").click()
d(resourceId="tech.gtt.frontapp.stb.demo:id/sign_up_tv2").click()
d.xpath('//*[@resource-id="tech.gtt.frontapp.stb.demo:id/layout_email_view"]/android.widget.LinearLayout[1]').click()
d.send_keys("ives_0705@gmail.com", clear=True)
d(resourceId="tech.gtt.frontapp.stb.demo:id/tv_verify").click()
d(resourceId="tech.gtt.frontapp.stb.demo:id/et_verify_code").click()
d.send_keys("5754", clear=True)
d(resourceId="tech.gtt.frontapp.stb.demo:id/et_pwd").click()
d(resourceId="tech.gtt.frontapp.stb.demo:id/et_pwd").click()
d.send_keys("123456", clear=True)
d(resourceId="tech.gtt.frontapp.stb.demo:id/resetpwd_tv_submit").click()
d(resourceId="tech.gtt.frontapp.stb.demo:id/tv_agreement_agree").click()
d(resourceId="tech.gtt.frontapp.stb.demo:id/btn_down").click()