"""
児童扶養手当の実装
"""

from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable
from openfisca_yuisekin.entities import 世帯


class 児童扶養手当(Variable):
    value_type = float
    entity = 世帯
    definition_period = MONTH
    label = "保護者への児童扶養手当"
    reference = "https://www.city.shibuya.tokyo.jp/kodomo/teate/hitorioya/hitorioya_teate.html"
    documentation = """
    渋谷区の児童扶養手当制度

    - 〒150-8010 東京都渋谷区宇田川町1-1
    - 渋谷区子ども青少年課子育て給付係
    - 03-3463-2558
    """

    def formula(対象世帯, 対象期間, parameters):
        児童扶養手当 = parameters(対象期間).福祉.育児.児童扶養手当

        世帯所得 = 対象世帯("世帯所得", 対象期間)
        世帯所得上限 = 児童扶養手当.所得制限限度額.全部支給.扶養人数1人
        所得条件 = 世帯所得 <= 世帯所得上限
        上限年齢 = 児童扶養手当.上限年齢

        ひとり親である = 対象世帯.nb_persons(世帯.保護者) == 1
        児童一覧の年齢 = 対象世帯.members("年齢", 対象期間)
        上限年齢以下の児童がいる = 対象世帯.any(児童一覧の年齢 < 上限年齢)

        手当条件 = 所得条件 * ひとり親である * 上限年齢以下の児童がいる
        手当金額 = 児童扶養手当.金額.全部支給.児童1人
        print(手当金額)

        return 手当条件 * 手当金額
