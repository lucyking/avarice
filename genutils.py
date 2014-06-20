import threading
import genconfig
import os

def do_every (interval, worker_func, iterations = 0):
    ''' Basic support for configurable/iterable threading'''
    if iterations != 1:
        threading.Timer (
            interval,
            do_every, [interval, worker_func,\
                    0 if iterations == 0 else iterations-1]
        ).start ();
    worker_func ();

def PrettyMinutes(seconds, place):
    minutes = seconds / 60
    if len(str(minutes).split('.')[1]) > place:
        pm = round(minutes, place)
    else:
        pm = minutes
    return pm

# Configure recorder
def PrepareRecord():
    if not genconfig.PersistTrades:
        try:
            os.rmdir(genconfig.RecordPath)
        except Exception:
            pass
    os.makedirs(genconfig.RecordPath, exist_ok=True)

def RecordTrades(action, price, amount):
    if genconfig.SimulatorTrading:
        f = open(genconfig.RecordPath + '/' + genconfig.RecordSimName, 'a')
    else:
        f = open(genconfig.RecordPath + '/' + genconfig.RecordTradeName)
    line = action + ' ' + str(amount) + genconfig.Asset + ' at ' + str(price)\
            + genconfig.Currency
    f.write(line + '\n')
    f.close
