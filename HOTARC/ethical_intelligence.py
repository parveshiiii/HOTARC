import logging

class EthicalIntelligence:
    def __init__(self):
        self.ethics_rules = []
        logging.basicConfig(filename='ethical_intelligence.log', level=logging.INFO)

    def apply_ethics(self, decision_context):
        return self._apply_ethics_rules(decision_context)

    def update_ethics(self, feedback):
        self._update_ethics_rules(feedback)

    def _apply_ethics_rules(self, decision_context):
        decision_ethical_score = 0
        total_weight = 0
        for rule in self.ethics_rules:
            if 'condition' in rule and 'action' in rule and 'weight' in rule:
                try:
                    condition_result = eval(rule['condition'], {}, decision_context)
                    if condition_result:
                        action_result = eval(rule['action'], {}, decision_context)
                        decision_ethical_score += action_result * rule['weight']
                        total_weight += rule['weight']
                except Exception as e:
                    logging.error(f"Error applying rule {rule}: {e}")
        if total_weight > 0:
            decision_ethical_score /= total_weight
        return decision_ethical_score >= 0

    def _update_ethics_rules(self, feedback):
        new_rules = feedback.get('new_rules', [])
        validated_rules = self._validate_rules(new_rules)
        for rule in validated_rules:
            if not self._is_conflicting(rule):
                self.ethics_rules.append(rule)
                logging.info(f"Added new ethical rule: {rule}")
            else:
                self._merge_rules(rule)

    def _validate_rules(self, new_rules):
        validated_rules = []
        for rule in new_rules:
            if 'condition' in rule and 'action' in rule and 'weight' in rule:
                try:
                    compile(rule['condition'], '<string>', 'eval')
                    compile(rule['action'], '<string>', 'eval')
                    validated_rules.append(rule)
                except Exception as e:
                    logging.error(f"Invalid rule {rule}: {e}")
        return validated_rules

    def _is_conflicting(self, new_rule):
        for rule in self.ethics_rules:
            if rule['condition'] == new_rule['condition'] and rule['action'] != new_rule['action']:
                return True
        return False

    def _merge_rules(self, new_rule):
        for rule in self.ethics_rules:
            if rule['condition'] == new_rule['condition']:
                rule['action'] = f"({rule['action']}) + ({new_rule['action']})"
                rule['weight'] = (rule['weight'] + new_rule['weight']) / 2
                logging.info(f"Merged rule {new_rule} into existing rule.")
                return