import math
import sqlite3

import genconfig
import loggerdb

## Indicators
price_list = loggerdb.price_list

# RS(I)
RS_list = []
RSI_list = []
RS_gain_list = []
RS_loss_list = []
avg_gain_list = []
avg_loss_list = []
def RSI():
    # We need a minimum of 2 candles to start RS calculations
    if len(price_list) >= 2:
        if price_list[-1] > price_list[-2]:
            gain = price_list[-1] - price_list[-2]
            RS_gain_list.append(gain)
            RS_loss_list.append(0)
        elif price_list[-1] < price_list[-2]:
            loss = price_list[-2] - price_list[-1]
            RS_loss_list.append(loss)
            RS_gain_list.append(0)

        # Do RS calculations if we have all requested periods
        if len(RS_gain_list) >= genconfig.RSIPeriod:
            if len(avg_gain_list) > 1:
                avg_gain_list.append(((avg_gain_list[-1] *\
                        (genconfig.RSIPeriod - 1)) + RS_gain_list[-1])\
                        / genconfig.RSIPeriod)
                avg_loss_list.append(((avg_loss_list[-1] *\
                        (genconfig.RSIPeriod - 1)) + RS_loss_list[-1])\
                        / genconfig.RSIPeriod)
            # Fist run, can't yet apply smoothing
            else:
                avg_gain_list.append(math.fsum(RS_gain_list[(\
                        genconfig.RSIPeriod * -1):]) / genconfig.RSIPeriod)
                avg_loss_list.append(math.fsum(RS_loss_list[(\
                        genconfig.RSIPeriod * -1):]) / genconfig.RSIPeriod)

            # Calculate and append current RS to RS_list
            RS_list.append(avg_gain_list[-1] / avg_loss_list[-1])

            # Calculate and append current RSI to RSI_list
            RSI_list.append(100 - (100 / (1 + RS_list[-1])))

    if genconfig.Indicator == 'RSI':
        if len(RSI_list) < 1:
            print('RSI: Not yet enough data to calculate')
        else:
            # RSI_list is externally accessible, so return NULL
            print('RSI:', RSI_list[-1])


# SMA
def SMAHelper(list1, period):
    if len(list1) >= period:
        SMA = math.fsum(list1[(period * -1):]) / period

        return SMA

SMA_list = []
def SMA():
    # We can start SMA calculations once we have SMAPeriod
    # candles, otherwise we append None until met
    if len(price_list) >= genconfig.SMAPeriod:
        SMA_list.append(SMAHelper(price_list, genconfig.SMAPeriod))


# Stochastic Oscillator
def FastStochKHelper(list1, period):
    if len(list1) >= period:
        LowestPeriod = min(float(s) for s in list1[(period * -1):])
        HighestPeriod = max(float(s) for s in list1[(period * -1):])
        FastStochK = ((list1[-1] - LowestPeriod) / (HighestPeriod\
                - LowestPeriod)) * 100

        return FastStochK

FastStochK_list = []
def FastStochK():
    # We can start FastStochK calculations once we have FastStochKPeriod
    # candles, otherwise we append None until met
    if len(price_list) >= genconfig.FastStochKPeriod:
        FastStochK_list.append(FastStochKHelper(price_list,\
                genconfig.FastStochKPeriod))

    if genconfig.Indicator == 'FastStochK':
        if len(FastStochK_list) < 1:
            print('FastStochK: Not yet enough data to calculate')
        else:
            # FastStochK_list is externally accessible, so return NULL
            print('FastStochK:', FastStochK_list[-1])


# StochRSIK
StochRSIK_list = []
def StochRSIK():
    # Call RSI
    RSI()
    # We can start FastStochRSIK calculations once we have
    # FastStochRSIKPeriod candles, otherwise we append None until met
    if len(RSI_list) >= genconfig.StochRSIKPeriod:
        StochRSIK_list.append(FastStochKHelper(RSI_list,\
                genconfig.StochRSIKPeriod))

    if genconfig.Indicator == 'StochRSIK':
        if len(StochRSIK_list) < 1:
            print('StochRSIK: Not yet enough data to calculate')
        else:
            # StochRSIK_list is externally accessible, so return NULL
            print('StochRSIK:', StochRSIK_list[-1])
