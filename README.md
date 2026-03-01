# Restful-Booker

[![CI](https://github.com/osanto/restful-booker-api-tests/actions/workflows/ci.yml/badge.svg)](https://github.com/osanto/restful-booker-api-tests/actions) [![Allure Report](https://img.shields.io/badge/Allure_Report-GitHub_Pages-blue?logo=googlechrome)](https://osanto.github.io/restful-booker-api-tests/)

API tests for [API playground by Mark Winteringham](https://restful-booker.herokuapp.com/)
implemented with python, requests and outputing results with allure reports.

## Installation
1. Clone the repository:
   ``` 
   git clone https://github.com/osanto/restful-booker-api-tests.git
   ```
3. Install dependencies
   ``` 
   pip install -r requirements.txt
   ```
3. Set up environment variables:

   Copy `.env.example` to `.env` and fill in your credentials:

   ```
   cp .env.example .env
   ```

   Edit `.env` and set your actual `LOGIN` and `PASSWORD` values.
   
