import talib
import numpy as np


class TechnicalAnalysis:
    def __init__(self, open, high, low, close, volume):
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume

        self.setter_periods()

    def setter_periods(self, ema_period=14,
                       rsi_period=14,
                       stoch_period=14,
                       mom_period=14,
                       adx_period=14,
                       willr_period=14,
                       cci_period=14,
                       roc_period=10,
                       stochrsi_period=14,
                       trix_period=30,
                       mfi_period=14,
                       ultosc_1_period=7,
                       ultosc_2_period=14,
                       ultosc_3_period=21,
                       aroon_period=14,
                       aroonosc_period=14,
                       atr_period=14,
                       adoscfast_period=3,
                       adoscslow_period=10):
        self.ema_period = ema_period
        self.rsi_period = rsi_period
        self.stoch_period = stoch_period
        self.mom_period = mom_period
        self.adx_period = adx_period
        self.willr_period = willr_period
        self.cci_period = cci_period
        self.roc_period = roc_period
        self.stochrsi_period = stochrsi_period
        self.trix_period = trix_period
        self.mfi_period = mfi_period
        self.ultosc_1_period = ultosc_1_period
        self.ultosc_2_period = ultosc_2_period
        self.ultosc_3_period = ultosc_3_period
        self.aroon_period = aroon_period
        self.aroonosc_period = aroonosc_period
        self.atr_period = atr_period
        self.adoscfast_period = adoscfast_period
        self.adoscslow_period = adoscslow_period

    def execute(self):
        ema = talib.EMA(self.close, self.ema_period)
        rsi = talib.RSI(self.close, self.rsi_period)
        stoch_K, stoch_D = talib.STOCHF(self.high, self.low, self.close, fastk_period=self.stoch_period)
        macd, macdsignal, macdhist = talib.MACD(self.close)
        sar = talib.SAR(self.high, self.low)
        mom = talib.MOM(self.close, self.mom_period)
        adx = talib.ADX(self.high, self.low, self.close, self.adx_period)
        willr = talib.WILLR(self.high, self.low, self.close, self.willr_period)
        cci = talib.CCI(self.high, self.low, self.close, self.cci_period)
        roc = talib.ROC(self.close, self.roc_period)
        stochrsi_K, stochrsi_D = talib.STOCHRSI(self.close, self.stochrsi_period)
        trix = talib.TRIX(self.close, self.trix_period)
        mfi = talib.MFI(self.high, self.low, self.close, self.volume, self.mfi_period)
        ultosc = talib.ULTOSC(self.high, self.low, self.close, self.ultosc_1_period, self.ultosc_2_period, self
                              .ultosc_3_period)
        aroon_down, aroon_up = talib.AROON(self.high, self.low, self.aroon_period)
        aroonosc = talib.AROONOSC(self.high, self.low, self.aroonosc_period)
        atr = talib.ATR(self.high, self.low, self.close, self.atr_period)
        ad = talib.AD(self.high, self.low, self.close, self.volume)
        obv = talib.OBV(self.close, self.volume)
        adosc = talib.ADOSC(self.high, self.low, self.close, self.volume, self.adoscfast_period, self.adoscslow_period)

        spread_ema = ema - self.close
        spread_stoch = stoch_K - stoch_D
        spread_stochrsi = stochrsi_K - stochrsi_D
        spread_aroon = aroon_up - aroon_down

        return np.array([
            self.close,
            spread_ema,
            rsi,
            macd,
            macdhist,
            stoch_K,
            spread_stoch,
            sar,
            mom,
            adx,
            willr,
            cci,
            roc,
            spread_stochrsi,
            trix,
            mfi,
            ultosc,
            aroon_down,
            aroon_up,
            spread_aroon,
            aroonosc,
            atr,
            ad,
            obv,
            adosc,
        ]).transpose()


class TechnicalAnalysisComplete:
    def __init__(self, open, high, low, close, volume):
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume

    def execute(self):
        return np.array([self.open,
                         self.high,
                         self.low,
                         self.close,
                         self.volume,
                         talib.HT_DCPERIOD(self.close),
                         talib.HT_DCPHASE(self.close),
                         talib.HT_PHASOR(self.close)[0],
                         talib.HT_PHASOR(self.close)[1],
                         talib.HT_SINE(self.close)[0],
                         talib.HT_SINE(self.close)[1],
                         talib.HT_TRENDMODE(self.close),
                         talib.ADX(self.high, self.low, self.close),
                         talib.ADXR(self.high, self.low, self.close),
                         talib.APO(self.close),
                         talib.AROON(self.high, self.low)[0],
                         talib.AROON(self.high, self.low)[1],
                         talib.AROONOSC(self.high, self.low),
                         talib.BOP(self.open, self.high, self.low, self.close),
                         talib.CCI(self.high, self.low, self.close),
                         talib.CMO(self.close),
                         talib.DX(self.high, self.low, self.close),
                         talib.MACD(self.close)[0],
                         talib.MACD(self.close)[1],
                         talib.MACD(self.close)[2],
                         talib.MACDEXT(self.close)[0],
                         talib.MACDEXT(self.close)[1],
                         talib.MACDEXT(self.close)[2],
                         talib.MACDFIX(self.close)[0],
                         talib.MACDFIX(self.close)[1],
                         talib.MACDFIX(self.close)[2],
                         talib.MFI(self.high, self.low, self.close, self.volume),
                         talib.MINUS_DI(self.high, self.low, self.close),
                         talib.MINUS_DM(self.high, self.low),
                         talib.MOM(self.close),
                         talib.PLUS_DI(self.high, self.low, self.close),
                         talib.PLUS_DM(self.high, self.low),
                         talib.PPO(self.close),
                         talib.ROC(self.close),
                         talib.ROCP(self.close),
                         talib.ROCR(self.close),
                         talib.ROCR100(self.close),
                         talib.RSI(self.close),
                         talib.STOCH(self.high, self.low, self.close)[0],
                         talib.STOCH(self.high, self.low, self.close)[1],
                         talib.STOCHF(self.high, self.low, self.close)[0],
                         talib.STOCHF(self.high, self.low, self.close)[1],
                         talib.STOCHRSI(self.close)[0],
                         talib.STOCHRSI(self.close)[1],
                         talib.TRIX(self.close),
                         talib.ULTOSC(self.high, self.low, self.close),
                         talib.WILLR(self.high, self.low, self.close),
                         talib.BBANDS(self.close)[0],
                         talib.BBANDS(self.close)[1],
                         talib.BBANDS(self.close)[2],
                         talib.DEMA(self.close),
                         talib.EMA(self.close),
                         talib.HT_TRENDLINE(self.close),
                         talib.KAMA(self.close),
                         talib.MA(self.close),
                         talib.MAMA(self.close)[0],
                         talib.MAMA(self.close)[1],
                         talib.MIDPOINT(self.close),
                         talib.MIDPRICE(self.high, self.low),
                         talib.SAR(self.high, self.low),
                         talib.SAREXT(self.high, self.low),
                         talib.T3(self.close),
                         talib.TEMA(self.close),
                         talib.TRIMA(self.close),
                         talib.WMA(self.close),
                         talib.AVGPRICE(self.open, self.high, self.low, self.close),
                         talib.MEDPRICE(self.high, self.low),
                         talib.TYPPRICE(self.high, self.low, self.close),
                         talib.WCLPRICE(self.high, self.low, self.close),
                         talib.ATR(self.high, self.low, self.close),
                         talib.NATR(self.high, self.low, self.close),
                         talib.TRANGE(self.high, self.low, self.close),
                         talib.AD(self.high, self.low, self.close, self.volume),
                         talib.ADOSC(self.high, self.low, self.close, self.volume),
                         talib.OBV(self.close, self.volume),
                         talib.CDL2CROWS(self.open, self.high, self.low, self.close),
                         talib.CDL3BLACKCROWS(self.open, self.high, self.low, self.close),
                         talib.CDL3INSIDE(self.open, self.high, self.low, self.close),
                         talib.CDL3LINESTRIKE(self.open, self.high, self.low, self.close),
                         talib.CDL3OUTSIDE(self.open, self.high, self.low, self.close),
                         talib.CDL3STARSINSOUTH(self.open, self.high, self.low, self.close),
                         talib.CDL3WHITESOLDIERS(self.open, self.high, self.low, self.close),
                         talib.CDLABANDONEDBABY(self.open, self.high, self.low, self.close),
                         talib.CDLADVANCEBLOCK(self.open, self.high, self.low, self.close),
                         talib.CDLBELTHOLD(self.open, self.high, self.low, self.close),
                         talib.CDLBREAKAWAY(self.open, self.high, self.low, self.close),
                         talib.CDLCLOSINGMARUBOZU(self.open, self.high, self.low, self.close),
                         talib.CDLCONCEALBABYSWALL(self.open, self.high, self.low, self.close),
                         talib.CDLCOUNTERATTACK(self.open, self.high, self.low, self.close),
                         talib.CDLDARKCLOUDCOVER(self.open, self.high, self.low, self.close),
                         talib.CDLDOJI(self.open, self.high, self.low, self.close),
                         talib.CDLDOJISTAR(self.open, self.high, self.low, self.close),
                         talib.CDLDRAGONFLYDOJI(self.open, self.high, self.low, self.close),
                         talib.CDLENGULFING(self.open, self.high, self.low, self.close),
                         talib.CDLEVENINGDOJISTAR(self.open, self.high, self.low, self.close),
                         talib.CDLEVENINGSTAR(self.open, self.high, self.low, self.close),
                         talib.CDLGAPSIDESIDEWHITE(self.open, self.high, self.low, self.close),
                         talib.CDLGRAVESTONEDOJI(self.open, self.high, self.low, self.close),
                         talib.CDLHAMMER(self.open, self.high, self.low, self.close),
                         talib.CDLHANGINGMAN(self.open, self.high, self.low, self.close),
                         talib.CDLHARAMI(self.open, self.high, self.low, self.close),
                         talib.CDLHARAMICROSS(self.open, self.high, self.low, self.close),
                         talib.CDLHIGHWAVE(self.open, self.high, self.low, self.close),
                         talib.CDLHIKKAKE(self.open, self.high, self.low, self.close),
                         talib.CDLHIKKAKEMOD(self.open, self.high, self.low, self.close),
                         talib.CDLHOMINGPIGEON(self.open, self.high, self.low, self.close),
                         talib.CDLIDENTICAL3CROWS(self.open, self.high, self.low, self.close),
                         talib.CDLINNECK(self.open, self.high, self.low, self.close),
                         talib.CDLINVERTEDHAMMER(self.open, self.high, self.low, self.close),
                         talib.CDLKICKING(self.open, self.high, self.low, self.close),
                         talib.CDLKICKINGBYLENGTH(self.open, self.high, self.low, self.close),
                         talib.CDLLADDERBOTTOM(self.open, self.high, self.low, self.close),
                         talib.CDLLONGLEGGEDDOJI(self.open, self.high, self.low, self.close),
                         talib.CDLLONGLINE(self.open, self.high, self.low, self.close),
                         talib.CDLMARUBOZU(self.open, self.high, self.low, self.close),
                         talib.CDLMATCHINGLOW(self.open, self.high, self.low, self.close),
                         talib.CDLMATHOLD(self.open, self.high, self.low, self.close),
                         talib.CDLMORNINGDOJISTAR(self.open, self.high, self.low, self.close),
                         talib.CDLMORNINGSTAR(self.open, self.high, self.low, self.close),
                         talib.CDLONNECK(self.open, self.high, self.low, self.close),
                         talib.CDLPIERCING(self.open, self.high, self.low, self.close),
                         talib.CDLRICKSHAWMAN(self.open, self.high, self.low, self.close),
                         talib.CDLRISEFALL3METHODS(self.open, self.high, self.low, self.close),
                         talib.CDLSEPARATINGLINES(self.open, self.high, self.low, self.close),
                         talib.CDLSHOOTINGSTAR(self.open, self.high, self.low, self.close),
                         talib.CDLSHORTLINE(self.open, self.high, self.low, self.close),
                         talib.CDLSPINNINGTOP(self.open, self.high, self.low, self.close),
                         talib.CDLSTALLEDPATTERN(self.open, self.high, self.low, self.close),
                         talib.CDLSTICKSANDWICH(self.open, self.high, self.low, self.close),
                         talib.CDLTAKURI(self.open, self.high, self.low, self.close),
                         talib.CDLTASUKIGAP(self.open, self.high, self.low, self.close),
                         talib.CDLTHRUSTING(self.open, self.high, self.low, self.close),
                         talib.CDLTRISTAR(self.open, self.high, self.low, self.close),
                         talib.CDLUNIQUE3RIVER(self.open, self.high, self.low, self.close),
                         talib.CDLUPSIDEGAP2CROWS(self.open, self.high, self.low, self.close),
                         talib.CDLXSIDEGAP3METHODS(self.open, self.high, self.low, self.close),
                         ]).transpose()
