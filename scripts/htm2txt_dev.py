from bs4 import BeautifulSoup
import urllib.request
soup = BeautifulSoup(urllib.request.urlopen('https://www.ietf.org/rfc/rfc2854.txt').read(), "html.parser")
t = soup.get_text()
print(t)
