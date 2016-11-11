# Under MIT License, see LICENSE.txt

from ai.executors.executor import Executor
from ai.Util.types import AICommand
from RULEngine.Util.constant import PLAYER_PER_TEAM, ROBOT_RADIUS
from RULEngine.Util.geometry import get_distance

DEFAULT_STEP = 0.1 #100ms

class MovementExecutor(Executor):

    def __init__(self, p_world_state):
        super().__init__(p_world_state)
        self.future_pose = {}
        self.collisions = {}
        self.ai_commands = []
        self._init_collisions()

    def exec(self):
        """ En cas de collision, le robot avec l'id inferieur s'arrete """
        self.future_pose = {}
        self._init_collisions()
        self._detect_collisions()
        self.ai_commands = self.ws.play_state.current_ai_commands
        for pid in self.collisions:
            potential_collisions = self.collisions[pid]
            for collision in potential_collisions:
                if collision and pid < collision[0]:
                    pose = self.ws.game_state.my_team.players[pid].pose
                    self.ai_commands[pid] = AICommand(pose, 0)

        self.ws.play_state.current_ai_commands = self.ai_commands

    def _detect_collisions(self):
        self._compute_future_pose()
        self._check_collisions()

    def _compute_future_pose(self):
        for player in self.ws.game_state.my_team.players.values():
            actual_pose = player.pose
            velocity = player.velocity
            mov = velocity * DEFAULT_STEP
            self.future_pose[player.id] = actual_pose + mov

    def _check_collisions(self):
        for pid in self.future_pose:
            for other_pid in self.future_pose:
                position = self.future_pose[pid].position
                other_position = self.future_pose[other_pid].position
                dist = get_distance(position, other_position)
                if pid != other_pid and dist < ROBOT_RADIUS * 5:
                    self.collisions[pid].append((other_pid, other_position))

    def _init_collisions(self):
        self.collisions = {}
        for pid in range(PLAYER_PER_TEAM):
            self.collisions[pid] = []
