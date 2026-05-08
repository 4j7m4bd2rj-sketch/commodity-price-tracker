import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import rcParams
import os

# 한글 폰트 설정 (Mac)
rcParams['font.family'] = 'AppleGothic'
rcParams['axes.unicode_minus'] = False

def make_chart():
    file_path = '원자재가격.xlsx'

    if not os.path.exists(file_path):
        print('원자재가격.xlsx 파일이 없어요. crawl.py 먼저 실행해주세요.')
        return

    df = pd.read_excel(file_path)
    items = df['품목'].unique()

    fig, axes = plt.subplots(len(items), 1, figsize=(12, 4 * len(items)))
    fig.suptitle('식품 원자재 가격 추이', fontsize=16, fontweight='bold', y=1.01)

    if len(items) == 1:
        axes = [axes]

    for ax, item in zip(axes, items):
        item_df = df[df['품목'] == item].copy()
        item_df = item_df.sort_values('날짜')

        prices = item_df['가격(USD)'].values
        dates = item_df['날짜'].values
        changes = item_df['변동률(%)'].values

        # 선 색상: 마지막 변동률 기준
        last_change = changes[-1] if len(changes) > 0 else 0
        line_color = '#e74c3c' if last_change >= 0 else '#3498db'

        ax.plot(dates, prices, color=line_color, linewidth=2, marker='o', markersize=5)
        ax.fill_between(range(len(prices)), prices,
                        alpha=0.1, color=line_color)
        ax.set_xticks(range(len(dates)))
        ax.set_xticklabels(dates, rotation=45, ha='right', fontsize=8)
        ax.set_title(f'{item}', fontsize=13, fontweight='bold')
        ax.set_ylabel('가격 (USD)', fontsize=10)
        ax.grid(True, alpha=0.3)

        # 마지막 가격 + 변동률 표시
        last_price = prices[-1]
        change_pct = changes[-1]
        color = '#e74c3c' if change_pct >= 0 else '#3498db'
        sign = '+' if change_pct >= 0 else ''
        ax.annotate(f'{last_price:.2f} USD\n{sign}{change_pct:.2f}%',
                    xy=(len(prices)-1, last_price),
                    xytext=(10, 0), textcoords='offset points',
                    fontsize=10, color=color, fontweight='bold')

    plt.tight_layout()
    plt.savefig('원자재가격_차트.png', dpi=150, bbox_inches='tight')
    print('차트 저장 완료: 원자재가격_차트.png')
    plt.show()

if __name__ == '__main__':
    make_chart()