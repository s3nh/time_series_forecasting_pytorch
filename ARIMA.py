from util import *
import eval
import numpy as np
import pyflux as pf


if __name__ == '__main__':

    ts, data = load_data("./data/NSW2013.csv", columnName="TOTALDEMAND")
    # ts, data = load_data("../data/bike_hour.csv", indexName="dteday", columnName="cnt")
    # ts, data = load_data("../data/traffic_data_in_bits.csv",  columnName="value")
    #  ts, data = load_data("../data/TAS2016.csv", indexName="SETTLEMENTDATE", columnName="TOTALDEMAND")
    # ts, data = util.load_data("../data/AEMO/TT30GEN.csv", indexName="TRADING_INTERVAL", columnName="VALUE")

    dataset = ts.values[:]
    X = np.array(dataset,dtype="float64")
    train, test = divideTrainTest(dataset)
    history = [x for x in train]
    predictions = []
    realTestY = []

    for t in range(len(test)):
        # order = st.arma_order_select_ic(history, max_ar=5, max_ma=5, ic=['aic', 'bic', 'hqic'])
        # print(order.bic_min_order)
            #model = ARIMA(history, order=(3, 2, 1))
        model = pf.ARIMA(data=np.array(history), ar=4, ma=4, family=pf.Normal())
        model.fit(method="MLE")

        output = model.predict(1, intervals=False)

        yhat = output.values[0][0]

        predictions.append(yhat)
        obs = test[t]
        history.append(obs)
        realTestY.append(obs)
        print('predicted=%f, expected=%f' % (yhat, obs))

    realTestY = np.array(test)
    predictions = np.array(predictions).reshape(-1)
    MAE = eval.calcMAE(realTestY, predictions)
    RMSE = eval.calcRMSE(realTestY, predictions)
    MAPE = eval.calcSMAPE(realTestY, predictions)
    print('Test MAE: %.8f' % MAE)
    print('Test RMSE: %.8f' % RMSE)
    print('Test MAPE: %.8f' % MAPE)
