# Interview exercise

Two short questions, about 15 minutes each. **Use any AI tool you like.** We
want to see how you work with it: what you ask, how you check its answers and
what you do when it is wrong. Python may not be your main language; that is
fine.

Everything runs on your machine. There is no network, database or cloud
account involved.

## Setup

Python 3.10 or later.

```sh
git clone https://github.com/hasanmazik/maj-interview.git
cd maj-interview
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
pytest
```

Four tests fail. That is expected.

## Question 1: Order sync

`order_sync/sync.py` fetches pending orders from an inventory API, a page at a
time, and reserves stock for each one. `order_sync/fakes.py` stands in for the
API. Read it, but do not change it or the tests.

- **1a. Retries.** The API sometimes answers 503 (unavailable) or 429 (too many
  requests). Retry those, up to 3 attempts in total, with a short wait between
  attempts. Do not retry other statuses.
  Tests: `tests/test_q1a_retries.py`
- **1b. Missing orders.** Some orders never get reserved, and
  `tests/test_q1b_missing_orders.py` fails. Find out why and fix it. Show us
  how you confirmed the cause.

## Question 2: Code review

`review/orders_service.py` is a pull request from a teammate. The problems in
it are not specific to Python; they would be problems in any language. The file
is not meant to be run.

- **2a.** Find the problems and fix them in the file. Add a comment starting
  with `# FIX:` next to each change, saying what was wrong and why it matters.
- **2b.** Tell us the three problems you would block the merge for, and why.
