"""
特別児童育成手当の実装
"""

import numpy as np
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable
from openfisca_yuisekin.entities import 世帯
from openfisca_yuisekin.variables.障害.身体障害者手帳 import 身体障害者手帳等級認定パターン


class 特別児童扶養手当(Variable):
    value_type = float
    entity = 世帯
    definition_period = MONTH
    label = "保護者への特別児童扶養手当"
    reference = "https://www.city.shibuya.tokyo.jp/kodomo/teate/teate/jido_f.html"
    documentation = """
    渋谷区の特別児童扶養手当制度

    - 〒150-8010 東京都渋谷区宇田川町1-1
    - 渋谷区子ども青少年課子育て給付係
    - 03-3463-2558
    """

    def formula(対象世帯, 対象期間, parameters):
        特別児童扶養手当 = parameters(対象期間).福祉.育児.特別児童扶養手当
        扶養控除所得金額 = parameters(対象期間).税金.扶養控除所得金額

        # 世帯で最も高い所得の人が基準となる
        世帯高所得 = 対象世帯("世帯高所得", 対象期間)

        # 世帯の扶養人数を考慮する必要がある
        世帯所得一覧 = 対象世帯.members("所得", 対象期間)
        扶養人数 = 対象世帯.sum(世帯所得一覧 < 扶養控除所得金額)

        # 児童扶養手当受給者の場合とそうでない場合に対応する
        児童扶養手当 = 対象世帯("児童扶養手当", 対象期間)
        所得制限限度額 = np.select(
            [児童扶養手当 <= 0, 0 < 児童扶養手当],
            [
                特別児童扶養手当.所得制限限度額.児童扶養手当受給者.calc(扶養人数),
                特別児童扶養手当.所得制限限度額.扶養義務者.calc(扶養人数),
            ],
            )
        所得条件 = 世帯高所得 <= 所得制限限度額

        身体障害者手帳等級一覧 = 対象世帯.members("身体障害者手帳等級", 対象期間)
        身体障害者がいる = 対象世帯.any(身体障害者手帳等級一覧 != 身体障害者手帳等級認定パターン.無)
        児童一覧の年齢 = 対象世帯.members("年齢", 対象期間)
        上限年齢以下の児童がいる = 対象世帯.any(児童一覧の年齢 < 特別児童扶養手当.上限年齢)

        手当条件 = 所得条件 * 上限年齢以下の児童がいる * 身体障害者がいる
        # TODO 身体障害者の児童の人数と等級に応じて手当金額を変える
        手当金額 = 特別児童扶養手当.金額.一級

        return 手当条件 * 手当金額
