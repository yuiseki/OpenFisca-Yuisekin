"""
身体障害者手帳の定義
"""

from datetime import date
from datetime import datetime

from dateutil.relativedelta import relativedelta
from openfisca_core.indexed_enums import Enum
from openfisca_core.periods import DAY, ETERNITY
from openfisca_core.variables import Variable
from openfisca_yuisekin.entities import 人物


class 身体障害者手帳最新交付年月日(Variable):
    value_type = date
    entity = 人物
    label = "人物の身体障害者手帳の最新交付年月日"
    definition_period = ETERNITY


class 身体障害者手帳等級認定パターン(Enum):
    __order__ = "無 一級 二級 三級"
    無 = "無"
    一級 = "一級"
    二級 = "二級"
    三級 = "三級"


class 身体障害者手帳最新等級認定(Variable):
    value_type = Enum
    possible_values = 身体障害者手帳等級認定パターン
    default_value = 身体障害者手帳等級認定パターン.無
    entity = 人物
    definition_period = ETERNITY
    label = "人物の身体障害者手帳等級認定"


class 身体障害者手帳等級(Variable):
    value_type = Enum
    possible_values = 身体障害者手帳等級認定パターン
    default_value = 身体障害者手帳等級認定パターン.無
    entity = 人物
    definition_period = DAY
    label = "人物の身体障害者手帳等級"

    def formula(対象人物, 対象期間, _parameters):
        最新交付年月日 = 対象人物("身体障害者手帳最新交付年月日", 対象期間)
        交付年月日 = 最新交付年月日.astype("datetime64[D]").astype(datetime)[0]
        有効年月日 = 交付年月日 + relativedelta(years=2)
        身体障害者手帳が有効 = (交付年月日 <= 対象期間.date) * (対象期間.date <= 有効年月日)
        身体障害者手帳最新等級認定 = 対象人物("身体障害者手帳最新等級認定", 対象期間)[0]
        return (身体障害者手帳最新等級認定 * 身体障害者手帳が有効)
