import urllib.request

def get_ip(proxy):
    url = f"http://httpbin.org/ip"

    request = urllib.request.Request(url)
    if proxy != None:
        request.set_proxy(proxy, "http")

    response = urllib.request.urlopen(request)
    ip = response.read().decode().split(': "')[1][:-4]
    if ", " in ip:
        ip = ip.split(", ")[1]

    return ip

def country_to_code(country):
    if country.lower() == "usa":
        return "US"
    if country.lower() == "russia":
        return "RU"
    if country.lower() == "ukraine":
        return "UA"