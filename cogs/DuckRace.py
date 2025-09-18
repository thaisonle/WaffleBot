import re

class DuckRace:
    def __init__(self, bot):
        self.bot = bot

    def __toString(self):
        return self.id if self.id else ''

    def setupSpots(self, numberOfSpots):
        self._spots = []
        for i in range(numberOfSpots):
            self._spots.append(i)

    @property
    def ducks(self):
        return self._ducks

    @ducks.setter
    def ducks(self, value):
        self._ducks = re.sub('[^0-9]', '', value)

    @property
    def bucks(self):
        return self._bucks

    @bucks.setter
    def bucks(self, value):
        self._bucks = re.sub('[^0-9]', '', value)

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        if "@" in value:
            self._user = value
        else:
            self._user = '@' . value

    @property
    def venmo(self):
        return self._venmo

    @venmo.setter
    def venmo(self, value):
        if "@" in value:
            self._venmo = value
        else:
            self._venmo = '@' . value

    @property
    def last4(self):
        return self._last4

    @last4.setter
    def last4(self, value):
        self._last4 = re.sub('[^0-9]', '', value)
