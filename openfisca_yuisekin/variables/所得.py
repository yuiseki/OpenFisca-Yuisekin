"""
This file defines variables for the modelled legislation.

A variable is a property of an Entity such as a 人物, a 世帯…

See https://openfisca.org/doc/key-concepts/variables.html
"""

# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from openfisca_core.holders import set_input_divide_by_period
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable
# Import the Entities specifically defined for this tax and benefit system
from openfisca_yuisekin.entities import 人物


class 所得(Variable):
    value_type = float
    entity = 人物
    definition_period = MONTH
    # Optional attribute. Allows user to declare a 所得 for a year.
    # OpenFisca will spread the yearly 金額 over the months contained in the year.
    set_input = set_input_divide_by_period
    label = "人物の所得"


class 可処分所得(Variable):
    value_type = float
    entity = 人物
    definition_period = MONTH
    label = "所得のうち、人物が実際に使える額"

    def formula(対象人物, 対象期間, _parameters):
        return (
            + 対象人物("所得", 対象期間)
            + 対象人物("ベーシックインカム", 対象期間)
            - 対象人物("所得税", 対象期間)
            - 対象人物("社会保険料", 対象期間)
            )
