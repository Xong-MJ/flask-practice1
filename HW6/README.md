# HW6

송민준 · 24013813

## 실행 방법

    python -m venv .venv
    .venv\Scripts\activate
    pip install pandas scikit-learn==1.9.1 joblib flask flask-restx jupyter ipykernel

- `.venv` 에서 jupyter 로 `hw6.ipynb` 를 Restart → Run All. 단계 ⑥ 이 `sales_model.pkl` 을 만든다.
- `flask --app app run` 뒤 http://127.0.0.1:5000/api/docs 에서 `POST /sales/predict` → Try it out → Execute.
- 요청 `{"quantity": 40, "unit_price": 200000}` → 응답 `{"total_sales": 8000000}` (`docs.png`).

| 단계 | 결과 |
|---|---|
| ① 읽기와 나누기 | 1004 줄 → training 803 · test 201 (random_state=0) |
| ② test R² | linear 0.862 · linear + qp 1.0 · tree (제한 없음) 0.994 |
| ④ max_depth 표 | 1 → 제한 없음 : training 0.361 → 1.000, test 0.346 → 0.994 |
| ⑤ cross-validation | depth 8 : 0.992 ± 0.000, depth 12 : 0.995 ± 0.000 |
| ⑥ 서버에 올린 model | linear regression + qp (`sales_model.pkl`) |

## 단계 ③ 답

실제 규칙은 `총액 = 수량 × 단가` 로 두 열을 곱한 것이다. linear regression 의 모양은 `a × 수량 + b × 단가 + c` 처럼 열마다 숫자를 곱해 더하는 것뿐이라 두 열의 곱을 표현할 수 없고, 그래서 곱셈을 직선으로 흉내 낸 0.862 에서 멈춘다.

qp (= 수량 × 단가) 를 feature 로 더하면 곱셈이 이미 열 안에 들어 있어 model 은 `총액 = 1 × qp` 만 찾으면 된다. 실제로 coef 가 [0, 0, 1], 절편이 0 으로 나와 test R² 가 1.0 이 되었다.

## 단계 ⑤ 결정과 이유

**max_depth 8.** cross-validation 평균이 depth 8 에서 0.992, depth 12 에서 0.995 로 0.003 차이뿐인데 잎은 250 개 대 781 개로 세 배다. 점수가 거의 같으면 단순한 쪽을 고른다.

training 1.000 과 test 0.994 의 차이가 작은 것은 이 문제에 규칙이 실제로 있어서 깊게 외워도 우연이 아니라 규칙을 외우게 되기 때문이다.

## 단계 ⑦ 답

**linear regression + qp 를 올렸다.** 수량 40 · 단가 200,000 의 실제 총액은 40 × 200,000 = 8,000,000 원이다. linear + qp 는 8,000,000 으로 정확히 맞혔고, 단계 ⑤ 에서 고른 tree (depth 8) 는 7,362,301 로 약 64 만 원 (8 %) 틀렸다.

tree 는 잎마다 training 총액의 평균을 답하는 계단이라 곱셈을 근사할 뿐이지만, linear + qp 는 실제 공식 `총액 = qp` 를 그대로 찾았다. 잎 250 개짜리 tree 보다 계수 셋과 절편 하나인 model 이 더 단순하고 더 정확하다. 서버에서는 학습 때와 똑같이 `x["qp"] = x["quantity"] * x["unit_price"]` 를 만들어 넣는다.
