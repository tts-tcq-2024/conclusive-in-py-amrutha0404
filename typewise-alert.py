class CoolingStrategy:
    def get_limits(self):
        pass

class PassiveCooling(CoolingStrategy):
    def get_limits(self):
        return 0, 35

class HiActiveCooling(CoolingStrategy):
    def get_limits(self):
        return 0, 45

class MedActiveCooling(CoolingStrategy):
    def get_limits(self):
        return 0, 40

class AlertStrategy:
    def send_alert(self, breachType):
        pass

class ControllerAlert(AlertStrategy):
    def send_alert(self, breachType):
        header = 0xfeed
        print(f'{header}, {breachType}')

class EmailAlert(AlertStrategy):
    def send_alert(self, breachType):
        recepient = "a.b@c.com"
        message = "low" if breachType == 'TOO_LOW' else "high"
        print(f'To: {recepient}\nHi, the temperature is too {message}')

def infer_breach(value, lowerLimit, upperLimit):
    if value < lowerLimit:
        return 'TOO_LOW'
    if value > upperLimit:
        return 'TOO_HIGH'
    return 'NORMAL'

def classify_temperature_breach(coolingStrategy, temperatureInC):
    lowerLimit, upperLimit = coolingStrategy.get_limits()
    return infer_breach(temperatureInC, lowerLimit, upperLimit)

def check_and_alert(alertStrategy, coolingStrategy, temperatureInC):
    breachType = classify_temperature_breach(coolingStrategy, temperatureInC)
    alertStrategy.send_alert(breachType)

# Factory functions
def cooling_strategy_factory(coolingType):
    strategies = {
        'PASSIVE_COOLING': PassiveCooling(),
        'HI_ACTIVE_COOLING': HiActiveCooling(),
        'MED_ACTIVE_COOLING': MedActiveCooling(),
    }
    return strategies.get(coolingType, PassiveCooling())

def alert_strategy_factory(alertTarget):
    strategies = {
        'TO_CONTROLLER': ControllerAlert(),
        'TO_EMAIL': EmailAlert(),
    }
    return strategies.get(alertTarget, ControllerAlert())

# Example usage
batteryChar = {'coolingType': 'PASSIVE_COOLING'}
coolingStrategy = cooling_strategy_factory(batteryChar['coolingType'])
alertStrategy = alert_strategy_factory('TO_EMAIL')
check_and_alert(alertStrategy, coolingStrategy, 125)
