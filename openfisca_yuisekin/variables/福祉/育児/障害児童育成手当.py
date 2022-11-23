"""
障害児童育成手当の実装
"""

from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable
from openfisca_yuisekin.entities import 世帯
from openfisca_yuisekin.variables.障害.身体障害者手帳 import 身体障害者手帳等級認定パターン


class 障害児童育成手当(Variable):
    value_type = float
    entity = 世帯
    definition_period = MONTH
    label = "保護者への特別児童扶養手当"
    reference = "https://www.city.shibuya.tokyo.jp/kodomo/ninshin/teate/jido_i.html"
    documentation = """
    渋谷区の児童育成（障害）手当

    - 〒150-8010 東京都渋谷区宇田川町1-1
    - 渋谷区子ども青少年課子育て給付係
    - 03-3463-2558
    """

    def formula(対象世帯, 対象期間, parameters):
        障害児童育成手当 = parameters(対象期間).福祉.育児.障害児童育成手当
        扶養控除所得金額 = parameters(対象期間).税金.扶養控除所得金額

        # 世帯で最も高い所得の人が基準となる
        世帯高所得 = 対象世帯("世帯高所得", 対象期間)
        # 扶養人数が1人ではない場合を考慮する
        世帯所得一覧 = 対象世帯.members("所得", 対象期間)
        扶養人数 = 対象世帯.sum(世帯所得一覧 < 扶養控除所得金額)
        所得制限限度額 = 障害児童育成手当.所得制限限度額.calc(扶養人数)
        所得条件 = 世帯高所得 <= 所得制限限度額

        身体障害者手帳等級一覧 = 対象世帯.members("身体障害者手帳等級", 対象期間)
        児童一覧の年齢 = 対象世帯.members("年齢", 対象期間)

        身体障害者手帳一級または二級 = \
            (身体障害者手帳等級一覧 == 身体障害者手帳等級認定パターン.一級) | (身体障害者手帳等級一覧 == 身体障害者手帳等級認定パターン.二級)
        上限年齢以下の児童 = 児童一覧の年齢 < 障害児童育成手当.上限年齢
        # 対象となる身体障害者手帳等級は1・2級程度
        上限年齢以下の身体障害を持つ児童人数 = 対象世帯.sum(上限年齢以下の児童 & 身体障害者手帳一級または二級)
        手当金額 = (障害児童育成手当.金額 * 上限年齢以下の身体障害を持つ児童人数)

        return 所得条件 * 手当金額
