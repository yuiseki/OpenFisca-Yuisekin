"""
特別児童育成手当の実装
"""

from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable
from openfisca_yuisekin.entities import 世帯
from openfisca_yuisekin.variables.障害.身体障害者手帳 import 身体障害者手帳等級認定パターン


class 特別児童扶養手当(Variable):
    value_type = float
    entity = 世帯
    definition_period = MONTH
    label = "保護者への特別児童扶養手当"
    reference = "https://www.city.shibuya.tokyo.jp/kodomo/teate/hitorioya/hitorioya_teate.html"
    documentation = """
    渋谷区の特別児童扶養手当制度

    - 〒150-8010 東京都渋谷区宇田川町1-1
    - 渋谷区子ども青少年課子育て給付係
    - 03-3463-2558
    """

    def formula(対象世帯, 対象期間, parameters):
        特別児童扶養手当 = parameters(対象期間).福祉.育児.特別児童扶養手当

        世帯所得 = 対象世帯("世帯所得", 対象期間)
        # TODO 児童扶養手当受給者である場合にも対応する
        # TODO 扶養人数1人以外にも対応する
        世帯所得上限 = 特別児童扶養手当.所得制限限度額.扶養義務者.扶養人数1人
        所得条件 = 世帯所得 <= 世帯所得上限
        上限年齢 = 特別児童扶養手当.上限年齢

        身体障害者手帳等級一覧 = 対象世帯.members("身体障害者手帳等級", 対象期間)
        身体障害者がいる = 対象世帯.any(身体障害者手帳等級一覧 != 身体障害者手帳等級認定パターン.無)
        児童一覧の年齢 = 対象世帯.members("年齢", 対象期間)
        上限年齢以下の児童がいる = 対象世帯.any(児童一覧の年齢 < 上限年齢)

        手当条件 = 所得条件 * 上限年齢以下の児童がいる * 身体障害者がいる
        # TODO 身体障害者の児童の人数と等級に応じて手当金額を変える
        手当金額 = 特別児童扶養手当.金額.一級

        return 手当条件 * 手当金額
