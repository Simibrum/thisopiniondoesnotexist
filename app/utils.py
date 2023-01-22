"""Miscellaneous utility functions."""

import os
import re
from typing import Tuple
from dateutil import parser
from dateutil import tz
from datetime import datetime

# List of premier league teams - filter these out of the trends!
premier_league_teams = [
    "Arsenal", "Aston Villa", "Brighton", "Burnley", "Chelsea", "Crystal Palace", "Everton",
    "Leeds United", "Leicester City", "Liverpool", "Manchester City", "Manchester United", "Man City",
    "Man United", "Man", "Newcastle United",
    "Norwich City", "Southampton", "Tottenham Hotspur", "Watford", "West Ham", "Wolves", "Rangers", "Celtic",
    "PSG", "Barcelona", "Real Madrid", "Bayern Munich", "Bayern", "Juventus", "AC Milan", "Inter Milan", "Lazio",
    "Leipzig", "Premier League", "Bundesliga", "Liga", "Serie", "Ligue", "Champions League", "Europa League",
]


def load_env_vars(path):
    """Load environment variables from a file."""
    with open(path) as f:
        for line in f:
            if "=" in line:
                # Split the line into the variable name and value
                var, value = line.split("=")

                # Strip leading and trailing whitespace from the variable name and value
                var = var.strip()
                value = value.strip()

                if var and value:
                    # Set the environment variable
                    os.environ[var] = value


def get_date_components(date_string: str) -> (int, int, int):
    """Get the year, month and day from a date string."""
    date_object = parser.parse(date_string)
    return date_object.day, date_object.month, date_object.year


def get_heading(string: str) -> str:
    """Get the heading from a string using regex."""
    regex = r"(?<=Title:).*(?=\n|\r)"
    match = re.search(regex, string, re.MULTILINE)
    if match:
        return match.group(0).strip()
    else:
        return ""


def get_alt_text(string: str) -> Tuple[str, str]:
    """Get the lead and body alt text from a string using regex."""
    regex = r"(?<=image \[alt text\]:).*(?=\n|\r|$)"
    matches = re.findall(regex, string, re.MULTILINE)
    if matches:
        # Return the first and second matches as a tuple
        try:
            return matches[0].strip(), matches[1].strip()
        except IndexError:
            return "", ""
    else:
        return "", ""


def get_current_date() -> str:
    """Get the current date in a string format."""
    now = datetime.now(tz.tzlocal())
    formatted_date = now.strftime("%-d %B %Y")
    return formatted_date


def count_paragraphs_in_plan(plan: str) -> int:
    """Count the number of paragraphs in a plan."""
    regex = r"[pP]aragraph \d"
    matches = re.findall(regex, plan)
    return len(matches)


def filter_out_football(topics: list) -> list:
    """Filter out football topics."""
    filtered_topics = []
    single_word_football_teams = {w for team in premier_league_teams for w in team.split(" ")}
    for topic in topics:
        versus = topic.split(" vs ")
        if len(versus) == 2:
            if versus[0] in premier_league_teams and versus[1] in premier_league_teams:
                continue
        words = {w for w in topic.split(" ")}
        # If intersection of words and football teams is empty, add to filtered topics
        if not words.intersection(single_word_football_teams):
            filtered_topics.append(topic)
    return filtered_topics
