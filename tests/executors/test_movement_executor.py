# Under MIT License, see LICENSE.txt

import unittest
import copy

from ai.executors.movement_executor import MovementExecutor
from ai.states.world_state import WorldStateFactory
from ai.Util.types import AICommand
from RULEngine.Util.Pose import Pose
from RULEngine.Util.Position import Position
from RULEngine.Util.Vector import Vector


class TestMovementExecutor(unittest.TestCase):

    def setUp(self):
        world_state = WorldStateFactory.default_world_state()
        self.mov_exec = MovementExecutor(world_state)
        self.mov_exec.ws.game_state.my_team.players[0].pose = Pose(Position(500, 500))
        self.mov_exec.ws.game_state.my_team.players[1].pose = Pose(Position(600, 600))
        self.mov_exec.ws.game_state.my_team.players[2].pose = Pose(Position(1500, 500))
        self.mov_exec.ws.game_state.my_team.players[3].pose = Pose(Position(-600, 600))
        self.mov_exec.ws.game_state.my_team.players[4].pose = Pose(Position(2500, 500))
        self.mov_exec.ws.game_state.my_team.players[5].pose = Pose(Position(3600, 600))
        robot_zero_velocity = Vector()
        robot_zero_velocity.x = 500
        robot_zero_velocity.y = 500
        robot_one_velocity = Vector()
        robot_one_velocity.x = -500
        robot_one_velocity.y = -500
        self.mov_exec.ws.game_state.my_team.players[0].velocity = robot_zero_velocity
        self.mov_exec.ws.game_state.my_team.players[1].velocity = robot_one_velocity
        ai_commands = [AICommand(Pose(Position(100, 100)), 0), AICommand(Pose(), 0)]
        self.mov_exec.ws.play_state.current_ai_commands = ai_commands

    def test_exec_future_pose(self):
        self.mov_exec.exec()
        future_pose = self.mov_exec.future_pose
        self.assertEqual(Position(550, 550), future_pose[0].position)
        self.assertEqual(Position(550, 550), future_pose[1].position)
        for pid in range(2, 6):
            expected_pose = self.mov_exec.ws.game_state.my_team.players[pid].pose
            self.assertEqual(expected_pose, future_pose[pid])

    def test_exec_no_collision_except_zero_one(self):
        self.mov_exec.exec()
        collisions = self.mov_exec.collisions
        for pid in range(0, 2):
            self.assertNotEqual([], collisions[pid])
        for pid in range(2, 6):
            self.assertEqual([], collisions[pid])

    def test_exec_collision_zero_one(self):
        self.mov_exec.exec()
        collisions = self.mov_exec.collisions

        expected_collision_zero = [(1, Position(550, 550))]
        self.assertEqual(expected_collision_zero, collisions[0])

        expected_collision_one = [(0, Position(550, 550))]
        self.assertEqual(expected_collision_one, collisions[1])

    def test_exec_ai_command_collision(self):
        old_aicmd = copy.deepcopy(self.mov_exec.ws.play_state.current_ai_commands)
        self.mov_exec.exec()
        ai_commands = self.mov_exec.ai_commands
        expected_ai_command_zero = AICommand(Pose(Position(500, 500)), 0)
        expected_ai_command_one = AICommand(Pose(), 0)

        self.assertEqual(expected_ai_command_zero, ai_commands[0])
        self.assertEqual(expected_ai_command_one, ai_commands[1])
        self.assertNotEqual(old_aicmd, ai_commands)

    @unittest.skip("todo")
    def test_exec_ai_command_multi_collisions_first_not_considered(self):
        self.fail()
