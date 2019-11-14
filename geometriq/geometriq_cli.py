from datetime import datetime
from math import floor
import os
import os.path
import sys
from time import time

import click
import opensimplex

from geometriq import *


@click.command()
@click.option(
    "--dimensions",
    help="Dimensions to use, formatted as \"width_height\", or a device name shorthand: \"ipad\" (1668x2388), \"iphone\" (1125x2436), \"macbook\" (1440x900), \"4k\" (3008x1692), \"square\" (4096x4096). Defaults to \"square\".",
    type=str,
    default="square",
)
@click.option(
    "--geometriq-directory",
    help="Directory where geometriq scripts can be found. Can be set in $GEOMETRIQ_DIRECTORY. Defaults to the current directory.",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    envvar="GEOMETRIQ_DIRECTORY",
    default=".",
)
@click.option(
    "--output-dir",
    help="Directory where resulting images should be saved. Can be set in $GEOMETRIQ_OUTPUT_DIRECTORY. Defaults to the current directory.",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    envvar="GEOMETRIQ_OUTPUT_DIRECTORY",
    default=".",
)
@click.option(
    "--contrast",
    "-c",
    help="Contrast theme background. Defaults to \"light\"",
    type=click.Choice(["dark", "light", "black", "white", "clear"]),
    default="light",
)
@click.option("--seed", "-s", help="Randomization seed. Defaults to the current time.", type=int)
@click.argument("geometriq-script")
def geometriq_cli(
    dimensions, geometriq_directory, output_dir, contrast, seed, geometriq_script
):
    """Generate art from a GEOMETRIQ_SCRIPT.
    """

    devices = {
        "ipad": "1668_2388",
        "iphone": "1125_2436",
        "macbook": "1440_900",
        "4k": "3008_1692",
        "square": "4096_4096",
    }

    background_fills = {
        "dark": base03,
        "light": base3,
        "black": black,
        "white": white,
        "clear": clear,
    }

    strokes = {
        "dark": base1,
        "light": base01,
        "black": white,
        "white": black,
        "clear": base01,
    }

    if not seed:
        seed = floor(time())

    DEBUG = os.getenv("GEOMETRIQ_DEBUG", False)

    sys.path.append(geometriq_directory)

    dimensions = dimensions if "_" in dimensions else devices[dimensions]
    width, height = [int(x) for x in dimensions.split("_")]

    script_name = os.path.splitext(os.path.basename(geometriq_script))[0]
    dated_name = f"{script_name}_{width}x{height}_{seed}"

    script = __import__("{}".format(script_name), globals(), locals(), ["draw"], 0)

    outputDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), output_dir)
    filename = os.path.join(outputDir, "{}".format(dated_name))

    canvas = CoreGraphicsCanvas(filename, width, height, seed, debug=DEBUG)
    canvas.set_miter_limit(15)
    canvas.set_line_cap(kCGLineCapRound)
    canvas.set_line_join(kCGLineJoinMiter)
    canvas.set_stroke_color(clear)
    canvas.set_stroke_width(4)
    canvas.set_fill_color(background_fills[contrast])

    canvas.fill_background()

    canvas.set_stroke_color(strokes[contrast])
    canvas.set_fill_color(clear)

    try:
        script.draw(canvas)
    except KeyboardInterrupt:
        pass
    finally:
        canvas.save()


if __name__ == "__main__":
    geometriq_cli()
