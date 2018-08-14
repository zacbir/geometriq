from datetime import datetime
import os
import os.path
import sys

import click

from geometer import *


@click.command()
@click.argument('geometer-script')
@click.argument('width', type=int)
@click.argument('height', type=int)
@click.option('--geometer-directory', help='directory where geometer scripts can be found', type=click.Path(exists=True, file_okay=False, dir_okay=True), envvar='GEOMETER_DIRECTORY')
@click.option('--output-dir', help='directory where resulting images should be saved', type=click.Path(exists=True, file_okay=False, dir_okay=True), envvar='GEOMETER_OUTPUT_DIRECTORY')
@click.option('--contrast', '-c', help='contrast theme', type=click.Choice(['dark', 'light', 'clear']), default='light')
def geometer_cli(geometer_script, width, height, geometer_directory, output_dir, contrast):

    background_fills = {
        'dark': base03,
        'light': base3,
        'clear': clear
    }

    strokes = {
        'dark': base1,
        'light': base01,
        'clear': base01
    }

    DEBUG = os.getenv('GEOMETER_DEBUG', False)

    sys.path.append(geometer_directory)

    script_name = os.path.splitext(os.path.basename(geometer_script))[0]
    dated_name = "{}_{}x{}_{}".format(script_name, width, height, datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))

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
    geometer_cli()