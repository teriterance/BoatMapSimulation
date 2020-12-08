from gym.envs.registration import register

register(
    id='boat-v0',
    entry_point='gym_boat.envs:boatEnv',
)
register(
    id='boat-extrahard-v0',
    entry_point='gym_boat.envs:boatExtraHardEnv',
)