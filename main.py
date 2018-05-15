import urllib
import urllib2
from bs4 import BeautifulSoup

class Scraping:
    def __init__(self,url,sessionId):
        self.url = url
        self.sessionId = sessionId

    def make_request_report(self,start_date,end_date):
        #the http headers are useful to simulate a particular browser (some sites deny
        #access to non-browsers (bots, etc.)
        #also needed to pass the content type.
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'es-CO,es-419;q=0.9,es;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Cookie': 'ASP.NET_SessionId='+self.sessionId+'; StationParam=START_DATE='+start_date+' 1:00:00&START_TIME=01:00&END_DATE='+end_date+' 0:00:00&END_TIME=00:00',
            'Host': '201.245.192.252:81',
            'Referer': 'http://201.245.192.252:81/frmStationReport.aspx',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36'
        }

        req = urllib2.Request(self.url, headers=headers)
        f= urllib2.urlopen(req)

        return f.read()

    def make_request_survey(self,url,start_date,end_date):
        #the http headers are useful to simulate a particular browser (some sites deny
        #access to non-browsers (bots, etc.)
        #also needed to pass the content type.
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'es-ES,es;q=0.8,en;q=0.6',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Content-Length':'7434',
            'Content-Type':'application/x-www-form-urlencoded',
            'Cookie': 'ASP.NET_SessionId='+self.sessionId+'; StationParam=START_DATE='+start_date+' 1:00:00&START_TIME=01:00&END_DATE='+end_date+' 0:00:00&END_TIME=00:00',
            'Host': '201.245.192.252:81',
            'Origin': 'http://201.245.192.252:81',
            'Referer': url,
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36'
        }

        with open('encoding.txt', 'r') as myfile:
            data=myfile.read().replace('\n', '')
        req = urllib2.Request(url, data, headers)
        f= urllib2.urlopen(req)

        return f.read()

    def get_beautiful_response(self,text_plain,id_item):
        soup = BeautifulSoup(text_plain, 'html.parser')
        return BeautifulSoup(str(soup.find_all(id=id_item)[0]), 'html.parser')

    def get_monitors_values(self,table,hour):
        index = 26+((hour-1)*13)
        results = {}
        table = table.find_all("td")
        results["Datetime"] = table[index].get_text()
        results["SO2"] = table[index+1].get_text()
        results["Temperatura"] = table[index+2].get_text()
        results["NO"] = table[index+3].get_text()
        results["NOX"] = table[index+4].get_text()
        results["Precipitacion"] = table[index+5].get_text()
        results["Dir.viento"] = table[index+6].get_text()
        results["Vel.viento"] = table[index+7].get_text()
        results["PM2.5"] = table[index+8].get_text()
        results["PM10"] = table[index+9].get_text()
        results["OZONO"] = table[index+10].get_text()
        results["CO"] = table[index+11].get_text()
        results["NO2"] = table[index+12].get_text()
        return results



scraping = Scraping("http://201.245.192.252:81/NewGrid.aspx","03esqlbye05mofnphel0bo25")
print scraping.make_request_survey("http://201.245.192.252:81/frmStationReport.aspx","14-05-2018","15-05-2018")
text_plain = scraping.make_request_report("14-05-2018","15-05-2018")
table = scraping.get_beautiful_response(text_plain,"C1WebGrid1")
response = scraping.get_monitors_values(table,1)
print response

#print f.read()

"""
print(soup.find_all("td")[26])# 1 - Date and time
print(soup.find_all("td")[27])# 2 - S02: ppb
print(soup.find_all("td")[28])# 3 - N02: ppb
print(soup.find_all("td")[29])# 4 - CO: ppm
print(soup.find_all("td")[30])# 5 - OZONO: ppb
print(soup.find_all("td")[31])# 6 - PM10: ug/m3
print(soup.find_all("td")[32])# 7 - PM2.5: ug/m3
print(soup.find_all("td")[33])# 8 - Vel. viento m/s
print(soup.find_all("td")[34])# 9 - Dir. viento Grados
print(soup.find_all("td")[35])# 10 - Precipitacion mm
print(soup.find_all("td")[36])# 11 - NOX ppb
print(soup.find_all("td")[37])# 12 - NO ppb
print(soup.find_all("td")[38])# 13 - Temperatura C"""
