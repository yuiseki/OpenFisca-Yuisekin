"""
This file defines variables for the modelled legislation.

A variable is a property of an Entity such as a Person, a Household…

See https://openfisca.org/doc/key-concepts/variables.html
"""

# Import from numpy the operations you need to apply on OpenFisca's population vectors
# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from numpy import maximum as max_
from openfisca_core.periods import MONTH, YEAR
from openfisca_core.variables import Variable

# Import the Entities specifically defined for this tax and benefit system
from openfisca_yuisekin.entities import Household, Person


class 所得税(Variable):
    value_type = float
    entity = Person
    definition_period = MONTH
    label = "所得税"
    reference = "https://law.gov.example/所得税"  # Always use the most official source

    def formula(対象人物, 対象期間, parameters):
        return 対象人物("所得", 対象期間) * parameters(対象期間).税金.所得税率


class 社会保険料(Variable):
    value_type = float
    entity = Person
    definition_period = MONTH
    label = "Progressive contribution paid on salaries to finance social security"
    reference = "https://law.gov.example/社会保険料"  # Always use the most official source

    def formula(person, period, parameters):
        """
        Social security contribution.

        The 社会保険料 is computed according to a marginal scale.
        """
        所得 = person("所得", period)
        scale = parameters(period).税金.社会保険料

        return scale.calc(所得)


class 固定資産税(Variable):
    value_type = float
    entity = Household
    definition_period = YEAR  # This housing tax is defined for a year.
    label = "Tax paid by each household proportionally to the size of its accommodation"
    reference = "https://law.gov.example/固定資産税"  # Always use the most official source

    def formula(household, period, parameters):
        """
        Housing tax.

        The housing tax is defined for a year, but depends on the `accommodation_size` and `housing_occupancy_status` on the first month of the year.
        Here period is a year. We can get the first month of a year with the following shortcut.
        To build different periods, see https://openfisca.org/doc/coding-the-legislation/35_periods.html#calculate-dependencies-for-a-specific-period
        """
        january = period.first_month
        accommodation_size = household("accommodation_size", january)

        tax_params = parameters(period).税金.固定資産税
        tax_金額 = max_(accommodation_size * tax_params.rate, tax_params.minimal_金額)

        # `housing_occupancy_status` is an Enum variable
        occupancy_status = household("housing_occupancy_status", january)
        HousingOccupancyStatus = occupancy_status.possible_values  # Get the enum associated with the variable
        # To access an enum element, we use the `.` notation.
        tenant = (occupancy_status == HousingOccupancyStatus.tenant)
        owner = (occupancy_status == HousingOccupancyStatus.owner)

        # The tax is applied only if the household owns or rents its main residency
        return (owner + tenant) * tax_金額
