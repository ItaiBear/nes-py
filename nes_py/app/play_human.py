"""A method to play gym environments using human IO inputs."""
import gym
from .._image_viewer import ImageViewer


# the sentinel value for "No Operation"
_NOP = 0


def play_human(env):
    """
    Play the environment using keyboard as a human.

    Args:
        env (gym.Env): the initialized gym environment to play

    Returns:
        None

    """
    fps = env.metadata['video.frames_per_second']

    # ensure the observation space is a box of pixels
    assert isinstance(env.observation_space, gym.spaces.box.Box)
    # ensure the observation space is either B&W pixels or RGB Pixels
    obs_s = env.observation_space
    is_bw = len(obs_s.shape) == 2
    is_rgb = len(obs_s.shape) == 3 and obs_s.shape[2] in [1, 3]
    assert is_bw or is_rgb
    # get the mapping of keyboard keys to actions in the environment
    if hasattr(env, 'get_keys_to_action'):
        keys_to_action = env.get_keys_to_action()
    elif hasattr(env.unwrapped, 'get_keys_to_action'):
        keys_to_action = env.unwrapped.get_keys_to_action()
    else:
        raise ValueError('env has no get_keys_to_action method')
    # create the image viewer
    viewer = ImageViewer(
        env.spec.id if env.spec is not None else env.__class__.__name__,
        env.observation_space.shape[0], # height
        env.observation_space.shape[1], # width
        monitor_keyboard=True,
        relevant_keys=set(sum(map(list, keys_to_action.keys()), []))
    )
    # create a done flag for the environment
    done = True
    # start the main game loop
    try:
        while True:
            # reset if the environment is done
            if done:
                done = False
                screen = env.reset()
                viewer.show(screen)
            # unwrap the action based on pressed relevant keys
            action = keys_to_action.get(viewer.pressed_keys, _NOP)
            screen, reward, done, info = env.step(action)
            viewer.show(screen)
            # shutdown if the escape key is pressed
            if viewer.is_escape_pressed:
                break
    except KeyboardInterrupt:
        pass

    viewer.close()
    env.close()


# explicitly define the outward facing API of the module
__all__ = [play_human.__name__]
