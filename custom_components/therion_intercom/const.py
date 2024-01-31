"""Constant for therion intercom."""

DOMAIN = "therion_intercom"
URL = "https://mb.therion.org"
URL_CODE = "/api/v1/auth/code"
URL_LOGIN = "/api/v1/auth/login"
URL_DATA = "/api/v1/contract"

HEADERS = {
    "Host": "mb.therion.org",
    "Content-Type": "application/json",
    "Connection": "keep-alive",
    "Accept": "*/*",
    "User-Agent": "Terion/1.0.9 (ru.televox.intercom; build:3; iOS 17.2.0) Alamofire/5.4.3",
}
