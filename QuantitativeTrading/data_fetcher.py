#!/usr/bin/env python3
import baostock as bs
import pandas as pd
import json
import os
from datetime import datetime, timedelta

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def login():
    bs.login()


def logout():
    bs.logout()


def get_trade_dates():
    today = datetime.now()
    start = (today - timedelta(days=90)).strftime("%Y-%m-%d")
    end = today.strftime("%Y-%m-%d")
    rs = bs.query_trade_dates(start_date=start, end_date=end)
    dates = []
    while rs.next():
        dates.append(rs.get_row_data())
    df = pd.DataFrame(dates, columns=["date", "is_trading_day"])
    trading_days = df[df["is_trading_day"] == "1"]["date"].tolist()
    return trading_days


def get_all_stocks(date=None):
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    rs = bs.query_stock_basic()
    data = []
    while rs.next():
        data.append(rs.get_row_data())
    df = pd.DataFrame(data, columns=rs.fields)
    df = df[(df["type"] == "1") & (df["status"] == "1")]
    return df


def get_stock_data(code, start_date, end_date, frequency="d"):
    rs = bs.query_history_k_data_plus(
        code,
        "date,code,open,high,low,close,preclose,volume,amount,turn,pctChg,isST",
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
        adjustflag="2",
    )
    data = []
    while rs.next():
        data.append(rs.get_row_data())
    if not data:
        return pd.DataFrame()
    df = pd.DataFrame(data, columns=rs.fields)
    for col in ["open", "high", "low", "close", "preclose", "volume", "amount", "turn", "pctChg"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df[df["isST"] != "1"]
    return df


def get_top_movers(days=30, top_n=50):
    today = datetime.now()
    end_date = today.strftime("%Y-%m-%d")
    start_date = (today - timedelta(days=days)).strftime("%Y-%m-%d")

    rs = bs.query_stock_basic()
    all_stocks = []
    while rs.next():
        all_stocks.append(rs.get_row_data())
    df_stocks = pd.DataFrame(all_stocks, columns=rs.fields)
    df_stocks = df_stocks[(df_stocks["type"] == "1") & (df_stocks["status"] == "1")]
    sh_main = df_stocks[df_stocks["code"].str.startswith("sh.6")]
    sz_main = df_stocks[df_stocks["code"].str.startswith("sz.0") | df_stocks["code"].str.startswith("sz.3")]
    candidates = pd.concat([sh_main, sz_main])

    results = []
    for _, row in candidates.iterrows():
        code = row["code"]
        stock_data = get_stock_data(code, start_date, end_date)
        if stock_data.empty:
            continue
        latest = stock_data.iloc[-1]
        results.append({
            "code": code,
            "name": row.get("code_name", ""),
            "close": latest["close"],
            "pctChg": latest["pctChg"],
            "volume": latest["volume"],
            "amount": latest["amount"],
            "turn": latest["turn"],
            "high": latest["high"],
            "low": latest["low"],
            "open": latest["open"],
        })

    df = pd.DataFrame(results)
    if df.empty:
        return df

    df = df.sort_values("pctChg", ascending=False)
    top_gainers = df.head(top_n)
    top_losers = df.tail(top_n)
    top_volume = df.sort_values("amount", ascending=False).head(top_n)

    return {
        "top_gainers": top_gainers.to_dict("records"),
        "top_losers": top_losers.to_dict("records"),
        "top_volume": top_volume.to_dict("records"),
        "all_data": df.to_dict("records"),
    }


def get_index_data(start_date, end_date):
    indices = {
        "sh.000001": "上证指数",
        "sz.399001": "深证成指",
        "sz.399006": "创业板指",
    }
    result = {}
    for code, name in indices.items():
        df = get_stock_data(code, start_date, end_date)
        if not df.empty:
            result[name] = df.to_dict("records")
    return result


def save_data(data, filename):
    filepath = os.path.join(OUTPUT_DIR, filename)
    if isinstance(data, pd.DataFrame):
        data.to_csv(filepath, index=False, encoding="utf-8-sig")
    else:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    return filepath


def main():
    login()

    today = datetime.now().strftime("%Y-%m-%d")
    start_30d = (datetime.now() - timedelta(days=45)).strftime("%Y-%m-%d")
    start_60d = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")

    print("=== 获取指数数据 ===")
    index_data = get_index_data(start_30d, today)
    save_data(index_data, f"index_{today}.json")
    for name, records in index_data.items():
        if records:
            print(f"  {name}: 最新收盘 {records[-1]['close']}")

    print("\n=== 获取涨跌幅排行 ===")
    movers = get_top_movers(days=5, top_n=30)
    if movers:
        save_data(movers, f"movers_{today}.json")
        gainers = movers.get("top_gainers", [])
        if gainers:
            print(f"  涨幅前5:")
            for g in gainers[:5]:
                print(f"    {g['code']} {g['name']}: {g['pctChg']:+.2f}%")

    print("\n=== 获取热门股票K线数据(涨幅前30) ===")
    hot_codes = []
    if movers and movers.get("top_gainers"):
        hot_codes = [g["code"] for g in movers["top_gainers"][:30]]
        for code in hot_codes:
            df = get_stock_data(code, start_60d, today)
            if not df.empty:
                save_data(df, f"kline_{code}_{today}.csv")
                name = next((g["name"] for g in movers["top_gainers"] if g["code"] == code), "")
                print(f"  {code} {name}: {len(df)}条K线数据已保存")

    logout()
    print("\n=== 数据获取完成 ===")


if __name__ == "__main__":
    main()