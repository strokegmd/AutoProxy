import urllib.request
import socket

import winreg

current_version = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion")
internet_settings = winreg.CreateKey(current_version, "Internet Settings")

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 YaBrowser/23.11.0.0 Safari/537.36"

def toggle_proxy(mode):
    winreg.SetValueEx(internet_settings, "ProxyEnable", 0, winreg.REG_DWORD, mode)

def set_proxy(proxy):
    winreg.SetValueEx(internet_settings, "ProxyServer", 0, winreg.REG_SZ, proxy)

def scrape_proxies(country, timeout, anonymity, ssl):
    url = f"https://api.proxyscrape.com/v2/?request=displayproxies&protocol=https&timeout={timeout}&country={country}&ssl={ssl}&anonymity={anonymity}"
    request = urllib.request.Request(url, headers={"User-Agent": user_agent})
    response = urllib.request.urlopen(request)

    return response.read().decode().splitlines()

def check_proxy(proxy, timeout):
    socket.setdefaulttimeout(timeout / 1000 + 1)

    url = "https://www.httpbin.org/ip"

    request = urllib.request.Request(url)
    request.set_proxy(proxy, "http")

    try:
        response = urllib.request.urlopen(request)
        return "origin" in response.read().decode() # checking if we are on httpbin.org website, because some bad proxies can return html error
    except:
        return False