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
    label = "世帯への児童扶養手当"
    documentation = "実際のオーストラリアの制度を参考にしている"
    reference = "https://www.servicesaustralia.gov.au/individuals/services/centrelink/parenting-payment/who-can-get-it"

    def formula(対象世帯, 対象期間, parameters):
        児童扶養手当 = parameters(対象期間).福祉.児童扶養手当

        世帯所得 = 対象世帯("世帯所得", 対象期間)
        世帯所得上限 = 児童扶養手当.世帯所得上限
        所得条件 = 世帯所得 <= 世帯所得上限

        ひとり親である = 対象世帯.nb_persons(世帯.保護者) == 1
        児童一覧の年齢 = 対象世帯.members("年齢", 対象期間)
        八歳未満の児童がいる = 対象世帯.any(児童一覧の年齢 < 8)
        六歳未満の児童がいる = 対象世帯.any(児童一覧の年齢 < 6)

        手当条件 = 所得条件 * ((ひとり親である * 八歳未満の児童がいる) + 六歳未満の児童がいる)
        手当金額 = 児童扶養手当.金額

        return 手当条件 * 手当金額
