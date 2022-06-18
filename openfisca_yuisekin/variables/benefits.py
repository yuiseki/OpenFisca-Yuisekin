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
        return 年齢条件 * parameters(対象期間).benefits.ベーシックインカム

    def formula_2015_12(対象人物, 対象期間, parameters):
        年齢条件 = 対象人物("年齢", 対象期間) >= parameters(対象期間).全般.成人年齢
        所得条件 = 対象人物("所得", 対象期間) == 0
        # The '*' is also used as a vectorial 'and'. See https://openfisca.org/doc/coding-the-legislation/25_vectorial_computing.html#boolean-operations
        return 年齢条件 * 所得条件 * parameters(対象期間).benefits.ベーシックインカム


class housing_allowance(Variable):
    value_type = float
    entity = Household
    definition_period = MONTH
    label = "Housing allowance"
    reference = "https://law.gov.example/housing_allowance"  # Always use the most official source
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
        return household("rent", period) * parameters(period).benefits.housing_allowance


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
        年齢条件 = person("年齢", period) >= parameters(period).general.定年年齢
        return 年齢条件


class parenting_allowance(Variable):
    value_type = float
    entity = Household
    definition_period = MONTH
    label = "Allowance for low 所得 people with children to care for."
    documentation = "Loosely based on the Australian parenting pension."
    reference = "https://www.servicesaustralia.gov.au/individuals/services/centrelink/parenting-payment/who-can-get-it"

    def formula(household, period, parameters):
        """
        Parenting allowance for households.

        A person's parenting allowance depends on how many dependents they have,
        how much they, and their partner, earn
        if they are single with a child under 8
        or if they are partnered with a child under 6.
        """
        parenting_allowance = parameters(period).benefits.parenting_allowance

        世帯収入 = household("世帯収入", period)
        所得閾値 = parenting_allowance.所得閾値
        所得条件 = 世帯収入 <= 所得閾値

        is_single = household.nb_persons(Household.PARENT) == 1
        ages = household.members("年齢", period)
        under_8 = household.any(ages < 8)
        under_6 = household.any(ages < 6)

        allowance条件 = 所得条件 * ((is_single * under_8) + under_6)
        allowance_amount = parenting_allowance.amount

        return allowance条件 * allowance_amount


class 世帯収入(Variable):
    value_type = float
    entity = Household
    definition_period = MONTH
    label = "The sum of the salaries of those living in a household"

    def formula(household, period, _parameters):
        """A household's 所得."""
        salaries = household.members("所得", period)
        return household.sum(salaries)
