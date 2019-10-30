from datetime import datetime
from math import floor
import os
import os.path
import random
import sys
from time import time

import click

from geometriq import *


@click.command()
@click.argument('geometriq-script')
@click.argument('width', type=int)
@click.argument('height', type=int)
@click.option('--geometriq-directory', help='directory where geometriq scripts can be found', type=click.Path(exists=True, file_okay=False, dir_okay=True), envvar='GEOMETRIQ_DIRECTORY')
@click.option('--output-dir', help='directory where resulting images should be saved', type=click.Path(exists=True, file_okay=False, dir_okay=True), envvar='GEOMETRIQ_OUTPUT_DIRECTORY')
@click.option('--contrast', '-c', help='contrast theme', type=click.Choice(['dark', 'light', 'black', 'white', 'clear']), default='light')
@click.option('--seed', '-s', help='randomization seed', type=int)
def geometriq_cli(geometriq_script, width, height, geometriq_directory, output_dir, contrast, seed):

    background_fills = {
        'dark': base03,
        'light': base3,
        'black': black,
        'white': white,
        'clear': clear
    }

    strokes = {
        'dark': base1,
        'light': base01,
        'black': white,
        'white': black,
        'clear': base01
    }

    if not seed:
        seed = floor(time())

    random.seed(seed)
        
    DEBUG = os.getenv('GEOMETRIQ_DEBUG', False)

    sys.path.append(geometriq_directory)

    script_name = os.path.splitext(os.path.basename(geometriq_script))[0]
    dated_name = f"{script_name}_{width}x{height}_{seed}"

    script = __import__('{}'.format(script_name), globals(), locals(), ['draw'], 0)

    outputDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), output_dir)
    filename = os.path.join(outputDir, "{}".format(dated_name))

    canvas = CoreGraphicsCanvas(filename, width, height, debug=DEBUG)
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
