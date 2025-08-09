from odoo import http
class TestApi(http.Controller):
    @http.route("/test/api",methods=["GET"],type="http",autho="none",csrf=False)
    def test_api(self):
        print("inside in test api")
