"""
This file defines variables for the modelled legislation.

A variable is a property of an Entity such as a 人物, a 世帯…

See https://openfisca.org/doc/key-concepts/variables.html
"""

from datetime import date

# Import from numpy the operations you need to apply on OpenFisca's population vectors
# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from numpy import where
from openfisca_core.periods import ETERNITY, MONTH, DAY
from openfisca_core.variables import Variable

# Import the Entities specifically defined for this tax and benefit system
from openfisca_yuisekin.entities import 人物


# This variable is a pure input: it doesn't have a formula
class 誕生年月日(Variable):
    value_type = date
    default_value = date(1970, 1, 1)  # By default, if no value is set for a simulation, we consider the people involved in a simulation to be born on the 1st of Jan 1970.
    entity = 人物
    label = "人物の誕生年月日"
    definition_period = ETERNITY  # This variable cannot change over time.
    reference = "https://en.wiktionary.org/wiki/birthdate"


class 年齢(Variable):
    value_type = int
    entity = 人物
    definition_period = MONTH
    label = "人物の年齢"

    def formula(対象人物, 対象期間, _parameters):
        誕生年月日 = 対象人物("誕生年月日", 対象期間)
        誕生年 = 誕生年月日.astype("datetime64[Y]").astype(int) + 1970
        誕生月 = 誕生年月日.astype("datetime64[M]").astype(int) % 12 + 1
        誕生日 = (誕生年月日 - 誕生年月日.astype("datetime64[M]") + 1).astype(int)

        誕生日を過ぎている = (誕生月 < 対象期間.start.month) + (誕生月 == 対象期間.start.month) * (誕生日 <= 対象期間.start.day)

        return (対象期間.start.year - 誕生年) - where(誕生日を過ぎている, 0, 1)  # If the birthday is not passed this year, subtract one year


class 学年(Variable):
    value_type = int
    entity = 人物
    definition_period = DAY
    label = "人物の学年"

    def formula(対象人物, 対象期間, _parameters):
        誕生年月日 = 対象人物("誕生年月日", 対象期間)
        誕生年 = 誕生年月日.astype("datetime64[Y]").astype(int) + 1970
        誕生月 = 誕生年月日.astype("datetime64[M]").astype(int) % 12 + 1
        # 誕生日 = (誕生年月日 - 誕生年月日.astype("datetime64[M]") + 1).astype(int)

        対象期間において早生まれ = (誕生月 < 4) *  (4 <= 対象期間.start.month)
        早生まれではないが四月以降 = (4 < 誕生月) * (4 <= 対象期間.start.month)
        学年を繰り上げるべき = 対象期間において早生まれ + 早生まれではないが四月以降

        print(学年を繰り上げるべき)

        return (対象期間.start.year - 誕生年) + where(学年を繰り上げるべき, 1, 0)
