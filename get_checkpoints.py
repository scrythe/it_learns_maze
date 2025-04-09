import os


def get_checkpoints():
    checkpoint_strings = os.listdir("checkpoints")
    checkpoints: list[int] = []
    for checkpoint_string in checkpoint_strings:
        checkpoint = int(checkpoint_string)
        checkpoints.append(checkpoint)
    checkpoints.sort()
    return checkpoints


def create_checkpoint_id_list(checkpoints, mouse_checkpoint):
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
