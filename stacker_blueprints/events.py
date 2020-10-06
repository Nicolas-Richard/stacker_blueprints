from stacker.blueprints.base import Blueprint

from troposphere import (
    NoValue,
    events
)


class EventBus(Blueprint):
    VARIABLES = {
        "EventSourceName": {
            "type": str,
            "description": "Optional name of the partner event source.",
            "default": "",

        },
        "EventBusName": {
            "type": str,
            "description": "The name of the event bus you are creating",
        }
    }

    def create_template(self):
        t = self.template

        eventbus = t.add_resource(
            events.EventBus(
                "EventBus",
                Name=self.event_bus_name,
                EventSourceName=self.event_source_name
            )
        )

        self.add_output("EventBusArn", eventbus.GetAtt("Arn"))
        self.add_output("EventBusName", eventbus.Ref())

    @property
    def event_bus_name(self):
        return self.get_variables()["EventBusName"]

    @property
    def event_source_name(self):
        return self.get_variables()["EventSourceName"] or NoValue


class Rule(Blueprint):

    VARIABLES = {
        "RuleDescription": {
            "type": str,
            "description": "Optional description of the rule.",
            "default": "",
        },
        "EventBusName": {
            "type": str,
            "description": "Optional, the event bus to associate with this rule. "
                           "If you omit this, the default event bus is used. ",
            "default": "default"
        },
        "EventPattern": {
            "type": dict,
            "description": "Describes which events are routed to the specified target",
        },
        "RuleName": {
            "type": str,
            "description": "The name of the rule.",
        },
        "RuleState": {
            "type": str,
            "description": "Indicates whether the rule is enabled. "
                           "Allowed values: DISABLED | ENABLED",
        },
        "Targets": {
            "type": list,
            "description": "The AWS resources that are invoked when the rule is triggered"
        }
    }

    @property
    def rule_description(self):
        return self.get_variables()["RuleDescription"] or NoValue

    @property
    def event_bus_name(self):
        return self.get_variables()["EventBusName"]

    @property
    def event_pattern(self):
        return self.get_variables()["EventPattern"]

    @property
    def rule_name(self):
        return self.get_variables()["RuleName"]

    @property
    def rule_state(self):
        return self.get_variables()["RuleState"]

    @property
    def targets(self):
        return [events.Target(Arn=t, Id="TriggeredPatternRuleTarget") for t in self.get_variables()["Targets"]]

    def create_template(self):
        t = self.template

        rule = t.add_resource(
            events.Rule(
                "TriggeredPatternRule",
                Description=self.rule_description,
                EventBusName=self.event_bus_name,
                EventPattern=self.event_pattern,
                Name=self.rule_name,
                State=self.rule_state,
                Targets=self.targets,
            )
        )

        self.add_output("RuleArn", rule.GetAtt("Arn"))

