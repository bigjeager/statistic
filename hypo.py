# z-test for two-sample proportion test
# https://www.hellovaia.com/explanations/math/statistics/confidence-intervals/
import math
from scipy import stats


n1, f1, n2, f2 = 3685614, 127729, 3690137, 120900  # x1 = exp, x2: base
prac_thres_rel = 0.05                    #相对基准起码提升5%/降低-5%，才认为业务能感知
alpha = 0.05                             #统计意义显著

z_score_thres = stats.norm.ppf(1 - alpha/2) #双边检测, zscore = 1.96 when alpha = 0.05
p1 = f1/n1
p2 = f2/n2
pool_prob = (f1 + f2) / (n1 + n2)
pool_standard_error = math.sqrt(p1*(1-p1)/n1 + p2*(1-p2)/n2)

center = p1 - p2
z_statistic = center/pool_standard_error
p_value = 1 - stats.norm.cdf(abs(z_statistic))

# 方法一：theory based method，置信区间公式: x +- z(0.05) * SE，SE用估计方法得到
margin_error = z_score_thres * pool_standard_error
conf_interval = (round(center - margin_error,4), round(center + margin_error,4))

# 除以base数据，得到相对提升
center_rel = round(center/p2, 4)
conf_interval_rel = list(map(lambda x: round(x/p2, 4), conf_interval))

# 是否统计意义上置信，置信区间要同号
statistic_conf = True if conf_interval_rel[0] * conf_interval_rel[1] > 0 else False

# 是否实际意义上置信，正向置信时，下界大于实际业务感知阈值；负向置信时，上界小于负的实际业务感知阈值
if statistic_conf and conf_interval_rel[0] > 0:
    pratically_conf = True if conf_interval_rel[0] > prac_thres_rel else False
    final_result = '置信正'
elif statistic_conf and conf_interval_rel[0] < 0:
    pratically_conf = True if conf_interval_rel[1] < -1 * prac_thres_rel else False
    final_result = '置信负'
else:
    pratically_conf = False
    final_result = '不置信'

{"z_statistic": z_statistic, 
 "p_value" : p_value, 
 "绝对变化": round(center, 4), 
 "绝对置信区间": conf_interval,
 "相对变化" : center_rel, 
 "相对置信区间": conf_interval_rel,
 "统计显著": statistic_conf,
 "业务显著": pratically_conf,
 "置信判断": final_result}
