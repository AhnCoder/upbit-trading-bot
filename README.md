# Upbit Auto Trading Bot 🤖

업비트 API를 활용한 자동매매 봇입니다. 모멘텀 기반 트레이딩 전략을 사용하여 RSI, 볼린저 밴드 등의 기술적 지표로 매수/매도 시점을 자동으로 판단합니다.

## 주요 기능

- **자동 매수/매도**: RSI 과매도/과매수 구간과 볼린저 밴드를 활용한 자동 거래
- **손절/익절 관리**: 설정한 비율에 따른 자동 손절 및 익절
- **24/7 자동 운영**: 1분 간격으로 시장을 모니터링하고 거래
- **환경 변수 기반 설정**: 쉬운 설정 및 관리

## 트레이딩 전략

### 매수 조건
- RSI < 30 (과매도 구간)
- 현재가가 볼린저 밴드 하단 근처 (102% 이내)

### 매도 조건
1. **손절**: 손실률이 설정값 이상일 때 (기본: -5%)
2. **익절**: 수익률이 설정값 이상일 때 (기본: +10%)
3. **RSI 매도**: RSI > 70 (과매수) AND 수익률 > 2%

## 설치 방법

### 1. 저장소 클론
```bash
git clone https://github.com/AhnCoder/upbit-trading-bot.git
cd upbit-trading-bot
```

### 2. 가상환경 생성 및 활성화
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
```

### 3. 패키지 설치
```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정
```bash
cp .env.example .env
```

`.env` 파일을 열어서 다음 정보를 입력하세요:
```
UPBIT_ACCESS_KEY=your_access_key_here
UPBIT_SECRET_KEY=your_secret_key_here
TRADING_COIN=KRW-BTC
BUY_AMOUNT=5000
STOP_LOSS_PERCENT=5
TAKE_PROFIT_PERCENT=10
```

## Upbit API 키 발급

1. [업비트 Open API 관리](https://upbit.com/mypage/open_api_management) 페이지 접속
2. "Open API Key 발급" 클릭
3. 다음 권한 선택:
   - 자산 조회
   - 주문 조회
   - 주문하기
4. IP 주소 등록 (선택사항, 보안을 위해 권장)
5. Access Key와 Secret Key를 `.env` 파일에 입력

⚠️ **보안 주의사항**: Secret Key는 한 번만 표시되므로 안전하게 보관하세요.

## 사용 방법

### 봇 실행
```bash
python trading_bot.py
```

### 실행 화면 예시
```
===== Upbit Trading Bot Started =====
Trading Coin: KRW-BTC
Buy Amount: 5000 KRW
Stop Loss: 5.0%
Take Profit: 10.0%
=====================================

[2026-01-07 23:30:00] 상태 확인...
보유 KRW: 10000, 보유 BTC: 0.00000000
[매수 시그널] RSI: 28.50, Price: 130500000, Lower Band: 128000000.00
[매수 완료] KRW-BTC, 금액: 5000 KRW
```

## 설정 옵션

| 환경 변수 | 설명 | 기본값 |
|----------|------|-------|
| `UPBIT_ACCESS_KEY` | 업비트 Access Key | 필수 |
| `UPBIT_SECRET_KEY` | 업비트 Secret Key | 필수 |
| `TRADING_COIN` | 거래할 코인 | `KRW-BTC` |
| `BUY_AMOUNT` | 매수 금액 (KRW) | `5000` |
| `STOP_LOSS_PERCENT` | 손절 비율 (%) | `5` |
| `TAKE_PROFIT_PERCENT` | 익절 비율 (%) | `10` |
| `RSI_PERIOD` | RSI 기간 | `14` |
| `RSI_OVERSOLD` | RSI 과매도 기준 | `30` |
| `RSI_OVERBOUGHT` | RSI 과매수 기준 | `70` |
| `BOLLINGER_PERIOD` | 볼린저 밴드 기간 | `20` |
| `BOLLINGER_STD` | 볼린저 밴드 표준편차 | `2` |

## ⚠️ 주의사항

1. **투자 위험**: 암호화폐 투자는 변동성이 크므로 투자 손실이 발생할 수 있습니다.
2. **테스트 필수**: 실제 자금을 사용하기 전에 소액으로 테스트하세요.
3. **모니터링**: 봇 실행 중에도 주기적으로 상태를 확인하세요.
4. **전략 이해**: 사용하는 트레이딩 전략을 충분히 이해한 후 사용하세요.
5. **API 키 보안**: `.env` 파일은 절대 공개 저장소에 업로드하지 마세요.

## 기술 스택

- Python 3.9+
- pyupbit: 업비트 API 래퍼
- pandas: 데이터 분석
- numpy: 수치 계산
- python-dotenv: 환경 변수 관리
- ta / pandas-ta: 기술적 지표 계산

## 라이선스

MIT License

## 기여하기

Pull Request는 언제나 환영입니다! 버그 리포트나 기능 제안은 Issues에 등록해주세요.

## 면책 조항

이 봇은 교육 및 연구 목적으로 제공됩니다. 실제 거래에 사용하여 발생하는 손실에 대해서는 개발자가 책임지지 않습니다. 투자는 본인의 판단과 책임 하에 진행하세요.
