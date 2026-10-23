# Interview exercise

There are two short questions, about 15 minutes each.

**Use any AI tool you like.** We want to see how you work with it: what you
ask, how you check its answers, and what you do when it is wrong. The code is
in Python. If Python is not your main language, that is fine. We do not score
syntax.

Everything runs on your machine. You do not need a network connection, a
database or a cloud account.

## Setup

You need Python 3.10 or later.

```sh
git clone https://github.com/hasanmazik/maj-interview.git
cd maj-interview
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
pytest
```

You should see **4 failed, 3 passed**. That is expected. The failing tests are
the work for Question 1.

## Question 1: Order sync

`order_sync/sync.py` gets pending orders from an inventory API, one page at a
time. Then it reserves stock for each order.

`order_sync/fakes.py` is a fake version of that API. Its docstring explains how
it behaves. Read it, but do not change it. Do not change the tests.

**1a. Retries.** The API sometimes answers with a temporary error: 503 or 429.
Change the code so it tries again when that happens. Make at most 3 attempts in
total, and wait a short time between attempts. Do not retry any other status
code.
Tests: `tests/test_q1a_retries.py`

**1b. Missing orders.** Some orders are never reserved, so
`tests/test_q1b_missing_orders.py` fails. Find out why, and fix it. Show us how
you confirmed the cause.

**Done when:** `pytest` shows **7 passed**, and you can explain each change you
made.

## Question 2: Code review

`review/orders_service.py` is a pull request from a teammate. Each function has
a docstring that says what it should do. The code has several problems. None of
them is specific to Python; each one would be a problem in any language. You do
not need to run this file.

**2a. Find and fix.** Fix each problem in the file. Next to each change, add a
comment that starts with `# FIX:` and says what was wrong and why it matters.

**2b. Prioritise.** Tell us which three problems you would block the merge
for, and why.

**Done when:** you have fixed every problem you found, each fix has a `# FIX:`
comment, and you have named your top three.
