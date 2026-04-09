import requests


class LottoFetchError(Exception):
    pass


LOTTO_HISTORY_URL = "https://www.dhlottery.co.kr/lt645/selectPstLt645Info.do"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.dhlottery.co.kr/",
    "Accept": "application/json, text/plain, */*",
}


def fetch_draws(start_draw_no: int, end_draw_no: int) -> list[dict]:
    params = {
        "srchStrLtEpsd": start_draw_no,
        "srchEndLtEpsd": end_draw_no,
    }

    response = requests.get(
        LOTTO_HISTORY_URL,
        params=params,
        headers=HEADERS,
        timeout=20,
    )
    response.raise_for_status()

    content_type = response.headers.get("content-type", "")
    if "json" not in content_type.lower():
        preview = response.text[:300].replace("\n", " ")
        raise LottoFetchError(f"JSON 응답이 아닙니다. preview={preview}")

    data = response.json()

    rows = data.get("data", {}).get("list")
    if rows is None:
        raise LottoFetchError("응답에 data.list가 없습니다.")

    return rows