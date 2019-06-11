import tushare as ts
from matplotlib import pyplot
import matplotlib.pyplot as plt

TOKEN = '23d23f5a51a2ebaae6f967dffbc2b2d677a042eb6a23288ac3397389' #替换为你的tushare token，注册链接：

pro = ts.pro_api(token=TOKEN)  #pro_api需要token

day_cnt = 600   #数据上限为600

#定投相关设置，尝试过一些盘中加仓和减仓操作，似乎还是傻瓜式定投收益较好
fixed_investment_amount_yuan = 500  # 每次基金的定投金额
extra_investment_amount_yuan = 500  # 每次基金的定投金额
investment_interval_day = 10  # 基金定投时间间隔
investment_total_yuan = 0  # 累计的原始投资金额
investment_quantity_total = 0  # 累计的基金份数
investment_balance_yuan = 0  # 空闲资金
investment_actual_total_yuan = 0  # 实际的基金现值

decrease_counter = 0  # 连续N天指数下跌则卖出sell_out_percentage
COUNTER_LIMIT = 4
sell_out_percentage = 0.25
buy_more_decrease_percentage = -0.9


sell_all = 0

sort_i = 0

#以下用于绘制折线图
investment_quantity_total_plot = []
investment_total_yuan_plot = []
earning_ratio = []
plot_x_len = 0


#获取上证指数数据
SH_PeArray = pro.index_dailybasic(ts_code='000001.SH', fields='trade_date,pe')

#获取ETF基金
ETF_50 = ts.get_hist_data('510500')
print('交易日   市盈率 收盘价 幅度变化 基金已买份额 原始投资金额 当前空闲资金 当前基金总额')

for i in range(day_cnt):
    # 数据是倒序的
    sort_i = day_cnt - i - 1;

    if SH_PeArray.trade_date[sort_i] == '20190419':
        plot_x_len = i
        break

    # 是否需要全部卖出
    if SH_PeArray.pe[sort_i] > 20:
        investment_balance_yuan = investment_balance_yuan + investment_quantity_total * ETF_50.close[sort_i]
        investment_quantity_total = 0
        print('全部卖出')

    # 是否需要卖出部分
    if sort_i < (day_cnt - 2) and SH_PeArray.pe[sort_i] < SH_PeArray.pe[sort_i - 1]:
        if decrease_counter <= COUNTER_LIMIT:
            decrease_counter += 1

    else:
        if decrease_counter > 0:
            decrease_counter -= 2

    # 如果需要卖出，则更新余额和份额
    if decrease_counter >= COUNTER_LIMIT and investment_quantity_total > 0:
        decrease_counter = 0
        #print('卖出部分')
        # investment_quantity_total = investment_quantity_total * (1 - sell_out_percentage)
        # investment_balance_yuan = investment_balance_yuan + investment_quantity_total * sell_out_percentage * \
        #                           ETF_50.close[sort_i]

        # 是否需要额外定投
    #if (SH_PeArray.pe[sort_i] < 13) and (ETF_50.p_change[sort_i] < buy_more_decrease_percentage):
        #pdb.in_trace()
        #investment_quantity_total = investment_quantity_total + extra_investment_amount_yuan / ETF_50.close[sort_i]
        #investment_total_yuan = investment_total_yuan + extra_investment_amount_yuan
        #print('加仓')

    # 是否定投
    if (SH_PeArray.pe[sort_i] < 15.0) and ((i % investment_interval_day) == 0):
        print('定投')
        investment_quantity_total = investment_quantity_total + fixed_investment_amount_yuan / ETF_50.close[sort_i]
        investment_total_yuan = investment_total_yuan + fixed_investment_amount_yuan

    print(SH_PeArray.trade_date[sort_i], SH_PeArray.pe[sort_i], ETF_50.close[sort_i], ETF_50.p_change[sort_i], \
          round(investment_quantity_total, 2), round(investment_total_yuan, 2), round(investment_balance_yuan, 2),
          round(investment_quantity_total * ETF_50.close[sort_i] + investment_balance_yuan, 2))

    investment_quantity_total_plot.append( round(investment_quantity_total * ETF_50.close[sort_i] + investment_balance_yuan, 2))
    investment_total_yuan_plot.append(round(investment_total_yuan, 2))
    earning_ratio.append(round((investment_quantity_total * ETF_50.close[sort_i] + investment_balance_yuan) / investment_total_yuan, 2))


plt.figure()
plt.plot(range(0, plot_x_len), investment_quantity_total_plot)
plt.plot(range(0, plot_x_len), investment_total_yuan_plot)
plt.show()


plt.plot(range(0, plot_x_len), earning_ratio)
plt.show()