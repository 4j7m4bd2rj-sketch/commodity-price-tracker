import requests
import pandas as pd
from datetime import datetime
import os

API_KEY = '11912bdc6ff18191dad951d8463a8ad8'  # 발급받은 FRED API 키 입력

ITEMS = {
    '쌀': 'PRICENPQUSDM',
    '밀': 'PWHEAMTUSDM',
    '옥수수': 'PMAIZMTUSDM',
    '대두': 'PSOYBUSDM',
    '설탕': 'PSUGAISAUSDM',
}

def get_fred_history(series_id, start_date='2020-01-01'):
    url = 'https://api.stlouisfed.org/fred/series/observations'
    params = {
        'series_id': series_id,
        'api_key': API_KEY,
        'file_type': 'json',
        'observation_start': start_date,
        'sort_order': 'asc',
    }
    res = requests.get(url, params=params)
    data = res.json()
    valid = [o for o in data['observations'] if o['value'] != '.']
    return [(o['date'], float(o['value'])) for o in valid]

def main():
    all_rows = []

    for item, series_id in ITEMS.items():
        print(f'{item} 과거 데이터 수집 중...')
        try:
            history = get_fred_history(series_id)
            for date, price in history:
                all_rows.append({
                    '날짜': date,
                    '품목': item,
                    '가격(USD)': price,
                })
            print(f'  → {len(history)}개 데이터 수집 완료')
        except Exception as e:
            print(f'  → 오류: {e}')

    df = pd.DataFrame(all_rows)

    # 품목별 전월대비 변동 계산
    df = df.sort_values(['품목', '날짜']).reset_index(drop=True)
    df['전월대비변동'] = df.groupby('품목')['가격(USD)'].diff().round(2)
    df['변동률(%)'] = (df['전월대비변동'] / df.groupby('품목')['가격(USD)'].shift(1) * 100).round(2)

    file_path = '원자재가격.xlsx'
    df.to_excel(file_path, index=False)
    print(f'\n저장 완료: {file_path} ({len(df)}행)')

if __name__ == '__main__':
    main()