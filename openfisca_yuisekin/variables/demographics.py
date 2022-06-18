"""
This file defines variables for the modelled legislation.

A variable is a property of an Entity such as a 人物, a 世帯…

See https://openfisca.org/doc/key-concepts/variables.html
"""

from datetime import date

# Import from numpy the operations you need to apply on OpenFisca's population vectors
# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from numpy import where
from openfisca_core.periods import ETERNITY, MONTH
from openfisca_core.variables import Variable

# Import the Entities specifically defined for this tax and benefit system
from openfisca_yuisekin.entities import 人物


# This variable is a pure input: it doesn't have a formula
class birth(Variable):
    value_type = date
    default_value = date(1970, 1, 1)  # By default, if no value is set for a simulation, we consider the people involved in a simulation to be born on the 1st of Jan 1970.
    entity = 人物
    label = "Birth date"
    definition_period = ETERNITY  # This variable cannot change over time.
    reference = "https://en.wiktionary.org/wiki/birthdate"


class 年齢(Variable):
    value_type = int
    entity = 人物
    definition_period = MONTH
    label = "人物's age (in years)"

    def formula(対象人物, 対象期間, _parameters):
        誕生年月日 = 対象人物("birth", 対象期間)
        誕生年 = 誕生年月日.astype("datetime64[Y]").astype(int) + 1970
        誕生月 = 誕生年月日.astype("datetime64[M]").astype(int) % 12 + 1
        誕生日 = (誕生年月日 - 誕生年月日.astype("datetime64[M]") + 1).astype(int)

        is_birthday_past = (誕生月 < 対象期間.start.month) + (誕生月 == 対象期間.start.month) * (誕生日 <= 対象期間.start.day)

        return (対象期間.start.year - 誕生年) - where(is_birthday_past, 0, 1)  # If the birthday is not passed this year, subtract one year
