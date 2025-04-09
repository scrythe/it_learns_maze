import os
import sys

browser = True if sys.platform == "emscripten" else False
if browser:
    from platform import window  # type: ignore[attr-defined]


def get_pc_checkpoints() -> list[int]:
    checkpoint_strings = os.listdir("checkpoints")
    checkpoints: list[int] = []
    for checkpoint_string in checkpoint_strings:
        checkpoint = int(checkpoint_string)
        checkpoints.append(checkpoint)
    checkpoints.sort()
    return checkpoints


def get_browser_checkpoints() -> list[int]:
    checkpoints: list[int] = []
    for i in range(window.localStorage.length):
        key = window.localStorage.key(i)
        key = key.split("/")
        if key[0] == "checkpoints":
            checkpoint = int(key[1])
            checkpoints.append(checkpoint)
    return checkpoints


def get_checkpoints():
    if browser:
        return get_browser_checkpoints()
    return get_pc_checkpoints()


def create_checkpoint_id_list(checkpoints, mouse_checkpoint) -> list[int]:
    n_checkpoint = 0
    i_checkpoint = mouse_checkpoint
    checkpoint_id_list: list[int] = []
    while n_checkpoint < 8:
        checkpoint_id_list.append(i_checkpoint)
        n_checkpoint += 1
        i_checkpoint += 1
        if i_checkpoint >= len(checkpoints):
            i_checkpoint = 0
        if i_checkpoint == mouse_checkpoint:
            break
    return checkpoint_id_list
