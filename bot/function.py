# Imports
import lichesspy.api
import requests

# The function checks all players of a team and returns a list of all cheaters.


def analyse_team(teamname: str, ignore_user: list) -> list:
    cheaters = []
    # The wrapper classes are used, because the PyPi functions have a wrong scope.
    # Please note the commit time.
    users = lichesspy.api.users_by_team(teamname)
    for i in users:
        if i.get("tosViolation") or i.get("closed"):
            username = i.get("username")
            if username not in ignore_user:
                cheaters.append(username)
    return cheaters


# The function kicks the specified player from the team.
# The bot token is required for this.
def kick(team: str, user: str, token: str) -> requests.Response:
    user = user.lower()
    # The token is the one from the bot account.
    # The bot must also be a team leader to be able to kick people.
    url = "https://lichess.org/team/" + team + "/kick/" + user
    header = {"Authorization": "Bearer " + token}
    # The Lichess API accepts the request as a POST request.
    # Therefore all data must be in the header.
    return requests.post(url, headers=header)


# Unfortunately, the API returns only an array.
# This is checked here.
def check(level: str) -> bool:
    """check"""
    # Since it is a request response, it cannot be interpreted as a string.
    return bool("true" in level.text)


# The function investigates why a request failed.
def status(level: requests.Response) -> str:
    """get status"""
    if "true" not in level.text:
        # The Lichess API actually works very well.
        # Therefore either the token is wrong or the error is about one meter behind the screen.
        if "No such token" in level.text:
            return "Invalid Token! (Wrong Token or not authorized)"
        if "Not your team" in level.text:
            return "Invalid Token! (Not your Team)"
        return "Undefined Error!"
    return "No Error"


# If anyone operates the bot incorrectly, it will be checked again for errors here.
def check_team_name(team: str) -> bool:
    # The program uses the static links from lichess
    if "/team/" in team:
        runner = len(team)
        while runner > 0:
            # Lichess cannot process teams with the "/" character for syntax reasons.
            # Therefore there are no such teams.
            if "/" in team[-runner::]:
                runner -= 1
            else:
                return team[-runner::]
    return team