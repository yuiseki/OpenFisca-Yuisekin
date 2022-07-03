"""
児童手当の実装
"""

import numpy as np
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable
from openfisca_yuisekin.entities import 世帯


class 児童手当(Variable):
    value_type = float
    entity = 世帯
    definition_period = MONTH
    label = "保護者への児童手当"
    reference = "https://www.city.shibuya.tokyo.jp/kodomo/teate/teate/jido_t.html"
    documentation = """
    渋谷区の児童手当制度

    - 〒150-8010 東京都渋谷区宇田川町1-1
    - 渋谷区子ども青少年課子育て給付係
    - 03-3463-2558
    """

    def formula(対象世帯, 対象期間, parameters):
        児童手当 = parameters(対象期間).福祉.育児.児童手当
        扶養控除所得金額 = parameters(対象期間).税金.扶養控除所得金額

        # 世帯で最も高い所得の人が基準となる
        世帯高所得 = 対象世帯("世帯高所得", 対象期間)
        # 扶養人数が1人ではない場合を考慮する
        世帯所得一覧 = 対象世帯.members("所得", 対象期間)
        扶養人数 = 対象世帯.sum(世帯所得一覧 < 扶養控除所得金額)
        所得上限限度額 = 児童手当.所得上限限度額.calc(扶養人数)
        所得条件 = 世帯高所得 <= 所得上限限度額

        児童一覧の年齢 = 対象世帯.members("年齢", 対象期間)
        三歳未満の児童の人数 = 対象世帯.sum(児童一覧の年齢 < 3)
        三歳から小学校修了前の児童の人数 = 対象世帯.sum(児童一覧の年齢 < 13) - 三歳未満の児童の人数
        中学生の児童の人数 = 対象世帯.sum(児童一覧の年齢 < 16) - 三歳から小学校修了前の児童の人数 - 三歳未満の児童の人数

        手当条件 = 所得条件
        手当金額 = \
            np.sum(
                + (児童手当.金額.三歳未満 * 三歳未満の児童の人数)
                + (児童手当.金額.三歳から小学校修了前 * 三歳から小学校修了前の児童の人数)
                + (児童手当.金額.中学生 * 中学生の児童の人数),
                )
        return 手当条件 * 手当金額
