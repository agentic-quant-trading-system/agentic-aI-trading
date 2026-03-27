import azure.functions as func
import logging

app = func.FunctionApp()

@app.timer_trigger(schedule="0 0 21 * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False)
def daily_market_fetch(myTimer: func.TimerRequest) -> None:
    logging.info('Automated trigger started: The architecture works perfectly!')
