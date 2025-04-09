import neat
from game.game import Game
import sys
import base64
import pickle
from game.errors import TerminateSession

browser = sys.platform == "emscripten"
if browser:
    from platform import window  # type: ignore[attr-defined]


async def test_ai(game: Game):
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        "config.txt",
    )

    if browser:
        pickled_data_b64 = window.localStorage.getItem("best.pickle")
        if not pickled_data_b64:
            return
        pickle_data = base64.b64decode(pickled_data_b64)
        winner = pickle.loads(pickle_data)
    else:
        with open("best.pickle", "rb") as f:
            winner = pickle.load(f)

    game.setup_game(0.5)
    while True:
        game.setup_ai_env(
            genomes=[[0, winner]], config=config, best_genome=[0], ai=True
        )
        try:
            await game.game_loop()
        except TerminateSession:
            return
        game.round += 1
