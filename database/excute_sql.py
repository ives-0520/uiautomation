import requests
import json

class EnduserDatabase:
    def __init__(self):
        self.url = 'https://gtt-enduser-qa-lion.vdemosit.com/query'
        self.headers = {
            'Content-Type': 'application/json',
            'Cookie': 'AWSALB=yyqKalQBzYBiEi6TCGm+EAl2/D8FNh1J7zXX1I0xNFayjg02ic0jKuxXg0PANmsSmSQc/QoFr3PpM6mmZwzxBWYP/mhMdmuwUqzsZwGMThZyVz9gmhMbH8MCr6OL; AWSALBCORS=yyqKalQBzYBiEi6TCGm+EAl2/D8FNh1J7zXX1I0xNFayjg02ic0jKuxXg0PANmsSmSQc/QoFr3PpM6mmZwzxBWYP/mhMdmuwUqzsZwGMThZyVz9gmhMbH8MCr6OL; AWSALB=q2BnvIYaS9q3sOjSUXJKTRqaHZTC3rmSU8elrgUlV/mLGm1VviWZ105YO3pI7E67dm7aaXIcFH9eSL2EAzsMPYEyM94GMa4gNQoDA63mRPmeifEBTcYmuswRx8u7; AWSALBCORS=q2BnvIYaS9q3sOjSUXJKTRqaHZTC3rmSU8elrgUlV/mLGm1VviWZ105YO3pI7E67dm7aaXIcFH9eSL2EAzsMPYEyM94GMa4gNQoDA63mRPmeifEBTcYmuswRx8u7'
        }
        self.connection_params = {
            "host": "gtt-enduser-rds-sit.chndooyhh10e.us-west-2.rds.amazonaws.com",
            "user": "read_only",
            "password": "Goose@123",
            "database": "gtt_enduser_account_db",
            "port": 3306
        }

    def query_unify_verify_code(self, email):
        data = {
            "query": f"SELECT unify_verify_code FROM `gtt_enduser_account_db`.`gtt_enduser_account_verification_code_info` WHERE `email` = '{email}' order by update_time DESC LIMIT 1;",
            "connection_params": self.connection_params
        }
        response = requests.post(self.url, headers=self.headers, data=json.dumps(data))
        if response.status_code == 200:
            try:
                return response.json()['results'][0]['unify_verify_code']
            except Exception as e:
                print('JSON decode error:', e)
                return response.text
        else:
            print('Request failed:', response.status_code)
            return response.text


if __name__ == "__main__":
    db = EnduserDatabase()
    result = db.query_unify_verify_code("ives_0705@qq.com")
    print(result)