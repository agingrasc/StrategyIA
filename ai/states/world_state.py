# Under MIT License, see LICENSE.txt

from ai.Debug.debug_interface import DebugInterface
from ai.states.debug_state import DebugState
from ai.states.game_state import GameState
from ai.states.play_state import PlayState
from ai.states.module_state import ModuleState
from RULEngine.Game.Team import Team
from RULEngine.Util.Pose import Pose
from RULEngine.Util.Position import Position


class WorldState:
    def __init__(self, mode_debug_active=True):
        self.mode_debug_active = mode_debug_active
        self.module_state = ModuleState()
        self.play_state = PlayState()
        self.game_state = GameState()

        if mode_debug_active:
            self.debug_state = DebugState()
            self.debug_interface = DebugInterface()

    def update(self, game_state):
        self.game_state.update(game_state)

        if self.mode_debug_active:
            self.debug_state.update(game_state.debug)

    def set_team_color(self, p_our_team_color):
        self.game_state.set_team_color(p_our_team_color)


class WorldStateFactory(object):

    @staticmethod
    def default_world_state():
        world_state = WorldState(False)
        game_state = GameState()
        team = Team(False)
        team.players[0].pose = Pose(Position(500, 500))
        team.players[1].pose = Pose(Position(600, 600))
        game_state.my_team = team
        world_state.game_state = game_state
        return world_state
