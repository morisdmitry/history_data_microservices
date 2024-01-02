# API-Service

For recieving klines by needed period from binance api
result is to send mini periods to next microservice "request_service" through kafka message broker

there id only one handler, calls period_klines
body looks like:
{
"symbol": "ETHBUSD",
"start_date": "2022-02-05",
"end_date": "2023-03-05",
"period": "4h"
}
