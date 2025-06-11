from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Literal

import matplotlib.axes as axes
import matplotlib.pyplot as plt

NameType = Literal[
    "Agrim",
    "Munira",
    "Tobi",
    "Alina",
    "Tobias Bl.",
    "Wissal",
    "Maxi",
    "Georgios",
]
FactionType = Literal[
    "Cats",
    "Birds",
    "Vagabond",
    "Woodland",
    "Crows",
    "Duchy",
    "Riverfolk",
    "Lizards",
]


@dataclass
class Player:
    """
    Represents a player in a game of Root.

    Attributes:
        name (NameType): The player's name.
        faction (FactionType): The faction the player played.
        is_winner (bool): Whether the player won the game.
    """

    name: NameType
    faction: FactionType
    is_winner: bool = False


@dataclass
class Game:
    """
    Represents a single game of Root.

    Attributes:
        game_date (date): The date the game was played.
        players (list[Player]): The list of players in the game.
    """

    game_date: date
    players: list[Player]

    @property
    def names(self) -> list[NameType]:
        """Returns a list of player names in the game."""
        return [player.name for player in self.players]

    @property
    def factions(self) -> list[FactionType]:
        """Returns a list of factions played in the game."""
        return [player.faction for player in self.players]

    @property
    def winner(self) -> Player:
        """Returns the winning player of the game."""
        return next(player for player in self.players if player.is_winner)

    @property
    def looser(self) -> list[Player]:
        """Returns a list of players who did not win the game."""
        return [player for player in self.players if not player.is_winner]

    @property
    def winner_name(self) -> NameType:
        """Returns the name of the winning player."""
        return self.winner.name

    @property
    def looser_name(self) -> list[NameType]:
        """Returns a list of names of players who did not win."""
        return [player.name for player in self.looser]

    @property
    def winner_faction(self) -> FactionType:
        """Returns the faction of the winning player."""
        return self.winner.faction

    @property
    def looser_faction(self) -> list[FactionType]:
        """Returns a list of factions played by non-winning players."""
        return [player.faction for player in self.looser]


def get_names(games: list[Game]) -> list[NameType]:
    """
    Returns a list of unique player names from a list of games.

    Args:
        games (list[Game]): List of games.

    Returns:
        list[NameType]: Unique player names.
    """
    return list({player.name for game in games for player in game.players})


def get_factions(games: list[Game]) -> list[FactionType]:
    """
    Returns a list of unique factions played in a list of games.

    Args:
        games (list[Game]): List of games.

    Returns:
        list[FactionType]: Unique factions.
    """
    return list({player.faction for game in games for player in game.players})


def get_num_wins(games: list[Game], name: NameType) -> int:
    """
    Returns the number of games won by a player.

    Args:
        games (list[Game]): List of games.
        name (NameType): Player name.

    Returns:
        int: Number of wins.
    """
    return sum(1 for game in games if game.winner_name == name)


def get_name_game_count_dict(games: list[Game]) -> dict[NameType, int]:
    """
    Returns a dictionary mapping player names to the number of games they played.

    Args:
        games (list[Game]): List of games.

    Returns:
        dict[NameType, int]: Player name to game count.
    """
    return {
        name: sum(1 for game in games if name in game.names)
        for name in get_names(games)
    }


def get_faction_game_count_dict(games: list[Game]) -> dict[FactionType, int]:
    """
    Returns a dictionary mapping factions to the number of games they were played in.

    Args:
        games (list[Game]): List of games.

    Returns:
        dict[FactionType, int]: Faction to game count.
    """
    return {
        faction: sum(1 for game in games if faction in game.factions)
        for faction in get_factions(games)
    }


def get_name_win_count_dict(games: list[Game]) -> dict[NameType, int]:
    """
    Returns a dictionary mapping player names to the number of games they won.

    Args:
        games (list[Game]): List of games.

    Returns:
        dict[NameType, int]: Player name to win count.
    """
    return {name: get_num_wins(games, name) for name in get_names(games)}


def get_faction_win_count_dict(games: list[Game]) -> dict[FactionType, int]:
    """
    Returns a dictionary mapping factions to the number of games won by that faction.

    Args:
        games (list[Game]): List of games.

    Returns:
        dict[FactionType, int]: Faction to win count.
    """
    return {
        faction: sum(1 for game in games if game.winner_faction == faction)
        for faction in get_factions(games)
    }


def get_relative_name_win_count_dict(games: list[Game]) -> dict[NameType, float]:
    """
    Returns a dictionary mapping player names to their win rate.

    Args:
        games (list[Game]): List of games.

    Returns:
        dict[NameType, float]: Player name to win rate.
    """
    names = get_names(games)
    name_game_count_dict = get_name_game_count_dict(games)
    name_win_count_dict = get_name_win_count_dict(games)
    assert all(name in name_game_count_dict.keys() for name in names)
    assert all(name in name_win_count_dict.keys() for name in names)
    return {
        name: name_win_count_dict[name] / name_game_count_dict[name]
        for name in get_names(games)
    }


def get_relative_faction_win_count_dict(
    games: list[Game],
) -> dict[FactionType, float]:
    """
    Returns a dictionary mapping factions to their win rate.

    Args:
        games (list[Game]): List of games.

    Returns:
        dict[FactionType, float]: Faction to win rate.
    """
    factions = get_factions(games)
    faction_game_count_dict = get_faction_game_count_dict(games)
    faction_win_count_dict = get_faction_win_count_dict(games)
    assert all(faction in faction_game_count_dict.keys() for faction in factions)
    assert all(faction in faction_win_count_dict.keys() for faction in factions)
    return {
        faction: faction_win_count_dict[faction] / faction_game_count_dict[faction]
        for faction in get_factions(games)
    }


def plot_dict(
    dict: dict[FactionType, int]
    | dict[NameType, int]
    | dict[FactionType, float]
    | dict[NameType, float],
    title: str = "",
    xlabel: str = "",
    ylabel: str = "",
    ax: axes.Axes | None = None,
) -> None:
    """
    Plots a bar chart for a given dictionary of values.

    Args:
        dict: Dictionary to plot (keys as categories, values as counts or rates).
        title: Title of the plot.
        xlabel: Label for the x-axis.
        ylabel: Label for the y-axis.
        ax: Matplotlib Axes to plot on. If None, creates a new figure.
    """
    _ax = ax or plt.subplots()[1]
    _ax.bar(list(dict.keys()), list(dict.values()))
    _ax.set_title(title)
    _ax.set_xlabel(xlabel)
    _ax.set_ylabel(ylabel)
    if ax is None:
        plt.tight_layout()
        plt.show()


def plot_name_game_count(games: list[Game], ax: axes.Axes | None = None) -> None:
    """
    Plots the number of games played by each player.

    Args:
        games (list[Game]): List of games.
        ax (Axes, optional): Matplotlib Axes to plot on.
    """
    plot_dict(
        dict=get_name_game_count_dict(games),
        xlabel="Player Name",
        ylabel="# Games",
        ax=ax,
    )


def plot_name_win_count(games: list[Game], ax: axes.Axes | None = None) -> None:
    """
    Plots the number of wins for each player.

    Args:
        games (list[Game]): List of games.
        ax (Axes, optional): Matplotlib Axes to plot on.
    """
    plot_dict(
        dict=get_name_win_count_dict(games),
        xlabel="Player Name",
        ylabel="# Wins",
        ax=ax,
    )


def plot_relative_name_win_count(
    games: list[Game], ax: axes.Axes | None = None
) -> None:
    """
    Plots the win rate for each player.

    Args:
        games (list[Game]): List of games.
        ax (Axes, optional): Matplotlib Axes to plot on.
    """
    plot_dict(
        dict=get_relative_name_win_count_dict(games),
        xlabel="Player Name",
        ylabel="Win Rate",
        ax=ax,
    )


def plot_faction_game_count(games: list[Game], ax: axes.Axes | None = None) -> None:
    """
    Plots the number of games played by each faction.

    Args:
        games (list[Game]): List of games.
        ax (Axes, optional): Matplotlib Axes to plot on.
    """
    plot_dict(
        dict=get_faction_game_count_dict(games),
        xlabel="Faction",
        ylabel="# Games",
        ax=ax,
    )


def plot_faction_win_count(games: list[Game], ax: axes.Axes | None = None) -> None:
    """
    Plots the number of wins for each faction.

    Args:
        games (list[Game]): List of games.
        ax (Axes, optional): Matplotlib Axes to plot on.
    """
    plot_dict(
        dict=get_faction_win_count_dict(games),
        xlabel="Faction",
        ylabel="# Wins",
        ax=ax,
    )


def plot_relative_faction_win_count(
    games: list[Game], ax: axes.Axes | None = None
) -> None:
    """
    Plots the win rate for each faction.

    Args:
        games (list[Game]): List of games.
        ax (Axes, optional): Matplotlib Axes to plot on.
    """
    plot_dict(
        dict=get_relative_faction_win_count_dict(games),
        xlabel="Faction",
        ylabel="Win Rate",
        ax=ax,
    )


def plot_game_stats(games: list[Game]) -> None:
    """
    Plots a summary of game statistics in a 2x3 grid of subplots.

    Args:
        games (list[Game]): List of games.
    """
    fig, axs = plt.subplots(2, 3, figsize=(3 * 6, 2 * 4))
    plot_name_game_count(games, ax=axs[0, 0])
    plot_name_win_count(games, ax=axs[0, 1])
    plot_relative_name_win_count(games, ax=axs[0, 2])
    plot_faction_game_count(games, ax=axs[1, 0])
    plot_faction_win_count(games, ax=axs[1, 1])
    plot_relative_faction_win_count(games, ax=axs[1, 2])
    plt.tight_layout()
    plt.show()
