import os
import keyboard
import time


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
    checkpoint_id_list = []
    while n_checkpoint < 8:
        checkpoint_id_list.append(i_checkpoint)
        n_checkpoint += 1
        i_checkpoint += 1
        if i_checkpoint >= len(checkpoints):
            i_checkpoint = 0
        if i_checkpoint == mouse_checkpoint:
            break
    return checkpoint_id_list


def scroll():
    checkpoints = get_checkpoints()
    mouse_checkpoint = 0
    while True:
        if keyboard.is_pressed("esc"):
            break
        if keyboard.is_pressed("down"):
            mouse_checkpoint += 1
            if mouse_checkpoint >= len(checkpoints):
                mouse_checkpoint = 0
        if keyboard.is_pressed("up"):
            mouse_checkpoint -= 1
            if mouse_checkpoint < 0:
                mouse_checkpoint = len(checkpoints) - 1
        time.sleep(0.1)
        checkpoint_id_list = create_checkpoint_id_list(checkpoints, mouse_checkpoint)
        os.system("clear")
        # print(checkpoint_id_list)
        for id in checkpoint_id_list:
            print(checkpoints[id])


scroll()
