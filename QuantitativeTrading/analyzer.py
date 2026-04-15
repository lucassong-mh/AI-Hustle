#!/usr/bin/env python3
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


def compute_ma(series, periods):
    result = {}
    for p in periods:
        ma = series.rolling(window=p, min_periods=1).mean()
        result[f"MA{p}"] = ma
    return result


def compute_ema(series, period):
    return series.ewm(span=period, adjust=False).mean()


def compute_macd(close, fast=12, slow=26, signal=9):
    ema_fast = compute_ema(close, fast)
    ema_slow = compute_ema(close, slow)
    dif = ema_fast - ema_slow
    dea = compute_ema(dif, signal)
    macd_bar = 2 * (dif - dea)
    return dif, dea, macd_bar


def compute_kdj(high, low, close, n=9, m1=3, m2=3):
    lowest = low.rolling(window=n, min_periods=1).min()
    highest = high.rolling(window=n, min_periods=1).max()
    rsv = (close - lowest) / (highest - lowest) * 100
    rsv = rsv.fillna(50)
    k = rsv.ewm(com=m1 - 1, adjust=False).mean()
    d = k.ewm(com=m2 - 1, adjust=False).mean()
    j = 3 * k - 2 * d
    return k, d, j


def compute_rsi(close, period=14):
    delta = close.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi


def compute_boll(close, period=20, std_dev=2):
    ma = close.rolling(window=period, min_periods=1).mean()
    std = close.rolling(window=period, min_periods=1).std()
    upper = ma + std_dev * std
    lower = ma - std_dev * std
    return upper, ma, lower


def compute_volume_ratio(volume, period=5):
    avg_vol = volume.rolling(window=period, min_periods=1).mean()
    return volume / avg_vol.replace(0, np.nan)


def analyze_technical(df):
    if df.empty or len(df) < 5:
        return None

    close = df["close"]
    high = df["high"]
    low = df["low"]
    volume = df["volume"]

    mas = compute_ma(close, [5, 10, 20, 60])
    for k, v in mas.items():
        df[k] = v

    dif, dea, macd_bar = compute_macd(close)
    df["DIF"] = dif
    df["DEA"] = dea
    df["MACD_bar"] = macd_bar

    k, d, j = compute_kdj(high, low, close)
    df["K"] = k
    df["D_val"] = d
    df["J"] = j

    rsi = compute_rsi(close)
    df["RSI"] = rsi

    boll_upper, boll_mid, boll_lower = compute_boll(close)
    df["BOLL_upper"] = boll_upper
    df["BOLL_mid"] = boll_mid
    df["BOLL_lower"] = boll_lower

    df["VOL_ratio"] = compute_volume_ratio(volume)

    return df


def generate_signals(df, stock_code="", stock_name=""):
    if df is None or df.empty or len(df) < 10:
        return {}

    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else latest

    signals = {
        "code": stock_code,
        "name": stock_name,
        "close": float(latest.get("close", 0)),
        "pctChg": float(latest.get("pctChg", 0)),
        "volume": float(latest.get("volume", 0)),
        "turn": float(latest.get("turn", 0)) if pd.notna(latest.get("turn", 0)) else 0,
        "score": 0,
        "signals": [],
    }

    score = 0

    ma5 = latest.get("MA5", np.nan)
    ma10 = latest.get("MA10", np.nan)
    ma20 = latest.get("MA20", np.nan)
    ma60 = latest.get("MA60", np.nan)
    close_val = latest["close"]

    if pd.notna(ma5) and pd.notna(ma10):
        if close_val > ma5 > ma10:
            score += 2
            signals["signals"].append(f"均线多头排列(短期): 收盘{close_val:.2f} > MA5 {ma5:.2f} > MA10 {ma10:.2f}")
        elif close_val < ma5 < ma10:
            score -= 2
            signals["signals"].append(f"均线空头排列: 收盘{close_val:.2f} < MA5 {ma5:.2f} < MA10 {ma10:.2f}")

    if pd.notna(ma20):
        if close_val > ma20:
            score += 1
            signals["signals"].append(f"站上20日均线({ma20:.2f})")
        else:
            score -= 1
            signals["signals"].append(f"跌破20日均线({ma20:.2f})")

    dif = latest.get("DIF", np.nan)
    dea = latest.get("DEA", np.nan)
    prev_dif = prev.get("DIF", np.nan)
    prev_dea = prev.get("DEA", np.nan)
    if pd.notna(dif) and pd.notna(dea) and pd.notna(prev_dif) and pd.notna(prev_dea):
        if prev_dif <= prev_dea and dif > dea:
            score += 3
            signals["signals"].append("MACD金叉")
        elif prev_dif >= prev_dea and dif < dea:
            score -= 3
            signals["signals"].append("MACD死叉")
        if dif > 0 and dea > 0:
            score += 1
            signals["signals"].append("MACD双线上零轴(多头)")
        elif dif < 0 and dea < 0:
            score -= 1
            signals["signals"].append("MACD双线下零轴(空头)")

    k_val = latest.get("K", np.nan)
    d_val = latest.get("D_val", np.nan)
    j_val = latest.get("J", np.nan)
    prev_k = prev.get("K", np.nan)
    prev_d = prev.get("D_val", np.nan)
    if pd.notna(k_val) and pd.notna(d_val) and pd.notna(prev_k) and pd.notna(prev_d):
        if prev_k <= prev_d and k_val > d_val:
            score += 2
            signals["signals"].append("KDJ金叉")
        elif prev_k >= prev_d and k_val < d_val:
            score -= 2
            signals["signals"].append("KDJ死叉")
        if pd.notna(j_val):
            if j_val > 100:
                score -= 1
                signals["signals"].append(f"KDJ超买(J={j_val:.1f})")
            elif j_val < 0:
                score += 1
                signals["signals"].append(f"KDJ超卖(J={j_val:.1f})")

    rsi_val = latest.get("RSI", np.nan)
    if pd.notna(rsi_val):
        if rsi_val > 70:
            score -= 2
            signals["signals"].append(f"RSI超买({rsi_val:.1f})")
        elif rsi_val < 30:
            score += 2
            signals["signals"].append(f"RSI超卖({rsi_val:.1f})")
        elif 40 <= rsi_val <= 60:
            score += 1
            signals["signals"].append(f"RSI中性区({rsi_val:.1f})")

    boll_upper = latest.get("BOLL_upper", np.nan)
    boll_lower = latest.get("BOLL_lower", np.nan)
    boll_mid = latest.get("BOLL_mid", np.nan)
    if pd.notna(boll_upper) and pd.notna(boll_lower):
        if close_val > boll_upper:
            score -= 1
            signals["signals"].append(f"突破布林上轨({boll_upper:.2f})")
        elif close_val < boll_lower:
            score += 1
            signals["signals"].append(f"跌破布林下轨({boll_lower:.2f})")
        boll_width = (boll_upper - boll_lower) / boll_mid if boll_mid > 0 else 0
        prev_width = (prev.get("BOLL_upper", 0) - prev.get("BOLL_lower", 0)) / prev.get("BOLL_mid", 1) if prev.get("BOLL_mid", 0) > 0 else 0
        if boll_width < prev_width * 0.8:
            signals["signals"].append("布林带缩口，可能变盘")

    vol_ratio = latest.get("VOL_ratio", np.nan)
    if pd.notna(vol_ratio):
        if vol_ratio > 2.0 and close_val > prev["close"]:
            score += 2
            signals["signals"].append(f"放量上涨(量比{vol_ratio:.1f})")
        elif vol_ratio > 2.0 and close_val < prev["close"]:
            score -= 2
            signals["signals"].append(f"放量下跌(量比{vol_ratio:.1f})")
        elif vol_ratio < 0.5:
            signals["signals"].append(f"缩量(量比{vol_ratio:.1f})")

    pct_chg = latest.get("pctChg", 0)
    if pd.notna(pct_chg):
        if pct_chg > 9.5:
            score -= 1
            signals["signals"].append(f"涨停或接近涨停({pct_chg:+.2f}%)，追高风险大")
        elif pct_chg < -9.5:
            signals["signals"].append(f"跌停或接近跌停({pct_chg:+.2f}%)")
        elif 2 <= pct_chg <= 7:
            score += 1
            signals["signals"].append(f"涨幅适中({pct_chg:+.2f}%)")

    signals["score"] = score

    if score >= 5:
        signals["recommendation"] = "强烈看多"
    elif score >= 3:
        signals["recommendation"] = "看多"
    elif score >= 1:
        signals["recommendation"] = "偏多"
    elif score <= -5:
        signals["recommendation"] = "强烈看空"
    elif score <= -3:
        signals["recommendation"] = "看空"
    elif score <= -1:
        signals["recommendation"] = "偏空"
    else:
        signals["recommendation"] = "中性"

    _low = df["low"].astype(float)
    _high = df["high"].astype(float)
    support = float(_low.tail(20).min()) if len(df) >= 20 else float(_low.min())
    resistance = float(_high.tail(20).max()) if len(df) >= 20 else float(_high.max())
    signals["support"] = round(support, 2)
    signals["resistance"] = round(resistance, 2)
    signals["buy_price_range"] = f"{close_val * 0.98:.2f} - {close_val * 1.02:.2f}"
    signals["stop_loss"] = round(close_val * 0.95, 2)
    signals["target_price"] = round(resistance, 2)

    return signals


def main():
    today = datetime.now().strftime("%Y-%m-%d")

    movers_file = os.path.join(OUTPUT_DIR, f"movers_{today}.json")
    if not os.path.exists(movers_file):
        print("请先运行 data_fetcher.py 获取数据")
        return

    with open(movers_file, "r") as f:
        movers = json.load(f)

    gainers = movers.get("top_gainers", [])
    print(f"=== 分析涨幅榜前 {len(gainers)} 只股票技术面 ===\n")

    all_signals = []
    for stock in gainers[:30]:
        code = stock["code"]
        kline_file = os.path.join(OUTPUT_DIR, f"kline_{code}_{today}.csv")
        if not os.path.exists(kline_file):
            print(f"  跳过 {code}: 无K线数据")
            continue

        df = pd.read_csv(kline_file)
        df = analyze_technical(df)
        if df is None:
            continue

        signals = generate_signals(df, code, stock.get("name", ""))
        if signals:
            all_signals.append(signals)
            print(f"  {code} {signals.get('name','')}: 评分={signals['score']}, 判定={signals['recommendation']}")
            for s in signals["signals"][:3]:
                print(f"    - {s}")
            print(f"    支撑={signals['support']}, 压力={signals['resistance']}, 止损={signals['stop_loss']}")

    all_signals.sort(key=lambda x: x["score"], reverse=True)

    result = {
        "date": today,
        "total_analyzed": len(all_signals),
        "signals": all_signals,
        "top_picks": all_signals[:5],
    }

    filepath = os.path.join(OUTPUT_DIR, f"analysis_{today}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2, default=str)
    print(f"\n=== 分析完成，结果已保存到 {filepath} ===")


if __name__ == "__main__":
    main()