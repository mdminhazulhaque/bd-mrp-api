#!/usr/bin/env python3

__author__ = "Md. Minhazul Haque"
__license__ = "GPLv3"

"""
Copyright (c) 2018 Md. Minhazul Haque
This file is part of mdminhazulhaque/bd-mrp-api
(see https://github.com/mdminhazulhaque/banglalionwimaxapi).
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

import requests
import re

class MRP():
    __headers = {
        'Cache-Control': 'no-cache',
        'Origin': 'http://www.passport.gov.bd',
        'Referer': 'http://www.passport.gov.bd/OnlineStatus.aspx',
        'X-MicrosoftAjax': 'Delta=true',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }

    __data = {
        'ctl00$ContentPlaceHolder1$ScriptManager1': 'ctl00$ContentPlaceHolder1$updPanelStatus|ctl00$ContentPlaceHolder1$btnVerify',
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        'ctl00$txtUserID': '',
        'ctl00$txtPassword': '',
        '__ASYNCPOST': 'true',
        'ctl00$ContentPlaceHolder1$btnVerify': 'Search'
    }
    
    def getCaptchaImageURL(self):
        response = requests.get('http://www.passport.gov.bd/OnlineStatus.aspx')
        
        for line in response.text.split("\n"):
            if "__VIEWSTATE" in line:
                soup = BeautifulSoup(line, "lxml")
                self.__data['__VIEWSTATE'] = soup.input.attrs['value']
            elif "__EVENTVALIDATION" in line:
                soup = BeautifulSoup(line, "lxml")
                self.__data['__EVENTVALIDATION'] = soup.input.attrs['value']
            elif "CaptchaImage.axd" in line:
                soup = BeautifulSoup(line, "lxml")
                CaptchaImageURL = soup.img.attrs['src']
                
        return self.__headers['Origin'] + '/' + CaptchaImageURL
    
    def getStatus(self, enrolmentid, dob, captchatext):
        self.__data['ctl00$ContentPlaceHolder1$txtSearchFormNo'] = enrolmentid
        self.__data['ctl00$ContentPlaceHolder1$txtSearchDOB'] = dob
        self.__data['ctl00$ContentPlaceHolder1$txtSearchVerify'] = captchatext        
        
        response = requests.post('http://www.passport.gov.bd/OnlineStatus.aspx', headers=self.__headers, data=self.__data).text
        
        e = "<li>The text you typed does not match the text in the image.</li>"
        if e in response: raise Exception(e.replace("<li>", "").replace("</li>", ""))
        
        regex = re.compile(r'<table\sclass=\"GridList\"(.*?)</table>', re.M|re.S) # M = multiline, S = dot as all
        table = regex.search(response).group(0)
        
        soup = BeautifulSoup(table, "lxml")
        values =  soup.find_all("tr")[2].find_all("td")
        
        info = {
            "Enrolment ID": values[0].text,
            "Status": values[1].text,
            "Full Name": values[2].text,
            "First Name": values[3].text,
            "Last Name": values[4].text,
            "Date of Birth": values[5].text,
            "Father's Name": values[6].text,
            "Mother's Name": values[7].text,
            "Permanent Address": {
                "Police Station": values[8].text,
                "District": values[9].text
            },
            "Present Address": {
                "Police Station": values[10].text,
                "District": values[11].text
            }
        }
        return info

if __name__ == "__main__":
    import argparse
    import sys
    import os
    import subprocess
    import shutil
    import json
    
    parser = argparse.ArgumentParser(description="Bangladesh MRP Status Checker", add_help=False)
    parser.add_argument('-e', dest='enrolmentid', action="store", required=True, type=str)
    parser.add_argument('-d', dest='dob', action="store", required=True, type=str)
    args = parser.parse_args()
    
    try:
        mrp = MRP()
        url = mrp.getCaptchaImageURL()
        
        TEMPFILE = "CaptchaImage.jpg"
        
        response = requests.get(url, stream=True)
        with open(TEMPFILE, "wb") as fp:
            shutil.copyfileobj(response.raw, fp)
        captcha = subprocess.check_output([
            "/usr/bin/kdialog",
            "--imginputbox",
            TEMPFILE
            ]).decode("utf-8").strip()
        os.unlink(TEMPFILE)
        
        status = mrp.getStatus(args.enrolmentid, args.dob, captcha)
        print(json.dumps(status, indent=2))
    except subprocess.CalledProcessError as cp:
        print("Captcha Text not provided")
    except Exception as r:
        print(r)
    
