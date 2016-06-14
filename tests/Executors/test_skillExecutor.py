#Under MIT License, see LICENSE.txt
# TODO : Modifier le nom des exceptions dans les tests
# TODO : Ajouter et modifier les tests quand implementee
from unittest import TestCase

from ai.InfoManager import InfoManager
from ai.Executor.SkillExecutor import SkillExecutor


from RULEngine.Game.Field import Field
from RULEngine.Game.Ball import Ball
from RULEngine.Game.Team import Team
from RULEngine.Game.Player import Player
from RULEngine.Util.Pose import Pose, Position
from RULEngine.Framework import GameState

__author__ = 'RoboCupULaval'


class TestSkillExecutor(TestCase):
    """Tests de la classe SkillExecutor"""

    def setUp(self):
        self.current_skill = None
        self.current_target = Pose(Position(0, 0), 0)
        self.current_goal = Pose(Position(1, 1), 1)

        # Initialisation de l'InfoManager avec des équipes de robots et une balle
        self.team = Team(True)
        for player in self.team.players:
            self.team.players[player.id].position = Position(100 * player.id, 100 * player.id)

        self.op_team = Team(False)
        for player in self.op_team.players:
            self.op_team.players[player.id].position = Position(-100 * player.id - 100, -100 * player.id - 100)

        self.field = Field(Ball())
        self.field.ball.set_position(Position(1000, 0), 1)
        self.info = InfoManager()

        game_state = GameState(self.field, None, self.team, self.op_team, {})
        self.info.update(game_state)

    def test_execSkillnNull(self):
        """Test la fonction exec si current_Skill == None"""
        self.assertRaises(Exception,self.current_skill,None)

    def test_execTargetNull(self):
        """Test la fonction exec si current_Skill == None"""
        self.assertRaises(Exception,self.current_target,None)

    def test_execGoalNull(self):
        """Test la fonction exec si current_Skill == None"""
        self.assertRaises(Exception,self.current_goal,None)











