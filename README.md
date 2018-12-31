# BD MRP Status Checker API

This (dump) API allows you to check the status of your passport using correct Enrollment ID, Date of Birth and Captcha Text.

The captcha image will be shown using ImageMagick and you have to provide the captcha text manually. :-(

## Requirment

* python3
* BeautifulSoup
* libxml
* Pillow

## How to Run

```bash
$ MRP.py -e 100100000123456 -d 12/03/1994
Enter the captcha text: L3AD2
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

- [ ] Remove Captcha prompt using AntiCaptcha API
- [ ] Bugs?
