"""
This file defines variables for the modelled legislation.

A variable is a property of an Entity such as a Person, a Household…

See https://openfisca.org/doc/key-concepts/variables.html
"""

# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

# Import the Entities specifically defined for this tax and benefit system
from openfisca_yuisekin.entities import Household, Person


class ベーシックインカム(Variable):
    value_type = float
    entity = Person
    definition_period = MONTH
    label = "ベーシックインカム"
    reference = "https://gov.ユイセキン共和国/ベーシックインカム"

    def formula_2016_12(対象人物, 対象期間, parameters):
        年齢条件 = 対象人物("年齢", 対象期間) >= parameters(対象期間).全般.成人年齢
        # This '*' is a vectorial 'if'. See https://openfisca.org/doc/coding-the-legislation/25_vectorial_computing.html#control-structures
        return 年齢条件 * parameters(対象期間).福祉.ベーシックインカム

    def formula_2015_12(対象人物, 対象期間, parameters):
        年齢条件 = 対象人物("年齢", 対象期間) >= parameters(対象期間).全般.成人年齢
        所得条件 = 対象人物("所得", 対象期間) == 0
        # The '*' is also used as a vectorial 'and'. See https://openfisca.org/doc/coding-the-legislation/25_vectorial_computing.html#boolean-operations
        return 年齢条件 * 所得条件 * parameters(対象期間).福祉.ベーシックインカム


class 住宅手当(Variable):
    value_type = float
    entity = Household
    definition_period = MONTH
    label = "Housing allowance"
    reference = "https://law.gov.example/住宅手当"  # Always use the most official source
    end = "2016-11-30"  # This allowance was removed on the 1st of Dec 2016. Calculating it before this date will always return the variable default value, 0.
    unit = "currency-EUR"
    documentation = """
    This allowance was introduced on the 1st of Jan 1980.
    It disappeared in Dec 2016.
    """

    def formula_1980(household, period, parameters):
        """
        Housing allowance.

        This allowance was introduced on the 1st of Jan 1980.
        Calculating it before this date will always return the variable default value, 0.

        To compute this allowance, the 'rent' value must be provided for the same month,
        but 'housing_occupancy_status' is not necessary.
        """
        return household("rent", period) * parameters(period).福祉.住宅手当


# By default, you can use utf-8 characters in a variable. OpenFisca web API manages utf-8 encoding.
class pension(Variable):
    value_type = float
    entity = Person
    definition_period = MONTH
    label = "Pension for the elderly. Pension attribuée aux personnes âgées. تقاعد."
    reference = ["https://fr.wikipedia.org/wiki/Retraite_(économie)", "https://ar.wikipedia.org/wiki/تقاعد"]

    def formula(person, period, parameters):
        """
        Pension for the elderly.

        A person's pension depends on their birth date.
        In French: retraite selon l'âge.
        In Arabic: تقاعد.
        """
        年齢条件 = person("年齢", period) >= parameters(period).全般.定年年齢
        return 年齢条件


class 児童手当(Variable):
    value_type = float
    entity = Household
    definition_period = MONTH
    label = "低所得世帯への児童手当"
    documentation = "実際のオーストラリアの制度を参考にしている"
    reference = "https://www.servicesaustralia.gov.au/individuals/services/centrelink/parenting-payment/who-can-get-it"

    def formula(対象世帯, 対象期間, parameters):
        児童手当 = parameters(対象期間).福祉.児童手当

        世帯収入 = 対象世帯("世帯収入", 対象期間)
        所得閾値 = 児童手当.所得閾値
        所得条件 = 世帯収入 <= 所得閾値

        ひとり親 = 対象世帯.nb_persons(Household.PARENT) == 1
        子どもたちの年齢 = 対象世帯.members("年齢", 対象期間)
        八歳未満の子どもがいる = 対象世帯.any(子どもたちの年齢 < 8)
        六歳未満の子どもがいる = 対象世帯.any(子どもたちの年齢 < 6)

        手当条件 = 所得条件 * ((ひとり親 * 八歳未満の子どもがいる) + 六歳未満の子どもがいる)
        手当金額 = 児童手当.金額

        return 手当条件 * 手当金額


class 世帯収入(Variable):
    value_type = float
    entity = Household
    definition_period = MONTH
    label = "The sum of the salaries of those living in a household"

    def formula(household, period, _parameters):
        """A household's 所得."""
        salaries = household.members("所得", period)
        return household.sum(salaries)
