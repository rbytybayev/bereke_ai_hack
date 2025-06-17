from app.models.schema import ContractData
from typing import List, Dict
import re

# Заглушки: при необходимости заменить на загрузку из базы/файла
SANCTIONED_ENTITIES = ["ООО Восток", "Vostok Ltd", "Иван Иванов"]
SANCTIONED_TNVED_GROUPS = ["8401", "8542", "8803"]


def check_sanctions(contract: ContractData) -> Dict:
    partner_name = contract.foreign_partner.name.lower() if contract.foreign_partner else ""
    for entity in SANCTIONED_ENTITIES:
        if entity.lower() in partner_name:
            return {
                "name": "Санкции по контрагенту",
                "status": "fail",
                "reason": f"Контрагент найден в санкционном списке: {entity}"
            }
    return {"name": "Санкции по контрагенту", "status": "pass"}


def check_tnved(contract: ContractData) -> Dict:
    code = contract.tnved_code or ""
    if not code:
        return {"name": "Код ТНВЭД", "status": "unknown", "reason": "Не указан в договоре"}

    for prefix in SANCTIONED_TNVED_GROUPS:
        if code.startswith(prefix):
            return {
                "name": "Код ТНВЭД",
                "status": "fail",
                "reason": f"Код {code} попадает под санкционную группу {prefix}"
            }
    return {"name": "Код ТНВЭД", "status": "pass"}


def check_currency_rules(contract: ContractData) -> Dict:
    # Пример: нельзя валютные сделки между резидентами
    if contract.foreign_partner and contract.foreign_partner.country in ["Казахстан", "Kazakhstan"]:
        return {
            "name": "Валютное законодательство",
            "status": "fail",
            "reason": "Обе стороны договора являются резидентами РК"
        }

    # Можно расширить по логике типов сделок, сроков и валют
    return {"name": "Валютное законодательство", "status": "pass"}


def run_checks(contract: ContractData) -> List[Dict]:
    return [
        check_sanctions(contract),
        check_tnved(contract),
        check_currency_rules(contract)
    ]