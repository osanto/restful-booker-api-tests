# Restful-Booker

[![CI](https://github.com/osanto/restful-booker-api-tests/actions/workflows/ci.yml/badge.svg)](https://github.com/osanto/restful-booker-api-tests/actions) [![Allure Report](https://img.shields.io/badge/Allure_Report-GitHub_Pages-blue?logo=googlechrome)](https://osanto.github.io/restful-booker-api-tests/)

API tests for [API playground by Mark Winteringham](https://restful-booker.herokuapp.com/) implemented with Python, requests, and Allure reports.

**Prerequisites:** Python 3.11+

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/osanto/restful-booker-api-tests.git
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:

   Copy `.env.example` to `.env` and fill in your credentials:

   ```
   cp .env.example .env
   ```

   Edit `.env` and set your actual `LOGIN` and `PASSWORD` values.

## Run tests

```bash
pytest
```

Allure results are written to `allure-results/` (see `pytest.ini`).

To view the report locally (requires [Allure CLI](https://docs.qameta.io/allure/)):

```bash
allure serve allure-results
```

## CI and report

CI runs on push to any branch (except `main`) and on pull requests targeting `main`. The latest Allure report is published to [GitHub Pages](https://osanto.github.io/restful-booker-api-tests/). For CI to pass, set `LOGIN` and `PASSWORD` in the repo’s **Settings → Secrets and variables → Actions**.
