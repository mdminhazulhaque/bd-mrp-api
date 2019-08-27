# BD MRP Status Checker API

This (dump) API allows you to check the status of your passport using correct Enrollment ID, Date of Birth and Captcha Text.

It can also be done from the following address but I tried to make this scriptable.

http://passport.gov.bd/OnlineStatus.aspx

The captcha image will be shown using ImageMagick and you have to provide the captcha text manually. :-(

## Requirment

* python3
* BeautifulSoup
* libxml
* Pillow

## How to Run

```bash
$ MRP.py -e 100100000123456 -d 12/03/1994 -k ANTICAPTCHA-KEY
{
  "Enrolment ID": "100100000123456",
  "Status": "QC Succeed Ready for Dispatch",
  "Full Name": "FOO BAR",
  "First Name": "FOO",
  "Last Name": "BAR",
  "Date of Birth": "12/03/1994",
  "Father's Name": "FOO BAR BABA",
  "Mother's Name": "FOO BAR MAMA",
  "Permanent Address": {
    "Police Station": "EXAMPLE PS",
    "District": "RAJSHAHI"
  },
  "Present Address": {
    "Police Station": "EXAMPLE PS",
    "District": "DHAKA"
  }
}

```

You can ignore the API Key. In that case, you need to input the captcha manually. Run without `-k` flag.

```bash
$ MRP.py -e 100100000123456 -d 12/03/1994
Open the following URL in browser and enter the captcha text:

http://www.passport.gov.bd/CaptchaImage.axd?guid=35d578dd-0125-4a9c-b972-7d303686e562

Captcha: QAGN8
{
  "Enrolment ID": "100100000123456",
  "Status": "QC Succeed Ready for Dispatch",
  "Full Name": "FOO BAR",
  "First Name": "FOO",
  "Last Name": "BAR",
  "Date of Birth": "12/03/1994",
  "Father's Name": "FOO BAR BABA",
  "Mother's Name": "FOO BAR MAMA",
  "Permanent Address": {
    "Police Station": "EXAMPLE PS",
    "District": "RAJSHAHI"
  },
  "Present Address": {
    "Police Station": "EXAMPLE PS",
    "District": "DHAKA"
  }
}

```

## TODO

- [x] Remove Captcha prompt using AntiCaptcha API
- [ ] Bugs?
