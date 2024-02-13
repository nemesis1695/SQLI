# SQLI
SQLInjectionTester

This tool is a SQL Injection vulnerability testing tool specifically designed to check and test SQL Injection vulnerabilities in applications and websites. It is capable of automatically testing various input parameters of websites using different testing methodologies to search for weaknesses that could be exploited by SQL Injection attacks.

The main features of this tool include:

    Testing SQL Injection vulnerabilities in various URL parameters.
    Ability to use popular bypasses to check for vulnerabilities.
    Testing Blind SQL Injection vulnerabilities using various techniques.
    Testing the ORDER BY capability to determine the number of columns in a table.
    Testing UNION SELECT to retrieve information from other tables.
    Ability to use switches for different configurations and specific tests.

This tool is crucial for protecting websites and web applications against SQL Injection attacks and assists testers and developers in identifying and fixing potential vulnerabilities, thus enhancing the security of information and information systems.


Using SQLI :

python3 SQLI.py -u http://target.com/[?id=9]


Switches : 


   ("-B", "--blind", dest="blind", help="Blind SQL Injection technique (time-based or boolean-based)")
   
   ("-o", "--order-by", dest="order_by", action="store_true", help="Test ORDER BY functionality")
   
   ("-u", "--union-select", dest="union_select", action="store_true", help="Test UNION SELECT functionality")
   
   ("-h", "--help", action="help", help="Show this help message and exit")
   
