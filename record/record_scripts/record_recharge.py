# coding: utf-8
#
import uiautomator2 as u2

d = u2.connect()

d.xpath('//*[@resource-id="tech.gtt.frontapp.stb.demo:id/recycler_view"]/android.widget.LinearLayout[1]').click()
d(resourceId="tech.gtt.frontapp.stb.demo:id/et_recharge_code").click()
d.send_keys("1158472753844023", clear=True)
d(resourceId="tech.gtt.frontapp.stb.demo:id/recharge_code_confirm").click()