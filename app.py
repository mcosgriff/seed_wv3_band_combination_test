import argparse
import logging
import os

import numpy as np

from band_combinations import GeneralLandCover, Water, ExposedSoil, RoofingAndRoads, ArtificialFeaturesInDesert
from enums import BandCombination


def run(args: argparse.Namespace) -> None:
    band_combination = np.array([])
    which_algorithm = BandCombination[args.band_combination]

    if which_algorithm == BandCombination.GENERAL_LAND_COVER:
        band_combination = GeneralLandCover(args.image_path, args.output_directory)
    elif which_algorithm == BandCombination.WATER:
        band_combination = Water(args.image_path, args.output_directory)
    elif which_algorithm == BandCombination.EXPOSED_SOIL:
        band_combination = ExposedSoil(args.image_path, args.output_directory)
    elif which_algorithm == BandCombination.ROOFING_AND_ROADS:
        band_combination = RoofingAndRoads(args.image_path, args.output_directory)
    elif which_algorithm == BandCombination.ARTIFICIAL_FEATURES_IN_DESERT:
        band_combination = ArtificialFeaturesInDesert(args.image_path, args.output_directory)

    if band_combination:
        with band_combination:
            red, green, blue = band_combination.process_band_combination()

            if red.size > 0 and green.size > 0 and blue.size > 0:
                rgb_raster_path = band_combination.save_output(red, green, blue)
                logger.info('RGB image saved to {}'.format(rgb_raster_path))


def build_cmd_line_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Load WV3 16 band image and run index on it.')
    parser.add_argument('--verbose', help='Output extra logging at DEBUG level', action='store_true')
    parser.add_argument('--band-combination', help='Which index to run on the WV3 image', required=True,
                        choices=['GENERAL_LAND_COVER', 'WATER', 'EXPOSED_SOIL', 'VEGETATION', 'ROOFING_AND_ROADS',
                                 'ARTIFICIAL_FEATURES_IN_DESERT', 'ARTIFICIAL_FEATURES_IN_VEGETATION',
                                 'UNDERWATER_OBSTRUCTION', 'DIRECTION_OF_TRAVEL', 'POLYMERS_PLASTICS',
                                 'SEEING_FIRE_THROUGH_SMOKE', 'FIRES', 'FIRES_AND_CHARRED_VEGETATION', 'MINERALS',
                                 'SOIL_MOISTURE', 'STANDING_WATER', 'METAL'])
    parser.add_argument('--image-path', help='Path to WV3 16 band image', required=True, type=str)
    parser.add_argument('--output-directory', help='Where to store the output', required=True, type=str)

    return parser.parse_args()


if __name__ == '__main__':
    _args = build_cmd_line_args()

    if _args.verbose:
        logging.basicConfig(level=logging.DEBUG, format="%(threadName)s::%(asctime)s::%(message)s")
    else:
        logging.basicConfig(level=logging.INFO, format="%(threadName)s::%(asctime)s::%(message)s")
    logger = logging.getLogger('wv3_band_combination_processing')

    if not os.path.exists(_args.output_directory):
        os.makedirs(_args.output_directory)

    run(_args)
