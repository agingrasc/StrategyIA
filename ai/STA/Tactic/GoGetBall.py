# Under MIT licence, see LICENCE.txt

from ai.STA.Tactic.Tactic import Tactic
from ai.STA.Tactic.GoToPosition import GoToPosition
from ai.STA.Action.GoBehind import GoBehind
from ai.STA.Action.GrabBall import GrabBall
from ai.STA.Action.Idle import Idle
from ai.STA.Tactic import tactic_constants

from RULEngine.Util.area import player_can_grab_ball, player_grabbed_ball
from RULEngine.Util.geometry import get_distance
from RULEngine.Util.constant import DISTANCE_BEHIND, PLAYER_PER_TEAM, POSITION_DEADZONE, BALL_RADIUS
from RULEngine.Util.Pose import Pose
from RULEngine.Util.Position import Position

__author__ = 'RoboCupULaval'

POSITION_DEADZONE = POSITION_DEADZONE + BALL_RADIUS


class GoGetBall(Tactic):
    """
    méthodes:
        exec(self) : Exécute une Action selon l'état courant
    attributs:
        info_manager: référence à la façade InfoManager
        player_id : Identifiant du joueur auquel est assigné la tactique
        current_state : L'état courant de la tactique
        next_state : L'état suivant de la tactique
        status_flag : L'indicateur de progression de la tactique
        target: Position à laquelle faire face après avoir pris la balle
    """

    def __init__(self, info_manager, player_id, target=Pose()):
        Tactic.__init__(self, info_manager, target)
        assert isinstance(player_id, int)
        assert PLAYER_PER_TEAM >= player_id >= 0

        self.player_id = player_id
        self.current_state = self.get_behind_ball
        self.next_state = self.get_behind_ball

        self.move_action = GoToPosition(self.info_manager, self.player_id, self.info_manager.get_player_pose(self.player_id))
        self.move_action.status_flag = tactic_constants.SUCCESS

    def get_behind_ball(self):
        self.status_flag = tactic_constants.WIP
        ball_position = self.info_manager.get_ball_position()
        move_action_status = self.move_action.status_flag

        dist = self._get_distance_from_ball()
        if move_action_status == tactic_constants.SUCCESS and dist <= POSITION_DEADZONE:
            self.next_state = self.halt
        elif move_action_status == tactic_constants.SUCCESS and dist > POSITION_DEADZONE:
            self.move_action = self._generate_move_to()
            self.next_state = self.get_behind_ball
        else:
            self.next_state = self.get_behind_ball

        return self.move_action

    def grab_ball(self):
        if player_grabbed_ball(self.info_manager, self.player_id):
            self.next_state = self.halt
            self.status_flag = tactic_constants.SUCCESS
        elif player_can_grab_ball(self.info_manager, self.player_id):
            self.next_state = self.grab_ball
        else:
            self.next_state = self.get_behind_ball  # back to go_behind; the ball has moved

        grab_ball = GrabBall(self.info_manager,self.player_id)
        return grab_ball

    def halt(self, reset=False):
        self.status_flag = tactic_constants.SUCCESS
        dist = self._get_distance_from_ball()

        if dist > POSITION_DEADZONE:
            self.next_state = self.get_behind_ball
        else:
            self.next_state = self.halt

        if reset:
            self.move_action = self._generate_move_to()

        return Idle(self.info_manager, self.player_id)

    def _get_distance_from_ball(self):
        return get_distance(self.info_manager.get_player_pose(self.player_id).position, self.info_manager.get_ball_position())

    def _generate_move_to(self):
        go_behind = GoBehind(self.info_manager, self.player_id, self.info_manager.get_ball_position(), self.target.position, DISTANCE_BEHIND)
        destination = go_behind.exec().move_destination
        return GoToPosition(self.info_manager, self.player_id, destination)
