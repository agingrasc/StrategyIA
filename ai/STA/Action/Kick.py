# Under MIT license, see LICENSE.txt
from .Action import Action
from ...Util.types import AICommand

class Kick(Action):
    '''
    Action Kick: Actionne le kick du robot
    Méthodes :
        exec(self): Retourne la position actuelle et une force de kick
    Attributs (en plus de ceux de Action):
        player_id : L'identifiant du joueur qui doit frapper la balle
    '''
    def __init__(self, p_info_manager, p_player_id, p_force):
        """
            :param pInfoManager: référence vers l'InfoManager
            :param pPlayerId: Identifiant du joueur qui frappe la balle
            :param pForce: force du kicker (float entre 0 et 1)
        """
        Action.__init__(self, p_info_manager)
        self.player_id = p_player_id
        self.force = p_force

    def exec(self):
        """
        Execute le kick
        :return: Un tuple (Pose, kick)
                     où Pose est la destination actuelle du joueur (ne pas la modifier)
                        kick est un float entre 0 et 1 qui determine la force du kick
        """
        position_joueur = self.info_manager.get_player_pose(self.player_id)
        force_kick = self.force
        return AICommand(position_joueur, force_kick)
