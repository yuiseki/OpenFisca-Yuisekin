"""
This file defines variables for the modelled legislation.

A variable is a property of an Entity such as a 人物, a 世帯…

See https://openfisca.org/doc/key-concepts/variables.html
"""

import numpy as np
# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable
# Import the Entities specifically defined for this tax and benefit system
from openfisca_yuisekin.entities import 世帯, 人物


class ベーシックインカム(Variable):
    value_type = float
    entity = 人物
    definition_period = MONTH
    label = "人物のベーシックインカム"
    reference = "https://gov.ユイセキン共和国/ベーシックインカム"

    def formula_2016_12(対象人物, 対象期間, parameters):
        # This '*' is a vectorial 'if'.
        # See https://openfisca.org/doc/coding-the-legislation/25_vectorial_computing.html#control-structures
        return parameters(対象期間).福祉.ベーシックインカム

    def formula_2015_12(対象人物, 対象期間, parameters):
        年齢条件 = 対象人物("年齢", 対象期間) >= parameters(対象期間).全般.成人年齢
        所得条件 = 対象人物("所得", 対象期間) == 0
        return 年齢条件 * 所得条件 * parameters(対象期間).福祉.ベーシックインカム


class 住宅手当(Variable):
    value_type = float
    entity = 世帯
    definition_period = MONTH
    label = "世帯の住宅手当"
    # 2016年12月以降は廃止されたのでendは2016年11月30日
    # これ以降はずっと0を返す
    end = "2016-11-30"
    unit = "currency-EUR"
    documentation = """
    住宅手当制度の例。
    1980年に開始され、2016年12月に廃止された想定。
    """

    def formula_1980(対象世帯, 対象期間, parameters):
        return 対象世帯("家賃", 対象期間) * parameters(対象期間).福祉.住宅手当


class 年金(Variable):
    value_type = float
    entity = 人物
    definition_period = MONTH
    label = "人物の受け取る年金"

    def formula(対象人物, 対象期間, parameters):
        年齢条件 = 対象人物("年齢", 対象期間) >= parameters(対象期間).全般.定年年齢
        return 年齢条件


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
        児童手当 = parameters(対象期間).福祉.児童手当

        世帯高所得 = 対象世帯("世帯高所得", 対象期間)
        # TODO
        所得上限限度額 = 児童手当.所得上限限度額.扶養人数1人
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


class 世帯所得(Variable):
    value_type = float
    entity = 世帯
    definition_period = MONTH
    label = "世帯全員の収入の合計"

    def formula(対象世帯, 対象期間, _parameters):
        各収入 = 対象世帯.members("所得", 対象期間)
        return 対象世帯.sum(各収入)


class 世帯高所得(Variable):
    value_type = float
    entity = 世帯
    definition_period = MONTH
    label = "世帯で最も所得が高い人物の所得"

    def formula(対象世帯, 対象期間, _parameters):
        各収入 = 対象世帯.members("所得", 対象期間)
        return 対象世帯.max(各収入)
